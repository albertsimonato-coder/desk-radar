"""Open / closed / new / reappeared transitions, driven through the real runner with fixtures."""

from datetime import UTC, datetime, timedelta
from pathlib import Path

import yaml

from radar import runner
from radar.profile import load_profile
from radar.render import build_payload, is_new
from radar.store import Store

GH_SLICE = "greenhouse_flow-traders.json"


def _write_registry(tmp_path: Path, companies: list[dict]) -> Path:
    p = tmp_path / "companies.yaml"
    p.write_text(yaml.safe_dump(companies))
    return p


def _registry(tmp_path):
    return _write_registry(
        tmp_path,
        [
            {
                "name": "Flow Traders",
                "priority": 1,
                "group": "prop_trading",
                "ats": "greenhouse",
                "config": {"board": "flowtraders"},
                "careers_url": "https://www.flowtraders.com/careers",
            },
            {
                "name": "Gunvor",
                "priority": 2,
                "group": "commodities",
                "ats": "workday",
                "config": {"tenant": "gunvor", "wd": "wd3", "site": "Gunvor_Careers"},
                "careers_url": "https://centalion.com/careers/",
            },
        ],
    )


def _run(tmp_path, fixtures_dir, now, tier="all"):
    return runner.run(
        tier,
        db_path=tmp_path / "radar.sqlite",
        companies_path=tmp_path / "companies.yaml",
        profile_path=runner.DEFAULT_PROFILE,
        docs_dir=tmp_path / "docs",
        dry_run=True,
        use_llm=False,
        now=now,
    )


def _point_fixtures(monkeypatch, d: Path):
    monkeypatch.setattr(runner, "FIXTURES", d)


def test_first_run_everything_is_new_then_stable(tmp_path, monkeypatch):
    _registry(tmp_path)
    _point_fixtures(monkeypatch, runner.FIXTURES)  # real recorded fixtures
    t0 = datetime(2026, 10, 23, 6, 0, tzinfo=UTC)
    r1 = _run(tmp_path, None, t0)
    assert r1.sources_ok == 2 and r1.new == r1.seen > 0
    r2 = _run(tmp_path, None, t0 + timedelta(days=1))
    assert r2.new == 0 and r2.closed == 0 and r2.seen == r1.seen
    store = Store(tmp_path / "radar.sqlite")
    assert store.counts() == {"total": r1.seen, "open": r1.seen}
    assert (tmp_path / "docs" / "index.html").exists() and (tmp_path / "docs" / "new.html").exists()


def test_closed_after_two_misses_reappear_not_new(tmp_path, monkeypatch):
    import json
    import shutil

    _registry(tmp_path)
    fx = tmp_path / "fx"
    fx.mkdir()
    shutil.copy(runner.FIXTURES / GH_SLICE, fx / GH_SLICE)
    shutil.copy(runner.FIXTURES / "workday_gunvor.json", fx / "workday_gunvor.json")
    _point_fixtures(monkeypatch, fx)
    full = json.loads((fx / GH_SLICE).read_text())
    t0 = datetime(2026, 10, 1, 6, 0, tzinfo=UTC)

    _run(tmp_path, fx, t0)
    store = Store(tmp_path / "radar.sqlite")
    victim = sorted(store.openings_for_company("flow-traders"), key=lambda o: o.title)[0]
    store.close()

    # Remove the victim from the source for two consecutive runs.
    reduced = dict(full)
    reduced["jobs"] = [j for j in full["jobs"] if str(j["id"]) != victim.external_id]
    (fx / GH_SLICE).write_text(json.dumps(reduced))

    r = _run(tmp_path, fx, t0 + timedelta(days=1))
    store = Store(tmp_path / "radar.sqlite")
    o = store.get(victim.dedup_key)
    assert o.status == "open" and o.missing_runs == 1 and r.closed == 0
    store.close()

    r = _run(tmp_path, fx, t0 + timedelta(days=2))
    store = Store(tmp_path / "radar.sqlite")
    o = store.get(victim.dedup_key)
    assert o.status == "closed" and r.closed == 1
    assert store.counts()["total"] == store.counts()["open"] + 1  # nothing deleted
    store.close()

    # Source failure must NOT count as a miss: use a broken fixture for one run.
    (fx / GH_SLICE).write_text("{}")
    r = _run(tmp_path, fx, t0 + timedelta(days=3))
    assert "flow-traders" in r.errors and r.sources_ok == 1
    store = Store(tmp_path / "radar.sqlite")
    others = [
        x for x in store.openings_for_company("flow-traders") if x.dedup_key != victim.dedup_key
    ]
    assert all(x.missing_runs == 0 and x.status == "open" for x in others)
    store.close()

    # Victim comes back: open again, reopened flag set, not new.
    (fx / GH_SLICE).write_text(json.dumps(full))
    t4 = t0 + timedelta(days=4)
    r = _run(tmp_path, fx, t4)
    assert r.new == 0 and r.reopened == 1
    store = Store(tmp_path / "radar.sqlite")
    o = store.get(victim.dedup_key)
    assert o.status == "open" and o.reopened == 1 and o.missing_runs == 0
    assert o.first_seen == t0  # history preserved
    profile = load_profile(runner.DEFAULT_PROFILE)
    assert not is_new(o, t4, profile["new_window_days"])
    payload = build_payload(store, profile, now=t4)
    row = next(x for x in payload["rows"] if x["k"] == victim.dedup_key)
    assert row["new"] is False and row["new_run"] is False and row["reopened"] == 1
    # Everything else was first seen 4 days ago (inside the 7-day window) and is new;
    # the reopened one is the only exception.
    assert payload["counts"]["new"] == payload["counts"]["open"] - 1
    store.close()


def test_new_window_and_new_since_last_run(tmp_path, monkeypatch):
    _registry(tmp_path)
    _point_fixtures(monkeypatch, runner.FIXTURES)
    profile = load_profile(runner.DEFAULT_PROFILE)
    t0 = datetime(2026, 9, 1, tzinfo=UTC)
    r1 = _run(tmp_path, None, t0)
    # 30 days later nothing is "new" anymore, even though all are still open.
    t1 = t0 + timedelta(days=30)
    _run(tmp_path, None, t1)
    store = Store(tmp_path / "radar.sqlite")
    payload = build_payload(store, profile, now=t1)
    assert payload["counts"]["open"] == r1.seen
    assert payload["counts"]["new"] == 0 and payload["counts"]["new_run"] == 0
    store.close()


def test_daily_tier_selects_priority(tmp_path, monkeypatch):
    _registry(tmp_path)
    _point_fixtures(monkeypatch, runner.FIXTURES)
    wednesday = datetime(2026, 10, 21, tzinfo=UTC)
    r = _run(tmp_path, None, wednesday, tier="daily")
    assert r.sources_total == 1  # Gunvor is priority 2
    monday = datetime(2026, 10, 19, tzinfo=UTC)
    r = _run(tmp_path, None, monday, tier="daily")
    assert r.sources_total == 2
