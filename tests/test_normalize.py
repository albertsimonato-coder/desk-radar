import pytest

from radar.normalize import dedup_key, normalize_location, normalize_title


@pytest.mark.parametrize(
    "raw,city,country",
    [
        ("London, GB", "London", "GB"),
        ("United Kingdom - London", "London", "GB"),
        ("Londra", "London", "GB"),
        ("London  United Kingdom", "London", "GB"),
        ("Milano, Italia", "Milan", "IT"),
        ("Milan", "Milan", "IT"),
        ("Luxembourg", "Luxembourg", "LU"),
        ("Zürich", "Zurich", "CH"),
        ("Genève, Suisse", "Geneva", "CH"),
        ("Paris - La Défense", "Paris", "FR"),
        ("Dublin, Ireland", "Dublin", "IE"),
        ("New York, NY", "New York", "US"),
        ("Frankfurt am Main, Germany", "Frankfurt", "DE"),
        ("Remote - EMEA", "Remote", ""),
        ("3 Locations", "", ""),
        ("United Kingdom", "", "GB"),
        ("", "", ""),
    ],
)
def test_city_alias_map(raw, city, country):
    assert normalize_location(raw) == (city, country)


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("Sales & Trading Analyst (m/f/d)", "sales & trading analyst"),
        ("Graduate Programme 2027 – Markets [JR123456]", "graduate programme markets"),
        ("Junior Risk Analyst - Req ID: R-0098765", "junior risk analyst"),
        ("FX Trader 12345678", "fx trader"),
        ("  Quant   Researcher  ", "quant researcher"),
        ("Summer Analyst 2027 - London", "summer analyst - london"),
    ],
)
def test_title_normalisation(raw, expected):
    assert normalize_title(raw) == expected


def test_dedup_key_stable_and_case_insensitive_city():
    a = dedup_key("ubs", "summer analyst", "London")
    b = dedup_key("ubs", "summer analyst", "london")
    assert a == b and len(a) == 40
    assert dedup_key("ubs", "summer analyst", "Zurich") != a
    assert dedup_key("citi", "summer analyst", "London") != a
