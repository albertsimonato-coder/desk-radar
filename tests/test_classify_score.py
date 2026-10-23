from datetime import UTC, datetime

from radar.classify import RuleClassifier
from radar.models import Opening
from radar.profile import load_profile
from radar.runner import DEFAULT_PROFILE
from radar.score import Scorer


def _opening(**kw) -> Opening:
    now = datetime(2026, 10, 23, tzinfo=UTC)
    base = dict(
        dedup_key="k",
        company_slug="x",
        company_name="X",
        group="bank",
        priority=1,
        external_id="1",
        title="t",
        title_norm="t",
        location_raw="",
        city="",
        country="",
        url="https://x",
        first_seen=now,
        last_seen=now,
        first_run_id=1,
    )
    base.update(kw)
    return Opening(**base)


def test_rule_classifier_examples():
    c = RuleClassifier(load_profile(DEFAULT_PROFILE))
    assert c.classify("Summer Analyst 2027 - Global Markets", "", "") == (
        "internship",
        "sales_trading",
    )
    assert c.classify("Graduate Programme - Oil Trading", "", "") == ("graduate", "commodities")
    assert c.classify("Senior Software Engineer", "", "") == ("experienced", "technology")
    assert c.classify("Junior Market Risk Analyst", "", "") == ("analyst_junior", "market_risk")
    assert c.classify("Off-cycle Intern - Commodities Trading", "", "") == (
        "internship",
        "commodities",
    )
    assert c.classify("Vice President, Treasury ALM", "", "") == ("experienced", "treasury")
    assert c.classify("Senior Analyst - Finance Operations", "", "")[0] == "experienced"
    assert c.classify("Something Unusual", "", "") == ("other", "other")
    # department / snippet fallbacks
    assert c.classify("Associate", "Investment Banking", "")[1] == "ibd"
    assert c.classify("Trainee", "", "")[0] == "graduate"


def test_score_prefers_target_city_type_function():
    s = Scorer(load_profile(DEFAULT_PROFILE))
    now = datetime(2026, 10, 23, tzinfo=UTC)
    good = _opening(
        title="Graduate Programme 2027 - Commodities Trading",
        city="London",
        country="GB",
        employment_type="graduate",
        function="commodities",
        posted_at=now,
    )
    bad = _opening(
        title="Senior Software Engineer",
        city="Pune",
        country="IN",
        employment_type="experienced",
        function="technology",
        posted_at=now,
    )
    bg, bb = s.score(good, now), s.score(bad, now)
    assert bg.total > 85
    assert bb.total < 25
    assert "2027" in bg.keyword_hits
    assert bg.city == 30 and bb.city < 10


def test_score_recency_decays():
    s = Scorer(load_profile(DEFAULT_PROFILE))
    now = datetime(2026, 10, 23, tzinfo=UTC)
    fresh = _opening(posted_at=now)
    old = _opening(posted_at=datetime(2026, 1, 1, tzinfo=UTC))
    assert s.score(fresh, now).recency > s.score(old, now).recency


def test_title_only_words_do_not_leak_from_snippet():
    c = RuleClassifier(load_profile(DEFAULT_PROFILE))
    et, fn = c.classify(
        "Commodities Broker Trader", "Trading", "an early stage initiative, take the lead"
    )
    assert et == "other" and fn == "commodities"
    assert c.classify("Software Engineer - Global Markets", "", "")[1] == "technology"
    assert c.classify("Trading Desk Operations Engineer", "", "")[1] == "technology"
    assert c.classify("Sales and Trading", "Sales & Trading", "", "Summer Internship") == (
        "internship",
        "sales_trading",
    )
