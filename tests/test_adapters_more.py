from radar.adapters.ashby import AshbyAdapter
from radar.adapters.custom import CustomAdapter
from radar.adapters.jsonld import parse_fallback, parse_job_page
from radar.adapters.lever import LeverAdapter
from radar.adapters.sitemap import SitemapAdapter
from radar.adapters.smartrecruiters import SmartRecruitersAdapter
from radar.adapters.workable import WorkableAdapter
from radar.models import Company, RawPosting
from tests.conftest import FIXTURES, load_fixture


def _co(ats, config, name="X"):
    return Company(
        name=name,
        priority=1,
        group="prop_trading",
        ats=ats,
        config=config,
        careers_url="https://example.com/careers",
    )


def test_lever_parse():
    ps = LeverAdapter(_co("lever", {"company": "palantir"})).parse(
        load_fixture("lever_palantir.json")
    )
    assert len(ps) == 10
    p = ps[0]
    assert p.url.startswith("https://jobs.lever.co/palantir/")
    assert p.title and p.location_raw and p.posted_at is not None
    assert p.employment_type_raw  # commitment


def test_smartrecruiters_parse_and_url():
    pages = load_fixture("smartrecruiters_vitol.json")
    ps = SmartRecruitersAdapter(_co("smartrecruiters", {"company": "Vitol"})).parse(pages)
    assert len(ps) == pages[0]["totalFound"] == 35
    p = ps[0]
    assert p.url == f"https://jobs.smartrecruiters.com/Vitol/{p.external_id}"
    assert p.location_raw and p.posted_at is not None
    assert any(x.location_raw.startswith("Geneva") for x in ps)


def test_ashby_parse():
    ps = AshbyAdapter(_co("ashby", {"board": "trading212"})).parse(
        load_fixture("ashby_trading-212.json")
    )
    assert len(ps) == 10
    p = ps[0]
    assert p.url.startswith("https://jobs.ashbyhq.com/trading212/")
    assert p.title and p.location_raw and p.posted_at is not None
    assert all("<" not in x.description_snippet for x in ps)


def test_workable_parse():
    ps = WorkableAdapter(_co("workable", {"account": "onyx-capital-group"})).parse(
        load_fixture("workable_onyx-capital-group.json")
    )
    assert len(ps) == 7
    titles = {p.title for p in ps}
    assert "Graduate Trader" in titles
    assert all(p.url.startswith("https://apply.workable.com/") for p in ps)
    assert next(p for p in ps if p.title == "Graduate Trader").location_raw.startswith("London")


def test_custom_glencore_parse():
    ps = CustomAdapter(_co("custom", {"kind": "glencore"})).parse(
        load_fixture("custom_glencore.json")
    )
    assert len(ps) == 8
    p = ps[0]
    assert p.url == f"https://www.glencore.com/en/careers/jobs/{p.external_id}"
    assert p.location_raw and p.title


def test_sitemap_jsonld_pages_and_known_urls_not_refetched():
    fx = load_fixture("sitemap_societe-generale.json")
    adapter = SitemapAdapter(
        _co("sitemap", {"job_url_pattern": r"/en/job-offers/", "sitemap_url": "x"}, name="SG")
    )
    ps = adapter.parse(fx)
    assert len(ps) == 3
    sa = next(p for p in ps if "summer-associate" in p.url)
    assert sa.title.startswith("2027 Masters of Financial Engineering")
    assert sa.employment_type_raw == "Internship"
    assert sa.posted_at is not None and sa.location_raw
    # A known URL is returned from memory even when its page is missing from the payload.
    known = RawPosting(external_id="k", title="Known Role", url=fx["urls"][0], location_raw="Paris")
    adapter.known_postings = {fx["urls"][0]: known}
    fx2 = {
        "urls": fx["urls"],
        "pages": {u: h for u, h in fx["pages"].items() if u != fx["urls"][0]},
    }
    ps2 = adapter.parse(fx2)
    assert any(p.title == "Known Role" for p in ps2) and len(ps2) == 3


def test_sitemap_fallback_successfactors_page():
    html = (FIXTURES / "sitemap_nomura_page.html").read_text()
    p = parse_fallback(html, "https://careers.nomura.com/Nomura/job/x/1/")
    assert p.title == "GM-Global Markets"
    assert p.location_raw == "Mumbai"
    assert parse_job_page(html, "u") is not None  # falls through to the fallback


