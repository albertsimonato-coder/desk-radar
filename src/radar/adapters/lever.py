"""Lever postings API.

GET https://api.lever.co/v0/postings/{company}?mode=json
Config: company
"""

from __future__ import annotations

from typing import Any

from radar.adapters.base import Adapter, SourceError, parse_dt
from radar.models import RawPosting

API = "https://api.lever.co/v0/postings/{company}?mode=json"


class LeverAdapter(Adapter):
    name = "lever"

    def fetch(self) -> list[RawPosting]:
        return self.parse(self._http().get_json(API.format(company=self.config["company"])))

    def parse(self, payload: Any) -> list[RawPosting]:
        if not isinstance(payload, list):
            raise SourceError("lever: unexpected payload (not a list)", company=self.company.name)
        out: list[RawPosting] = []
        for j in payload:
            cats = j.get("categories") or {}
            location = cats.get("location") or ""
            extra = j.get("allLocations") or []
            if extra and isinstance(extra, list):
                location = (
                    "; ".join(dict.fromkeys([location, *extra])) if location else "; ".join(extra)
                )
            dept = ", ".join(x for x in (cats.get("team"), cats.get("department")) if x)
            text = (j.get("descriptionPlain") or j.get("description") or "")[:400]
            out.append(
                RawPosting(
                    external_id=str(j.get("id")),
                    title=(j.get("text") or "").strip(),
                    location_raw=location,
                    department=dept,
                    posted_at=parse_dt(j.get("createdAt")),
                    url=j.get("hostedUrl") or j.get("applyUrl") or "",
                    description_snippet=" ".join(text.split()),
                    employment_type_raw=cats.get("commitment") or "",
                )
            )
        return out
