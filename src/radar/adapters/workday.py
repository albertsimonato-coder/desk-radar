"""Workday CXS job search API.

POST https://{tenant}.{wd}.myworkdayjobs.com/wday/cxs/{tenant}/{site}/jobs
body {"appliedFacets": {}, "limit": 20, "offset": N, "searchText": ""}
Config: tenant, wd (wd1..wd5), site, locale (default en-US), applied_facets (optional dict)
Job URL: https://{tenant}.{wd}.myworkdayjobs.com/{locale}/{site}{externalPath}
"""

from __future__ import annotations

import re
from datetime import UTC, datetime, timedelta
from typing import Any

from radar.adapters.base import Adapter, Http, SourceError
from radar.models import RawPosting

PAGE = 20
MAX_PAGES = 400  # 8000 postings hard cap per source

_POSTED_RE = re.compile(r"posted\s+(.*)", re.I)
_N_LOCATIONS_RE = re.compile(r"^\s*\d+\s+locations?\s*$", re.I)


def location_from_path(external_path: str) -> str:
    """'/job/London--United-Kingdom/Title_R123' -> 'London, United Kingdom'."""
    parts = [x for x in external_path.split("/") if x]
    if len(parts) < 2 or parts[0] != "job":
        return ""
    seg = parts[1]
    return seg.replace("--", ", ").replace("-", " ").strip()


def resolve_location(locations_text: str, external_path: str) -> str:
    if locations_text and not _N_LOCATIONS_RE.match(locations_text):
        return locations_text
    primary = location_from_path(external_path)
    if primary and locations_text:
        return f"{primary} ({locations_text.strip()})"
    return primary or locations_text or ""


def parse_posted_on(text: str, now: datetime | None = None) -> datetime | None:
    """Workday gives relative strings: 'Posted Today', 'Posted Yesterday', 'Posted 3 Days Ago',
    'Posted 30+ Days Ago'. Returns a UTC date at midnight; None if unparseable."""
    if not text:
        return None
    now = now or datetime.now(UTC)
    base = now.replace(hour=0, minute=0, second=0, microsecond=0)
    m = _POSTED_RE.search(text)
    s = (m.group(1) if m else text).strip().lower()
    if s.startswith("today"):
        return base
    if s.startswith("yesterday"):
        return base - timedelta(days=1)
    m2 = re.match(r"(\d+)\+?\s*days?\s*ago", s)
    if m2:
        return base - timedelta(days=int(m2.group(1)))
    return None


class WorkdayAdapter(Adapter):
    name = "workday"

    def __init__(self, company, http: Http | None = None):
        super().__init__(company, http)
        self.tenant = self.config["tenant"]
        self.wd = self.config["wd"]
        self.site = self.config["site"]
        self.locale = self.config.get("locale", "en-US")
        self.base = f"https://{self.tenant}.{self.wd}.myworkdayjobs.com"
        self.api = f"{self.base}/wday/cxs/{self.tenant}/{self.site}/jobs"

    def _headers(self) -> dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Origin": self.base,
            "Referer": f"{self.base}/{self.locale}/{self.site}",
        }

    def fetch(self) -> list[RawPosting]:
        http = self._http()
        facets = self.config.get("applied_facets") or {}
        search = self.config.get("search_text", "")
        offset = 0
        total: int | None = None
        pages: list[dict] = []
        for _ in range(MAX_PAGES):
            body = {"appliedFacets": facets, "limit": PAGE, "offset": offset, "searchText": search}
            data = http.post_json(self.api, json=body, headers=self._headers())
            if not isinstance(data, dict) or "jobPostings" not in data:
                raise SourceError(
                    f"workday: unexpected payload at offset {offset}", company=self.company.name
                )
            pages.append(data)
            if total is None:
                total = int(data.get("total") or 0)
            offset += PAGE
            if offset >= total or not data["jobPostings"]:
                break
        return self.parse(pages)

    def parse(self, payload: Any) -> list[RawPosting]:
        pages = payload if isinstance(payload, list) else [payload]
        out: list[RawPosting] = []
        seen: set[str] = set()
        for page in pages:
            for j in page.get("jobPostings", []):
                path = j.get("externalPath") or ""
                if not path:
                    continue
                ext_id = ""
                for bf in j.get("bulletFields") or []:
                    if isinstance(bf, str) and bf and not bf.lower().startswith("posted"):
                        ext_id = bf
                        break
                ext_id = ext_id or path.rsplit("/", 1)[-1]
                if ext_id in seen:
                    continue
                seen.add(ext_id)
                out.append(
                    RawPosting(
                        external_id=ext_id,
                        title=(j.get("title") or "").strip(),
                        location_raw=resolve_location(j.get("locationsText") or "", path),
                        department="",
                        posted_at=parse_posted_on(j.get("postedOn") or ""),
                        url=f"{self.base}/{self.locale}/{self.site}{path}",
                        description_snippet="",
                        employment_type_raw=j.get("timeType") or "",
                    )
                )
        return out
