"""Ashby job board API.

GET https://api.ashbyhq.com/posting-api/job-board/{board}?includeCompensation=false
Config: board
"""

from __future__ import annotations

from typing import Any

from radar.adapters.base import Adapter, SourceError, parse_dt
from radar.models import RawPosting

API = "https://api.ashbyhq.com/posting-api/job-board/{board}?includeCompensation=false"


class AshbyAdapter(Adapter):
    name = "ashby"

    def fetch(self) -> list[RawPosting]:
        return self.parse(self._http().get_json(API.format(board=self.config["board"])))

    def parse(self, payload: Any) -> list[RawPosting]:
        if not isinstance(payload, dict) or "jobs" not in payload:
            raise SourceError("ashby: unexpected payload (no 'jobs')", company=self.company.name)
        out: list[RawPosting] = []
        for j in payload["jobs"]:
            if j.get("isListed") is False:
                continue
            location = j.get("location") or ""
            extra = [
                x.get("location") for x in j.get("secondaryLocations") or [] if x.get("location")
            ]
            if extra:
                location = "; ".join([location, *extra]) if location else "; ".join(extra)
            if j.get("isRemote") and "remote" not in location.lower():
                location = f"{location} (Remote)" if location else "Remote"
            dept = ", ".join(x for x in (j.get("team"), j.get("department")) if x)
            text = (j.get("descriptionPlain") or "")[:400]
            out.append(
                RawPosting(
                    external_id=str(j.get("id")),
                    title=(j.get("title") or "").strip(),
                    location_raw=location,
                    department=dept,
                    posted_at=parse_dt(j.get("publishedAt")),
                    url=j.get("jobUrl") or j.get("applyUrl") or "",
                    description_snippet=" ".join(text.split()),
                    employment_type_raw=j.get("employmentType") or "",
                )
            )
        return out