def test_sitemap_index_page_harvest(monkeypatch):
    import httpx

    from radar.adapters.base import Http

    listing = (
        '<a href="/careers/career-opportunities/abc123-trader">T</a><a href="/careers/x">no</a>'
    )
    job = (
        "<html><head><title>Junior Trader - Marex Careers</title>"
        '<meta name="description" content="Join Marex as a Junior Trader in London, GB. '
        'Trading position available.">'
        "</head></html>"
    )

    def handler(req):
        if req.url.path.endswith("/career-opportunities"):
            return httpx.Response(200, text=listing)
        return httpx.Response(200, text=job)

    http = Http()
    http.client = httpx.Client(transport=httpx.MockTransport(handler))
    adapter = SitemapAdapter(
        _co(
            "sitemap",
            {
                "sitemap_url": "none",
                "index_urls": ["https://www.marex.com/careers/career-opportunities"],
                "job_url_pattern": r"career-opportunities/[a-z0-9]+-",
                "title_strip": r" - Marex Careers$",
                "location_regex": r"\bin ([^.]+?)\. ",
            },
            name="Marex",
        ),
        http=http,
    )
    ps = adapter.fetch()
    assert len(ps) == 1
    assert ps[0].title == "Junior Trader" and ps[0].location_raw == "London, GB"
    assert ps[0].url == "https://www.marex.com/careers/career-opportunities/abc123-trader"


def test_rss_feed_items_become_postings():
    fx = load_fixture("sitemap_intesa-sanpaolo.json")
    adapter = SitemapAdapter(
        _co(
            "sitemap",
            {"rss_url": "x", "job_url_pattern": r"jobs\.intesasanpaolo\.com/job/"},
            name="ISP",
        )
    )
    ps = adapter.parse(fx)
    assert len(ps) == 12
    p = ps[0]
    assert p.url.startswith("https://jobs.intesasanpaolo.com/job/")
    assert p.location_raw and "(" not in p.title  # "(City, CC)" moved from title to location
    assert p.description_snippet and "<" not in p.description_snippet


def test_custom_intervieweb_parse():
    ps = CustomAdapter(_co("custom", {"kind": "intervieweb", "page_url": "x"})).parse(
        load_fixture("custom_mediobanca.json")
    )
    assert len(ps) == 6
    p = ps[0]
    assert p.url.startswith("https://mediobanca.intervieweb.it/jobs/")
    assert p.location_raw.startswith("Milano") and p.posted_at is not None
    assert p.department


def test_sitemap_paginated_index_stops_when_nothing_new():
    import httpx

    from radar.adapters.base import Http

    pages = {
        0: '<a href="/JobDetail/1">a</a><a href="/JobDetail/2">b</a>',
        2: '<a href="/JobDetail/3">c</a>',
        4: '<a href="/JobDetail/3">c again</a>',  # nothing new -> stop
        6: '<a href="/JobDetail/99">never reached</a>',
    }
    seen = []

    def handler(req):
        if "offset=" in str(req.url):
            off = int(str(req.url).split("offset=")[1])
            seen.append(off)
            return httpx.Response(200, text=pages.get(off, ""))
        return httpx.Response(200, text="<title>Job</title>")

    http = Http()
    http.client = httpx.Client(transport=httpx.MockTransport(handler))
    adapter = SitemapAdapter(
        _co(
            "sitemap",
            {
                "sitemap_url": "none",
                "index_url_pattern": "https://x.test/list?offset={offset}",
                "index_step": 2,
                "job_url_pattern": r"/JobDetail/\d+",
            },
        ),
        http=http,
    )
    urls = adapter.job_urls()
    assert urls == {
        "https://x.test/JobDetail/1",
        "https://x.test/JobDetail/2",
        "https://x.test/JobDetail/3",
    }
    assert seen == [0, 2, 4]


def test_sitemap_location_regex_fills_missing_jsonld_location():
    html = (
        '<html><head><script type="application/ld+json">{"@type":"JobPosting","title":"Analyst",'
        '"datePosted":"2026-10-01"}</script></head><body><script>var loc = {city: "Milan", '
        'country: "Italy"};</script></body></html>'
    )
    adapter = SitemapAdapter(
        _co(
            "sitemap",
            {
                "job_url_pattern": "x",
                "sitemap_url": "none",
                "location_regex": r'city:\s*"([^"]*)"[^}]*?country:\s*"([^"]*)"',
            },
        )
    )
    p = adapter._parse_page(html, "https://x.test/j/1")
    assert p.title == "Analyst" and p.location_raw == "Milan, Italy"


