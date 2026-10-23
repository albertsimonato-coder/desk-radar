"""SQLite persistence: openings, runs, source_health. Nothing is ever deleted."""

from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from radar.models import Opening, ScoreBreakdown

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
  run_id        INTEGER PRIMARY KEY AUTOINCREMENT,
  started_at    TEXT NOT NULL,
  finished_at   TEXT,
  tier          TEXT NOT NULL,
  sources_total INTEGER DEFAULT 0,
  sources_ok    INTEGER DEFAULT 0,
  openings_seen INTEGER DEFAULT 0,
  openings_new  INTEGER DEFAULT 0,
  dry_run       INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS openings (
  dedup_key           TEXT PRIMARY KEY,
  company_slug        TEXT NOT NULL,
  company_name        TEXT NOT NULL,
  "group"             TEXT NOT NULL,
  priority            INTEGER NOT NULL,
  external_id         TEXT NOT NULL,
  title               TEXT NOT NULL,
  title_norm          TEXT NOT NULL,
  location_raw        TEXT NOT NULL DEFAULT '',
  city                TEXT NOT NULL DEFAULT '',
  country             TEXT NOT NULL DEFAULT '',
  department          TEXT NOT NULL DEFAULT '',
  posted_at           TEXT,
  url                 TEXT NOT NULL,
  description_snippet TEXT NOT NULL DEFAULT '',
  employment_type_raw TEXT NOT NULL DEFAULT '',
  employment_type     TEXT NOT NULL DEFAULT 'other',
  function            TEXT NOT NULL DEFAULT 'other',
  classified_by       TEXT NOT NULL DEFAULT 'rules',
  fit_score           REAL NOT NULL DEFAULT 0,
  score_breakdown     TEXT NOT NULL DEFAULT '{}',
  first_seen          TEXT NOT NULL,
  last_seen           TEXT NOT NULL,
  status              TEXT NOT NULL DEFAULT 'open',
  first_run_id        INTEGER NOT NULL,
  missing_runs        INTEGER NOT NULL DEFAULT 0,
  reopened            INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_openings_company ON openings(company_slug);
CREATE INDEX IF NOT EXISTS idx_openings_status ON openings(status);
CREATE INDEX IF NOT EXISTS idx_openings_first_seen ON openings(first_seen);

CREATE TABLE IF NOT EXISTS source_health (
  company_slug   TEXT PRIMARY KEY,
  company_name   TEXT NOT NULL,
  ats            TEXT NOT NULL,
  last_run_id    INTEGER,
  last_attempt   TEXT,
  last_success   TEXT,
  last_error     TEXT,
  last_error_at  TEXT,
  last_count     INTEGER DEFAULT 0,
  consecutive_failures INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS llm_cache (
  dedup_key  TEXT PRIMARY KEY,
  model      TEXT NOT NULL,
  result     TEXT NOT NULL,
  created_at TEXT NOT NULL
);
"""


def _iso(dt: datetime | None) -> str | None:
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC).isoformat(timespec="seconds")


def _parse(s: str | None) -> datetime | None:
    if not s:
        return None
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt


def now_utc() -> datetime:
    return datetime.now(UTC).replace(microsecond=0)


class Store:
    def __init__(self, path: str | Path = ":memory:"):
        self.path = str(path)
        if self.path != ":memory:":
            Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)

    def close(self) -> None:
        self.conn.close()

    # ---- runs -------------------------------------------------------------
    def start_run(self, tier: str, dry_run: bool = False) -> int:
        cur = self.conn.execute(
            "INSERT INTO runs (started_at, tier, dry_run) VALUES (?, ?, ?)",
            (_iso(now_utc()), tier, int(dry_run)),
        )
        self.conn.commit()
        return int(cur.lastrowid)

    def finish_run(self, run_id: int, **counts: int) -> None:
        sets = ", ".join(f"{k} = ?" for k in counts)
        params = [*counts.values(), _iso(now_utc()), run_id]
        self.conn.execute(
            f"UPDATE runs SET {sets}{', ' if sets else ''}finished_at = ? WHERE run_id = ?", params
        )
        self.conn.commit()

    def last_run(self) -> sqlite3.Row | None:
        return self.conn.execute(
            "SELECT * FROM runs WHERE finished_at IS NOT NULL ORDER BY run_id DESC LIMIT 1"
        ).fetchone()

    def previous_run_id(self, before_run_id: int) -> int | None:
        row = self.conn.execute(
            "SELECT run_id FROM runs WHERE finished_at IS NOT NULL AND run_id < ? "
            "ORDER BY run_id DESC LIMIT 1",
            (before_run_id,),
        ).fetchone()
        return int(row["run_id"]) if row else None

    # ---- openings ---------------------------------------------------------
    def get(self, dedup_key: str) -> Opening | None:
        row = self.conn.execute(
            "SELECT * FROM openings WHERE dedup_key = ?", (dedup_key,)
        ).fetchone()
        return self._row_to_opening(row) if row else None

    def upsert(self, o: Opening) -> None:
        d = o.model_dump()
        d["posted_at"] = _iso(o.posted_at)
        d["first_seen"] = _iso(o.first_seen)
        d["last_seen"] = _iso(o.last_seen)
        d["score_breakdown"] = json.dumps(o.score_breakdown.model_dump())
        cols = list(d.keys())
        quoted = ", ".join(f'"{c}"' for c in cols)
        placeholders = ", ".join("?" for _ in cols)
        updates = ", ".join(f'"{c}" = excluded."{c}"' for c in cols if c != "dedup_key")
        self.conn.execute(
            f"INSERT INTO openings ({quoted}) VALUES ({placeholders}) "
            f"ON CONFLICT(dedup_key) DO UPDATE SET {updates}",
            [d[c] for c in cols],
        )

    def commit(self) -> None:
        self.conn.commit()

    def openings_for_company(self, company_slug: str) -> list[Opening]:
        rows = self.conn.execute(
            "SELECT * FROM openings WHERE company_slug = ?", (company_slug,)
        ).fetchall()
        return [self._row_to_opening(r) for r in rows]

    def all_openings(self) -> list[Opening]:
        rows = self.conn.execute("SELECT * FROM openings").fetchall()
        return [self._row_to_opening(r) for r in rows]

    def mark_missing(self, company_slug: str, seen_keys: set[str], run_id: int) -> int:
        """Openings of this company not seen in this successful run: bump missing_runs;
        after two consecutive misses, mark closed. Returns number newly closed."""
        closed = 0
        for o in self.openings_for_company(company_slug):
            if o.dedup_key in seen_keys:
                continue
            if o.status == "closed":
                continue
            o.missing_runs += 1
            if o.missing_runs >= 2:
                o.status = "closed"
                closed += 1
            self.upsert(o)
        return closed

    def _row_to_opening(self, r: sqlite3.Row) -> Opening:
        d = dict(r)
        d["posted_at"] = _parse(d["posted_at"])
        d["first_seen"] = _parse(d["first_seen"])
        d["last_seen"] = _parse(d["last_seen"])
        d["score_breakdown"] = ScoreBreakdown.model_validate(
            json.loads(d["score_breakdown"] or "{}")
        )
        return Opening.model_validate(d)

    # ---- source health ----------------------------------------------------
    def record_source_success(
        self, slug: str, name: str, ats: str, run_id: int, count: int
    ) -> None:
        ts = _iso(now_utc())
        self.conn.execute(
            """INSERT INTO source_health
               (company_slug, company_name, ats, last_run_id, last_attempt, last_success,
                last_count, consecutive_failures)
               VALUES (?, ?, ?, ?, ?, ?, ?, 0)
               ON CONFLICT(company_slug) DO UPDATE SET
                 company_name = excluded.company_name, ats = excluded.ats,
                 last_run_id = excluded.last_run_id, last_attempt = excluded.last_attempt,
                 last_success = excluded.last_success, last_count = excluded.last_count,
                 consecutive_failures = 0""",
            (slug, name, ats, run_id, ts, ts, count),
        )
        self.conn.commit()

    def record_source_error(self, slug: str, name: str, ats: str, run_id: int, error: str) -> None:
        ts = _iso(now_utc())
        self.conn.execute(
            """INSERT INTO source_health
               (company_slug, company_name, ats, last_run_id, last_attempt, last_error,
                last_error_at, consecutive_failures)
               VALUES (?, ?, ?, ?, ?, ?, ?, 1)
               ON CONFLICT(company_slug) DO UPDATE SET
                 company_name = excluded.company_name, ats = excluded.ats,
                 last_run_id = excluded.last_run_id, last_attempt = excluded.last_attempt,
                 last_error = excluded.last_error, last_error_at = excluded.last_error_at,
                 consecutive_failures = source_health.consecutive_failures + 1""",
            (slug, name, ats, run_id, ts, error[:500], ts),
        )
        self.conn.commit()

    def source_health(self) -> list[dict]:
        rows = self.conn.execute("SELECT * FROM source_health ORDER BY company_name").fetchall()
        return [dict(r) for r in rows]

    # ---- llm cache --------------------------------------------------------
    def llm_cache_get(self, dedup_key: str) -> dict | None:
        row = self.conn.execute(
            "SELECT result FROM llm_cache WHERE dedup_key = ?", (dedup_key,)
        ).fetchone()
        return json.loads(row["result"]) if row else None

    def llm_cache_put(self, dedup_key: str, model: str, result: dict) -> None:
        self.conn.execute(
            "INSERT OR REPLACE INTO llm_cache (dedup_key, model, result, created_at) "
            "VALUES (?, ?, ?, ?)",
            (dedup_key, model, json.dumps(result), _iso(now_utc())),
        )
        self.conn.commit()

    # ---- stats ------------------------------------------------------------
    def counts(self) -> dict[str, int]:
        total = self.conn.execute("SELECT COUNT(*) FROM openings").fetchone()[0]
        open_ = self.conn.execute("SELECT COUNT(*) FROM openings WHERE status='open'").fetchone()[0]
        return {"total": int(total), "open": int(open_)}
