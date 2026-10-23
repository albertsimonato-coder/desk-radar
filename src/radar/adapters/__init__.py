"""ATS adapters. Each exposes a class with fetch() -> list[RawPosting]."""

from __future__ import annotations

from radar.adapters.base import Adapter, SourceError
from radar.models import Company


def get_adapter(company: Company) -> Adapter:
    ats = company.ats
    if ats == "greenhouse":
        from radar.adapters.greenhouse import GreenhouseAdapter

        return GreenhouseAdapter(company)
    if ats == "workday":
        from radar.adapters.workday import WorkdayAdapter

        return WorkdayAdapter(company)
    if ats == "lever":
        from radar.adapters.lever import LeverAdapter

        return LeverAdapter(company)
    if ats == "smartrecruiters":
        from radar.adapters.smartrecruiters import SmartRecruitersAdapter

        return SmartRecruitersAdapter(company)
    if ats == "ashby":
        from radar.adapters.ashby import AshbyAdapter

        return AshbyAdapter(company)
    if ats == "workable":
        from radar.adapters.workable import WorkableAdapter

        return WorkableAdapter(company)
    if ats == "custom":
        from radar.adapters.custom import CustomAdapter

        return CustomAdapter(company)
    if ats == "sitemap":
        from radar.adapters.sitemap import SitemapAdapter

        return SitemapAdapter(company)
    raise SourceError(f"no adapter for ats={ats}")


__all__ = ["Adapter", "SourceError", "get_adapter"]
