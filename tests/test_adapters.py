from datetime import UTC, datetime

import httpx
import pytest

from radar.adapters.base import Http, SourceError
from radar.adapters.greenhouse import GreenhouseAdapter
from radar.adapters.workday import WorkdayAdapter, parse_posted_on
from radar.registry import slugify
from tests.conftest import load_fixture


def test_greenhouse_parse(gh_company):
    gh_company.slug = slugify(gh_company.name)
    postings = GreenhouseAdapter(gh_company).parse(load_fixture("greenhouse_flow-traders.json"))
    assert len(postings) == 12
    p = postings[0]
    assert p.external_id.isdigit()
    assert p.title
    assert p.url.startswith("https://") and "greenhouse" in p.url or "flowtraders" in p.url
    assert p.location_raw
    assert p.posted_at is None or p.posted_at.tzinfo is not None
    assert all(len(x.description_snippet) <= 400 for x in postings)


def test_greenhouse_rejects_bad_payload(gh_company):
    with pytest.raises(SourceError):
        GreenhouseAdapter(gh_company).parse({"nope": []})


def test_workday_parse_two_pages_and_urls(wd_company):
    pages = load_fixture("workday_gunvor.json")
    assert len(pages) == 2
    postings = WorkdayAdapter(wd_company).parse(pages)
    assert len(postings) == pages[0]["total"] == 35
    p = postings[0]
    assert p.url.startswith("https://gunvor.wd3.myworkdayjobs.com/en-US/Gunvor_Careers/job/")
    assert p.external_id == "JR102824"
    assert p.location_raw == "Houston"
    assert all(x.external_id for x in postings)
    assert len({x.external_id for x in postings}) == len(postings)


def test_workday_pagination_hits_api_until_total(wd_company):
    pages = load_fixture("workday_gunvor.json")
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        body = request.read()
        calls.append(body)
        import json

        offset = json.loads(body)["offset"]
        assert request.headers["accept"] == "application/json"
        return httpx.Response(200, json=pages[offset // 20])

    http = Http()
    http.client = httpx.Client(transport=httpx.MockTransport(handler))
    adapter = WorkdayAdapter(wd_company, http=http)
    postings = adapter.fetch()
    assert len(calls) == 2
    assert len(postings) == 35


def test_workday_posted_on_relative_dates():
    now = datetime(2026, 10, 23, 15, 0, tzinfo=UTC)
    assert parse_posted_on("Posted Today", now) == datetime(2026, 10, 23, tzinfo=UTC)
    assert parse_posted_on("Posted Yesterday", now) == datetime(2026, 10, 22, tzinfo=UTC)
    assert parse_posted_on("Posted 7 Days Ago", now) == datetime(2026, 10, 16, tzinfo=UTC)
    assert parse_posted_on("Posted 30+ Days Ago", now) == datetime(2026, 9, 23, tzinfo=UTC)
    assert parse_posted_on("", now) is None


def test_http_retries_on_5xx_then_raises(monkeypatch):
    import radar.adapters.base as base

    monkeypatch.setattr(base.time, "sleep", lambda s: None)
    n = {"calls": 0}

    def handler(request):
        n["calls"] += 1
        return httpx.Response(503)

    http = Http()
    http.client = httpx.Client(transport=httpx.MockTransport(handler))
    with pytest.raises(SourceError):
        http.get_json("https://example.test/x")
    assert n["calls"] == base.MAX_RETRIES + 1


def test_workday_multi_location_falls_back_to_path():
    from radar.adapters.workday import resolve_location

    assert resolve_location("London", "/job/London/Trader_R1") == "London"
    assert (
        resolve_location("2 Locations", "/job/London--United-Kingdom/Trader_R1")
        == "London, United Kingdom (2 Locations)"
    )
    assert resolve_location("", "/job/Zurich/Trader_R1") == "Zurich"


def test_greenhouse_snippet_is_plain_text(gh_company):
    postings = GreenhouseAdapter(gh_company).parse(load_fixture("greenhouse_flow-traders.json"))
    assert all(
        "<" not in p.description_snippet and "&lt;" not in p.description_snippet for p in postings
    )
