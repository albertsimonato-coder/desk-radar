"""Greenhouse job board API.

GET https://boards-api.greenhouse.io/v1/boards/{board}/jobs?content=true
Config: board
"""

from __future__ import annotations

import html
import re
from typing import Any

from radar.adapters.base import Adapter, SourceError, parse_dt
from radar.models import RawPosting

API = "https://boards-api.greenhouse.io/v1/boards/{board}/jobs?content=true"
_TAG = re.compile(r"<[^>]+>")


def _snippet(content: str, n: int = 400) -> str:
    text = html.unescape(content or "")  # Greenhouse escapes the HTML itself
    text = html.unescape(_TAG.sub(" ", text))
    text = re.sub(r"\s+", " ", text).strip()
    return text[:n]


class GreenhouseAdapter(Adapter):
    name = "greenhouse"

    def fetch(self) -> list[RawPosting]:
        board = self.config["board"]
        url = API.format(board=board)
        data = self._http().get_json(url)
        return self.parse(data)

    def parse(self, payload: Any) -> list[RawPosting]:
        if not isinstance(payload, dict) or "jobs" not in payload:
            raise SourceError(
                "greenhouse: unexpected payload (no 'jobs')", company=self.company.name
            )
        out: list[RawPosting] = []
        for j in payload["jobs"]:
            loc = (j.get("location") or {}).get("name", "") or ""
            offices = j.get("offices") or []
            if not loc and offices:
                loc = ", ".join(o.get("name", "") for o in offices if o.get("name"))
            depts = j.get("departments") or []
            dept = ", ".join(d.get("name", "") for d in depts if d.get("name"))
            emp_type = ""
            for m in j.get("metadata") or []:
                nm = (m.get("name") or "").lower()
                if "employment" in nm or "job type" in nm or "type" == nm:
                    v = m.get("value")
                    emp_type = ", ".join(v) if isinstance(v, list) else str(v or "")
                    break
            out.append(
                RawPosting(
                    external_id=str(j.get("id")),
                    title=(j.get("title") or "").strip(),
                    location_raw=loc,
                    department=dept,
                    posted_at=parse_dt(j.get("first_published") or j.get("updated_at")),
                    url=j.get("absolute_url") or "",
                    description_snippet=_snippet(j.get("content", "")),
                    employment_type_raw=emp_type,
                )
            )
        return out
