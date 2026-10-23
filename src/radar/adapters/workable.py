"""Workable public widget API.

GET https://www.workable.com/api/accounts/{account}?details=false
Config: account (the slug in apply.workable.com/<account>/)
"""

from __future__ import annotations

from typing import Any

from radar.adapters.base import Adapter, SourceError, parse_dt
from radar.models import RawPosting

API = "https://www.workable.com/api/accounts/{account}?details=false"


class WorkableAdapter(Adapter):
    name = "workable"

    def fetch(self) -> list[RawPosting]:
        return self.parse(self._http().get_json(API.format(account=self.config["account"])))

    def parse(self, payload: Any) -> list[RawPosting]:
        if not isinstance(payload, dict) or "jobs" not in payload:
            raise SourceError("workable: unexpected payload (no 'jobs')", company=self.company.name)
        out: list[RawPosting] = []
        for j in payload["jobs"]:
            parts = [j.get("city"), j.get("state"), j.get("country")]
            location = ", ".join(p for p in parts if p)
            if (j.get("workplace") or "").lower() == "remote" or j.get("telecommuting"):
                location = f"{location} (Remote)" if location else "Remote"
            out.append(
                RawPosting(
                    external_id=str(j.get("shortcode") or j.get("code") or j.get("url")),
                    title=(j.get("title") or "").strip(),
                    location_raw=location,
                    department=j.get("department") or "",
                    posted_at=parse_dt(j.get("published_on") or j.get("created_at")),
                    url=j.get("url") or j.get("shortlink") or "",
                    description_snippet=" ".join((j.get("description") or "")[:400].split()),
                    employment_type_raw=j.get("employment_type") or "",
                )
            )
        return out
