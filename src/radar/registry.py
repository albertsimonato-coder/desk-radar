"""Load and validate companies.yaml."""

from __future__ import annotations

import re
from pathlib import Path

import yaml
from pydantic import ValidationError

from radar.models import Company

REQUIRED_CONFIG = {
    "greenhouse": ["board"],
    "lever": ["company"],
    "smartrecruiters": ["company"],
    "ashby": ["board"],
    "workday": ["tenant", "wd", "site"],
    "workable": ["account"],
    "sitemap": ["job_url_pattern"],
    "custom": ["kind"],
    "manual": [],
}


class RegistryError(ValueError):
    pass


def slugify(name: str) -> str:
    s = name.lower()
    s = s.replace("&", " and ")
    s = re.sub(r"[àáâä]", "a", s)
    s = re.sub(r"[èéêë]", "e", s)
    s = re.sub(r"[ìíîï]", "i", s)
    s = re.sub(r"[òóôö]", "o", s)
    s = re.sub(r"[ùúûü]", "u", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def load_registry(path: str | Path) -> list[Company]:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or []
    if not isinstance(raw, list):
        raise RegistryError("companies.yaml must be a list")
    companies: list[Company] = []
    seen: set[str] = set()
    for i, item in enumerate(raw):
        try:
            c = Company.model_validate(item)
        except ValidationError as e:
            raise RegistryError(f"companies.yaml entry #{i} ({item.get('name')}): {e}") from e
        if not c.slug:
            c.slug = slugify(c.name)
        if c.slug in seen:
            raise RegistryError(f"duplicate company slug: {c.slug}")
        seen.add(c.slug)
        missing = [k for k in REQUIRED_CONFIG[c.ats] if k not in c.config]
        if missing and c.active and c.ats != "manual":
            raise RegistryError(f"{c.name}: ats={c.ats} requires config keys {missing}")
        companies.append(c)
    return companies


def select_companies(
    companies: list[Company], tier: str = "all", today_is_monday: bool = False
) -> list[Company]:
    """tier: 'all' | 'daily'. Daily = priority 1, plus priority 2 on Mondays."""
    active = [c for c in companies if c.active and c.ats != "manual"]
    if tier == "all":
        return active
    if tier == "daily":
        return [c for c in active if c.priority == 1 or today_is_monday]
    raise ValueError(f"unknown tier {tier}")
