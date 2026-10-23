"""Core data models."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl, field_validator

ATS = Literal[
    "greenhouse",
    "lever",
    "smartrecruiters",
    "ashby",
    "workday",
    "workable",
    "sitemap",
    "custom",
    "manual",
]
Group = Literal[
    "bank",
    "boutique",
    "asset_manager",
    "commodities",
    "exchange",
    "prop_trading",
    "advisory",
    "corporate",
]
EmploymentType = Literal[
    "graduate", "internship", "offcycle", "analyst_junior", "experienced", "other"
]
Function = Literal[
    "sales_trading",
    "commodities",
    "market_making",
    "quant",
    "market_risk",
    "treasury",
    "ibd",
    "advisory_valuation",
    "asset_management",
    "operations",
    "technology",
    "other",
]


class Company(BaseModel):
    """One row of companies.yaml."""

    name: str
    slug: str = ""
    priority: int = Field(ge=1, le=2)
    group: Group
    ats: ATS
    config: dict = Field(default_factory=dict)
    careers_url: HttpUrl
    active: bool = True
    notes: str = ""

    @field_validator("slug", mode="before")
    @classmethod
    def _empty_slug_ok(cls, v: str | None) -> str:
        return v or ""


class RawPosting(BaseModel):
    """What an adapter returns: one posting as seen on the source, un-normalised."""

    external_id: str
    title: str
    location_raw: str = ""
    department: str = ""
    posted_at: datetime | None = None
    url: str
    description_snippet: str = ""
    employment_type_raw: str = ""


class ScoreBreakdown(BaseModel):
    city: float = 0
    employment_type: float = 0
    function: float = 0
    keywords: float = 0
    recency: float = 0
    keyword_hits: list[str] = Field(default_factory=list)
    total: float = 0


class Opening(BaseModel):
    """A stored opening (one row of the `openings` table)."""

    dedup_key: str
    company_slug: str
    company_name: str
    group: str
    priority: int
    external_id: str
    title: str
    title_norm: str
    location_raw: str
    city: str
    country: str
    department: str = ""
    posted_at: datetime | None = None
    url: str
    description_snippet: str = ""
    employment_type_raw: str = ""
    employment_type: EmploymentType = "other"
    function: Function = "other"
    classified_by: str = "rules"
    fit_score: float = 0
    score_breakdown: ScoreBreakdown = Field(default_factory=ScoreBreakdown)
    first_seen: datetime
    last_seen: datetime
    status: Literal["open", "closed"] = "open"
    first_run_id: int
    missing_runs: int = 0
    reopened: int = 0  # times it came back from closed; reopened openings are never 'new'
