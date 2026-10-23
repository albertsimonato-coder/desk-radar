import json
from pathlib import Path

import pytest

from radar.models import Company

FIXTURES = Path(__file__).parent / "fixtures"


def load_fixture(name: str):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


@pytest.fixture
def gh_company() -> Company:
    return Company(
        name="Flow Traders",
        priority=1,
        group="prop_trading",
        ats="greenhouse",
        config={"board": "flowtraders"},
        careers_url="https://www.flowtraders.com/careers",
    )


@pytest.fixture
def wd_company() -> Company:
    return Company(
        name="Gunvor",
        priority=1,
        group="commodities",
        ats="workday",
        config={"tenant": "gunvor", "wd": "wd3", "site": "Gunvor_Careers"},
        careers_url="https://centalion.com/careers/",
    )


@pytest.fixture
def unscoped_profile(tmp_path) -> Path:
    """profile.yaml with the scope filter switched off: the recorded fixtures are worldwide."""
    import yaml

    from radar.runner import DEFAULT_PROFILE

    data = yaml.safe_load(DEFAULT_PROFILE.read_text(encoding="utf-8"))
    data["scope"] = {"enabled": False}
    out = tmp_path / "profile.yaml"
    out.write_text(yaml.safe_dump(data, allow_unicode=True))
    return out
