"""Parallel fetching: hosts do not block each other, and results match a sequential run."""

import threading
import time
from datetime import UTC, datetime

import yaml

from radar import runner
from radar.adapters.base import _HostThrottle
from radar.store import Store


def test_throttle_is_per_host_and_does_not_hold_the_lock_while_sleeping():
    t = _HostThrottle(interval=0.3)
    stamps: dict[str, list[float]] = {"a": [], "b": [], "c": []}

    def hit(host: str) -> None:
        for _ in range(3):
            t.wait(f"https://{host}.test/x")
            stamps[host].append(time.monotonic())

    t0 = time.monotonic()
    threads = [threading.Thread(target=hit, args=(h,)) for h in stamps]
    for th in threads:
        th.start()
    for th in threads:
        th.join()
    elapsed = time.monotonic() - t0
    # 3 hosts x 3 requests at 0.3 s: ~0.6 s if hosts run side by side, ~2.4 s if serialised.
    assert elapsed < 1.5, elapsed
    for host, ts in stamps.items():
        gaps = [b - a for a, b in zip(ts, ts[1:], strict=False)]
        assert all(g >= 0.29 for g in gaps), (host, gaps)


def _registry(tmp_path):
    (tmp_path / "companies.yaml").write_text(
        yaml.safe_dump(
            [
                {
                    "name": "Flow Traders",
                    "priority": 1,
                    "group": "prop_trading",
                    "ats": "greenhouse",
                    "config": {"board": "flowtraders"},
                    "careers_url": "https://x.test/",
                },
                {
                    "name": "Gunvor",
                    "priority": 1,
                    "group": "commodities",
                    "ats": "workday",
                    "config": {"tenant": "gunvor", "wd": "wd3", "site": "Gunvor_Careers"},
                    "careers_url": "https://x.test/",
                },
                {
                    "name": "Trading 212",
                    "priority": 1,
                    "group": "corporate",
                    "ats": "ashby",
                    "config": {"board": "trading212"},
                    "careers_url": "https://x.test/",
                },
                {
                    "name": "Vitol",
                    "priority": 1,
                    "group": "commodities",
                    "ats": "smartrecruiters",
                    "config": {"company": "Vitol"},
                    "careers_url": "https://x.test/",
                },
                {
                    "name": "Nowhere Bank",
                    "priority": 1,
                    "group": "bank",
                    "ats": "lever",
                    "config": {"company": "nowhere"},
                    "careers_url": "https://x.test/",
                },  # no fixture
            ]
        )
    )


def _run(tmp_path, workers, db):
    return runner.run(
        "all",
        db_path=db,
        companies_path=tmp_path / "companies.yaml",
        profile_path=runner.DEFAULT_PROFILE,
        docs_dir=tmp_path / "docs",
        dry_run=True,
        use_llm=False,
        now=datetime(2026, 10, 23, tzinfo=UTC),
        workers=workers,
    )


def test_parallel_run_matches_sequential_and_records_errors(tmp_path):
    _registry(tmp_path)
    seq = _run(tmp_path, 1, tmp_path / "seq.sqlite")
    par = _run(tmp_path, 4, tmp_path / "par.sqlite")
    assert (seq.sources_ok, seq.seen, seq.new) == (par.sources_ok, par.seen, par.new)
    assert seq.sources_ok == 4 and "nowhere-bank" in par.errors
    a = Store(tmp_path / "seq.sqlite")
    b = Store(tmp_path / "par.sqlite")
    assert {o.dedup_key for o in a.all_openings()} == {o.dedup_key for o in b.all_openings()}
    health = {h["company_slug"]: h for h in b.source_health()}
    assert health["nowhere-bank"]["consecutive_failures"] == 1
    assert health["vitol"]["last_count"] > 0
    a.close()
    b.close()
