"""SmartRecruiters public postings API.

GET https://api.smartrecruiters.com/v1/companies/{company}/postings?limit=100&offset=N
Paginates until totalFound. Config: company
"""

from __future__ import annotations

from typing import Any

from radar.adapters.base import Adapter, SourceError, parse_dt
from radar.models import RawPosting

API = (
    "https://api.smartrecruiters.com/v1/companies/{company}/postings?limit={limit}&offset={offset}"
)
PAGE = 100
MAX_PAGES = 50


class SmartRecruitersAdapter(Adapter):
    name = "smartrecruiters"

    def fetch(self) -> list[RawPosting]:
        http = self._http()
        company = self.config["company"]
        pages: list[dict] = []
        offset = 0
        total: int | None = None
        for _ in range(MAX_PAGES):
            data = http.get_json(API.format(company=company, limit=PAGE, offset=offset))
            if not isinstance(data, dict) or "content" not in data:
                raise SourceError(
                    f"smartrecruiters: unexpected payload at offset {offset}",
                    company=self.company.name,
                )
            pages.append(data)
            if total is None:
                total = int(data.get("totalFound") or 0)
            offset += PAGE
            if offset >= total or not data["content"]:
                break
        return self.parse(pages)

    def parse(self, payload: Any) -> list[RawPosting]:
        pages = payload if isinstance(payload, list) else [payload]
        company = self.config["company"]
        out: list[RawPosting] = []
        for page in pages:
            for j in page.get("content", []):
                loc = j.get("location") or {}
                parts = [loc.get("city"), loc.get("region"), loc.get("country")]
                location = ", ".join(p for p in parts if p)
                if loc.get("remote"):
                    location = f"{location} (Remote)" if location else "Remote"
                out.append(
                    RawPosting(
                        external_id=str(j.get("id")),
                        title=(j.get("name") or "").strip(),
                        location_raw=location,
                        department=(j.get("department") or {}).get("label") or "",
                        posted_at=parse_dt(j.get("releasedDate")),
                        url=f"https://jobs.smartrecruiters.com/{company}/{j.get('id')}",
                        description_snippet="",
                        employment_type_raw=(j.get("typeOfEmployment") or {}).get("label") or "",
                    )
                )
        return out
