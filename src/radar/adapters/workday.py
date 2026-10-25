"""Workday CXS job search API.

POST https://{tenant}.{wd}.myworkdayjobs.com/wday/cxs/{tenant}/{site}/jobs
body {"appliedFacets": {}, "limit": 20, "offset": N, "searchText": ""}
Config: tenant, wd (wd1..wd5), site, locale (default en-US), applied_facets (optional dict)
Job URL: https://{tenant}.{wd}.myworkdayjobs.com/{locale}/{site}{externalPath}
"""

from __future__ import annotations

import logging
import re
import time
from datetime import UTC, datetime, timedelta
from typing import Any

from radar.adapters.base import Adapter, Http, SourceError, parse_dt
from radar.models import RawPosting

log = logging.getLogger(__name__)

PAGE = 20
MAX_PAGES = 400  # 8000 postings hard cap per source
DETAIL_CAP = 40  # job-detail requests per run, for postings the list gives no exact date for

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
        # A few tenants spell the API tenant differently from the host ("osv-cci" vs "osv_cci").
        cxs_tenant = self.config.get("cxs_tenant", self.tenant)
        self.api = f"{self.base}/wday/cxs/{cxs_tenant}/{self.site}/jobs"

    def _headers(self) -> dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Origin": self.base,
            "Referer": f"{self.base}/{self.locale}/{self.site}",
        }

    def _open_session(self, http: Http) -> None:
        """Workday answers the CXS API more reliably once the site page has set its cookies."""
        try:
            http.get(
                f"{self.base}/{self.locale}/{self.site}", headers={"Accept": "text/html,*/*;q=0.8"}
            )
        except SourceError:
            pass  # the API call below decides

    def _page(self, http: Http, body: dict) -> dict:
        try:
            data = http.post_json(self.api, json=body, headers=self._headers())
        except SourceError as e:
            if not e.retryable:
                raise
            time.sleep(5)  # bot wall or empty body: re-open the session and try once more
            self._open_session(http)
            data = http.post_json(self.api, json=body, headers=self._headers())
        return data

    def fetch(self) -> list[RawPosting]:
        http = self._http()
        self._open_session(http)
        facets = self.config.get("applied_facets") or {}
        search = self.config.get("search_text", "")
        offset = 0
        total: int | None = None
        pages: list[dict] = []
        for _ in range(MAX_PAGES):
            body = {"appliedFacets": facets, "limit": PAGE, "offset": offset, "searchText": search}
            data = self._page(http, body)
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
        postings = self.parse(pages)
        self._backfill_dates(http, pages, postings)
        return postings

    def _backfill_dates(self, http: Http, pages: list[dict], postings: list[RawPosting]) -> None:
        """Some tenants omit postedOn from the list, and "30+ Days Ago" is only a bound; the
        job-detail endpoint has the exact startDate. Fetch it for new postings, DETAIL_CAP per
        run, so a newly added employer gets its dates over a few runs."""
        posted_on = {}
        for page in pages:
            for j in page.get("jobPostings", []):
                path = j.get("externalPath") or ""
                if path:
                    posted_on[f"{self.base}/{self.locale}/{self.site}{path}"] = (
                        j.get("postedOn") or ""
                    )
        known = self.known_postings
        todo = []
        for p in postings:
            raw = posted_on.get(p.url, "")
            if p.posted_at is not None and "30+" not in raw:
                continue
            k = known.get(p.url)
            if k is not None and k.posted_at is not None:
                continue
            todo.append(p)
        todo.sort(key=lambda p: p.url not in known)  # stored (in-scope) rows first
        for p in todo[:DETAIL_CAP]:
            path = p.url.split(f"/{self.site}", 1)[-1]
            try:
                data = http.get_json(
                    self.api[: -len("/jobs")] + path,
                    headers={
                        "Accept": "application/json",
                        "Referer": f"{self.base}/{self.locale}/{self.site}",
                    },
                )
            except SourceError as e:
                log.debug("%s: detail %s: %s", self.company.name, path, e)
                continue
            info = data.get("jobPostingInfo") if isinstance(data, dict) else None
            dt = parse_dt((info or {}).get("startDate"))
            if dt:
                p.posted_at = dt

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
