"""Orchestrates a run and exposes the CLI (`python -m radar run ...`)."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

from radar.adapters import SourceError, get_adapter
from radar.classify import RuleClassifier, llm_available, llm_classify
from radar.models import Company, Opening, RawPosting
from radar.normalize import dedup_key, normalize_location, normalize_title
from radar.profile import load_profile
from radar.registry import load_registry, select_companies
from radar.render import render_pages
from radar.score import Scorer
from radar.store import Store, now_utc

log = logging.getLogger("radar")

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_WORKERS = 8
DEFAULT_DB = ROOT / "data" / "radar.sqlite"
DEFAULT_COMPANIES = ROOT / "companies.yaml"
DEFAULT_PROFILE = ROOT / "profile.yaml"
DEFAULT_DOCS = ROOT / "docs"
FIXTURES = ROOT / "tests" / "fixtures"


class RunResult:
    def __init__(self) -> None:
        self.run_id = 0
        self.sources_total = 0
        self.sources_ok = 0
        self.seen = 0
        self.new = 0
        self.closed = 0
        self.reopened = 0
        self.errors: dict[str, str] = {}


def build_opening(
    company: Company,
    raw: RawPosting,
    classifier: RuleClassifier,
    now: datetime,
    run_id: int,
) -> Opening:
    title_norm = normalize_title(raw.title)
    city, country = normalize_location(raw.location_raw)
    key = dedup_key(company.slug, title_norm, city)
    et, fn = classifier.classify(
        raw.title, raw.department, raw.description_snippet, raw.employment_type_raw
    )
    return Opening(
        dedup_key=key,
        company_slug=company.slug,
        company_name=company.name,
        group=company.group,
        priority=company.priority,
        external_id=raw.external_id,
        title=raw.title.strip(),
        title_norm=title_norm,
        location_raw=raw.location_raw,
        city=city,
        country=country,
        department=raw.department,
        posted_at=raw.posted_at,
        url=raw.url or str(company.careers_url),
        description_snippet=raw.description_snippet,
        employment_type_raw=raw.employment_type_raw,
        employment_type=et,  # type: ignore[arg-type]
        function=fn,  # type: ignore[arg-type]
        first_seen=now,
        last_seen=now,
        status="open",
        first_run_id=run_id,
    )


def merge_into_store(
    store: Store,
    company: Company,
    postings: list[RawPosting],
    classifier: RuleClassifier,
    now: datetime,
    run_id: int,
    result: RunResult,
) -> set[str]:
    """Apply one source's postings: insert new, refresh existing, reopen closed.

    Returns the dedup keys seen in this scan."""
    seen: set[str] = set()
    for raw in postings:
        if not raw.title:
            continue
        fresh = build_opening(company, raw, classifier, now, run_id)
        if fresh.dedup_key in seen:
            continue  # same title+city listed twice (multiple reqs) -> one row
        seen.add(fresh.dedup_key)
        existing = store.get(fresh.dedup_key)
        if existing is None:
            store.upsert(fresh)
            result.new += 1
            continue
        existing.last_seen = now
        existing.missing_runs = 0
        existing.title = fresh.title
        existing.location_raw = fresh.location_raw
        existing.department = fresh.department or existing.department
        existing.url = fresh.url
        existing.external_id = fresh.external_id
        existing.priority = company.priority
        existing.group = company.group
        existing.company_name = company.name
        if fresh.posted_at and not existing.posted_at:
            existing.posted_at = fresh.posted_at
        if fresh.description_snippet:
            existing.description_snippet = fresh.description_snippet
        if existing.classified_by == "rules":
            existing.employment_type = fresh.employment_type
            existing.function = fresh.function
        if existing.status == "closed":
            existing.status = "open"
            existing.reopened += 1
            result.reopened += 1
        store.upsert(existing)
    result.seen += len(seen)
    return seen


def load_fixture(company: Company) -> object:
    for cand in (
        FIXTURES / f"{company.ats}_{company.slug}.json",
        FIXTURES / f"{company.slug}.json",
        FIXTURES / f"{company.ats}.json",
    ):
        if cand.exists():
            return json.loads(cand.read_text(encoding="utf-8"))
    raise SourceError(f"no fixture for {company.slug} ({company.ats})", company=company.name)


def run(
    tier: str = "daily",
    *,
    db_path: str | Path = DEFAULT_DB,
    companies_path: str | Path = DEFAULT_COMPANIES,
    profile_path: str | Path = DEFAULT_PROFILE,
    docs_dir: str | Path = DEFAULT_DOCS,
    dry_run: bool = False,
    only: list[str] | None = None,
    use_llm: bool = True,
    render: bool = True,
    now: datetime | None = None,
    workers: int = DEFAULT_WORKERS,
) -> RunResult:
    now = now or now_utc()
    profile = load_profile(profile_path)
    companies = load_registry(companies_path)
    selected = select_companies(companies, tier=tier, today_is_monday=now.weekday() == 0)
    if only:
        wanted = {s.strip() for s in only}
        selected = [c for c in selected if c.slug in wanted or c.name in wanted]
    classifier = RuleClassifier(profile)
    scorer = Scorer(profile)
    store = Store(db_path)
    result = RunResult()
    result.run_id = store.start_run(tier, dry_run=dry_run)
    result.sources_total = len(selected)
    log.info(
        "run #%d tier=%s companies=%d workers=%d dry_run=%s",
        result.run_id,
        tier,
        len(selected),
        workers,
        dry_run,
    )

    def known_for(company: Company) -> dict[str, RawPosting]:
        return {
            o.url: RawPosting(
                external_id=o.external_id,
                title=o.title,
                location_raw=o.location_raw,
                department=o.department,
                posted_at=o.posted_at,
                url=o.url,
                description_snippet=o.description_snippet,
                employment_type_raw=o.employment_type_raw,
            )
            for o in store.openings_for_company(company.slug)
        }

    def fetch_one(company: Company, known: dict[str, RawPosting]) -> list[RawPosting]:
        """Runs in a worker thread: network only, no database access."""
        adapter = get_adapter(company)
        adapter.known_postings = known
        if dry_run:
            return adapter.parse(load_fixture(company))
        return adapter.fetch()

    def apply(company: Company, outcome: list[RawPosting] | BaseException) -> None:
        """Runs on the main thread: all SQLite writes happen here, one source at a time."""
        if isinstance(outcome, SourceError):
            log.warning("%s: %s", company.name, outcome)
            store.record_source_error(
                company.slug, company.name, company.ats, result.run_id, str(outcome)
            )
            result.errors[company.slug] = str(outcome)
            return
        if isinstance(outcome, BaseException):  # any adapter bug must not abort the run
            log.error("%s: unexpected error: %s", company.name, outcome, exc_info=outcome)
            msg = f"{type(outcome).__name__}: {outcome}"
            store.record_source_error(company.slug, company.name, company.ats, result.run_id, msg)
            result.errors[company.slug] = msg
            return
        seen = merge_into_store(store, company, outcome, classifier, now, result.run_id, result)
        result.closed += store.mark_missing(company.slug, seen, result.run_id)
        store.commit()
        store.record_source_success(
            company.slug, company.name, company.ats, result.run_id, len(seen)
        )
        result.sources_ok += 1
        log.info("%s: %d postings (%s)", company.name, len(seen), company.ats)

    # Sitemap-style sources need to know what is already stored before they fetch; read that on
    # the main thread, then fan the network work out to `workers` threads (one employer each,
    # still one request per second per host) and apply results here as they complete.
    known_by_slug = {c.slug: (known_for(c) if c.ats == "sitemap" else {}) for c in selected}
    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        futures = {pool.submit(fetch_one, c, known_by_slug[c.slug]): c for c in selected}
        for fut in as_completed(futures):
            company = futures[fut]
            try:
                apply(company, fut.result())
            except BaseException as e:  # noqa: BLE001
                apply(company, e)

    # Optional LLM pass for rows still classified other/other.
    all_openings = store.all_openings()
    if use_llm and not dry_run and llm_available():
        n = llm_classify([o for o in all_openings if o.status == "open"], store)
        log.info("LLM classified %d openings", n)

    # Re-score everything (recency decays, profile may have changed).
    for o in all_openings:
        o.score_breakdown = scorer.score(o, now=now)
        o.fit_score = o.score_breakdown.total
        store.upsert(o)
    store.commit()

    store.finish_run(
        result.run_id,
        sources_total=result.sources_total,
        sources_ok=result.sources_ok,
        openings_seen=result.seen,
        openings_new=result.new,
    )
    if render:
        render_pages(store, profile, docs_dir)
    store.close()
    log.info(
        "done: %d/%d sources ok, %d seen, %d new, %d closed, %d reopened",
        result.sources_ok,
        result.sources_total,
        result.seen,
        result.new,
        result.closed,
        result.reopened,
    )
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="radar", description="Desk Radar Scanner")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("run", help="scan sources, update the database and render the pages")
    p.add_argument("--tier", choices=["daily", "all"], default="daily")
    p.add_argument("--all", action="store_true", help="shortcut for --tier all")
    p.add_argument(
        "--dry-run", action="store_true", help="use recorded fixtures instead of live sites"
    )
    p.add_argument("--only", help="comma-separated company slugs/names to scan")
    p.add_argument("--db", default=str(DEFAULT_DB))
    p.add_argument("--companies", default=str(DEFAULT_COMPANIES))
    p.add_argument("--profile", default=str(DEFAULT_PROFILE))
    p.add_argument("--docs", default=str(DEFAULT_DOCS))
    p.add_argument(
        "--workers",
        type=int,
        default=DEFAULT_WORKERS,
        help="employers fetched concurrently (1 = sequential)",
    )
    p.add_argument("--no-llm", action="store_true")
    p.add_argument("--no-render", action="store_true")
    p.add_argument("-v", "--verbose", action="store_true")
    r = sub.add_parser("render", help="re-render the pages from the database without scanning")
    r.add_argument("--db", default=str(DEFAULT_DB))
    r.add_argument("--profile", default=str(DEFAULT_PROFILE))
    r.add_argument("--docs", default=str(DEFAULT_DOCS))
    c = sub.add_parser("check", help="validate companies.yaml and profile.yaml")
    c.add_argument("--companies", default=str(DEFAULT_COMPANIES))
    c.add_argument("--profile", default=str(DEFAULT_PROFILE))
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if getattr(args, "verbose", False) else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        stream=sys.stderr,
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)

    if args.cmd == "run":
        res = run(
            "all" if args.all else args.tier,
            db_path=args.db,
            companies_path=args.companies,
            profile_path=args.profile,
            docs_dir=args.docs,
            dry_run=args.dry_run,
            only=args.only.split(",") if args.only else None,
            use_llm=not args.no_llm,
            render=not args.no_render,
            workers=args.workers,
        )
        for slug, err in res.errors.items():
            print(f"SOURCE ERROR {slug}: {err}", file=sys.stderr)
        return 0
    if args.cmd == "render":
        store = Store(args.db)
        render_pages(store, load_profile(args.profile), args.docs)
        store.close()
        return 0
    if args.cmd == "check":
        companies = load_registry(args.companies)
        load_profile(args.profile)
        active = [c for c in companies if c.active and c.ats != "manual"]
        print(f"{len(companies)} companies, {len(active)} active with an adapter")
        return 0
    return 1