def test_sitemap_index_item_regex_attaches_listing_metadata():
    import httpx

    from radar.adapters.base import Http

    listing = (
        '<h3><a href="https://x.test/JobDetail/Payroll-Expert/1"> Payroll Expert </a></h3>'
        '<div><span class="job-info-icon job-info-icon_world"> Bulgaria </span>'
        '<span class="job-info-icon job-info-icon_function"> People &amp; Culture </span>'
        '<span class="job-info-icon job-info-icon_work"> Full-time </span></div>'
        '<h3><a href="https://x.test/JobDetail/Trader/2"> Trader </a></h3>'
        '<div><span class="job-info-icon job-info-icon_world"> Italy </span></div>'
    )
    job = '<script type="application/ld+json">{"@type":"JobPosting","title":"T"}</script>'

    def handler(req):
        return httpx.Response(200, text=listing if "list" in str(req.url) else job)

    http = Http()
    http.client = httpx.Client(transport=httpx.MockTransport(handler))
    adapter = SitemapAdapter(
        _co(
            "sitemap",
            {
                "sitemap_url": "none",
                "index_urls": ["https://x.test/list"],
                "job_url_pattern": r"/JobDetail/",
                "index_item_regex": (
                    r'href="(?P<url>https://x\.test/JobDetail/[^"]+)">[^<]*</a>'
                    r'.*?job-info-icon_world"> ?(?P<location>[^<]*?) ?</span>'
                    r'(?:.*?job-info-icon_function"> ?(?P<department>[^<]*?) ?</span>)?'
                ),
            },
        ),
        http=http,
    )
    ps = {p.url: p for p in adapter.fetch()}
    assert ps["https://x.test/JobDetail/Payroll-Expert/1"].location_raw == "Bulgaria"
    assert ps["https://x.test/JobDetail/Payroll-Expert/1"].department == "People & Culture"
    assert ps["https://x.test/JobDetail/Trader/2"].location_raw == "Italy"


def test_sitemap_index_item_split_keeps_fields_within_one_entry():
    import httpx

    from radar.adapters.base import Http

    # First entry has no metadata at all; without the split its regex would swallow the
    # second entry's country.
    listing = (
        '<h3 class="t"><a href="https://x.test/JobDetail/A/1"> A </a></h3>'
        '<h3 class="t"><a href="https://x.test/JobDetail/B/2"> B </a></h3>'
        '<span class="job-info-icon_world"> Italy </span>'
    )

    def handler(req):
        return httpx.Response(200, text=listing if "list" in str(req.url) else "<title>J</title>")

    http = Http()
    http.client = httpx.Client(transport=httpx.MockTransport(handler))
    adapter = SitemapAdapter(
        _co(
            "sitemap",
            {
                "sitemap_url": "none",
                "index_urls": ["https://x.test/list"],
                "job_url_pattern": r"/JobDetail/",
                "index_item_split": r'<h3 class="t"',
                "index_item_regex": (
                    r'href="(?P<url>https://x\.test/JobDetail/[^"]+)">'
                    r'(?:.*?job-info-icon_world"> ?(?P<location>[^<]*?) ?</span>)?'
                ),
            },
        ),
        http=http,
    )
    ps = {p.url: p for p in adapter.fetch()}
    assert ps["https://x.test/JobDetail/A/1"].location_raw == ""
    assert ps["https://x.test/JobDetail/B/2"].location_raw == "Italy"


def test_sitemap_fetch_pages_false_builds_postings_from_listing_only():
    import httpx

    from radar.adapters.base import Http

    listing = (
        '<article class="r"><h3><a href="https://x.test/JobDetail?jobId=1"> Trader </a></h3>'
        '<p class="icon">ID</p> <p> 1 </p> <img alt="Office Location:"> <p> London Office </p>'
        '<img alt="Posted Date:"> <p> 23 Oct 2026 </p> <img alt="Job Category:"> <p> Equities </p>'
        "</article>"
        '<article class="r"><h3><a href="https://x.test/JobDetail?jobId=2"> Analyst </a></h3>'
        "</article>"
    )
    calls = []

    def handler(req):
        calls.append(str(req.url))
        return httpx.Response(200, text=listing if "offset=0" in str(req.url) else "")

    http = Http()
    http.client = httpx.Client(transport=httpx.MockTransport(handler))
    adapter = SitemapAdapter(
        _co(
            "sitemap",
            {
                "sitemap_url": "none",
                "index_url_pattern": "https://x.test/list?offset={offset}",
                "index_step": 9,
                "index_item_split": r'<article class="r"',
                "index_item_regex": (
                    r'href="(?P<url>https://x\.test/JobDetail\?jobId=\d+)">'
                    r" ?(?P<title>[^<]+?) ?</a>"
                    r'(?:.*?alt="Office Location:"> <p> ?(?P<location>[^<]*?) ?</p>)?'
                    r'(?:.*?alt="Posted Date:"> <p> ?(?P<posted>[^<]*?) ?</p>)?'
                    r'(?:.*?alt="Job Category:"> <p> ?(?P<department>[^<]*?) ?</p>)?'
                ),
                "fetch_pages": False,
                "job_url_pattern": r"JobDetail",
            },
        ),
        http=http,
    )
    ps = {p.url: p for p in adapter.fetch()}
    assert set(ps) == {"https://x.test/JobDetail?jobId=1", "https://x.test/JobDetail?jobId=2"}
    t = ps["https://x.test/JobDetail?jobId=1"]
    assert t.title == "Trader" and t.location_raw == "London Office" and t.department == "Equities"
    assert t.posted_at is not None and t.posted_at.day == 23
    assert ps["https://x.test/JobDetail?jobId=2"].title == "Analyst"
    assert not any("JobDetail" in c for c in calls)  # job pages never opened
