"""Bespoke employer APIs that are too simple to deserve their own ATS type.

ats: custom, config.kind selects the fetcher.

kind: glencore
  GET https://www.glencore.com/.rest/api/v2/careers/?locale=en&sortBy=title-asc&offset=N&limit=50
  Items carry jobId, title, city, region, country, highlights, description.
  Job URL: https://www.glencore.com/en/careers/jobs/{jobId}

kind: intervieweb  (In-recruiting / Intervieweb, common among Italian employers)
  config.page_url: the employer page that embeds the widget; the adapter extracts the
  `https://<tenant>.intervieweb.it/annunci.php?...&format=json_en` feed URL from it each run
  (or set config.feed_url directly). Items carry title, city, nation, published, url, function.
"""

from __future__ import annotations

import html as htmllib
import re
from typing import Any

from radar.adapters.base import Adapter, SourceError
from radar.models import RawPosting

_TAG = re.compile(r"<[^>]+>")
GLENCORE_API = (
    "https://www.glencore.com/.rest/api/v2/careers/?locale=en&sortBy=title-asc"
    "&offset={offset}&limit={limit}&keyword="
)
GLENCORE_PAGE = 50
GLENCORE_MAX_PAGES = 40


class CustomAdapter(Adapter):
    name = "custom"

    def __init__(self, company, http=None):
        super().__init__(company, http)
        self.kind = self.config.get("kind", "")
        if self.kind not in ("glencore", "intervieweb"):
            raise SourceError(f"custom: unknown kind {self.kind!r}", company=company.name)

    def fetch(self) -> list[RawPosting]:
        if self.kind == "glencore":
            http = self._http()
            pages: list[dict] = []
            offset = 0
            total = None
            for _ in range(GLENCORE_MAX_PAGES):
                data = http.get_json(
                    GLENCORE_API.format(offset=offset, limit=GLENCORE_PAGE),
                    headers={
                        "Accept": "application/json",
                        "Referer": "https://www.glencore.com/en/careers/jobs",
                    },
                )
                if not isinstance(data, dict) or "data" not in data:
                    raise SourceError("glencore: unexpected payload", company=self.company.name)
                pages.append(data)
                if total is None:
                    total = int(data.get("totalResults") or 0)
                offset += GLENCORE_PAGE
                if offset >= total or not data["data"]:
                    break
            return self.parse(pages)
        if self.kind == "intervieweb":
            http = self._http()
            feed = self.config.get("feed_url")
            if not feed:
                page = http.get(self.config["page_url"])
                m = re.search(
                    r"(https?://[a-z0-9.-]+\.intervieweb\.it/annunci\.php\?[^\"'\s<>]+)", page.text
                )
                if not m:
                    raise SourceError(
                        "intervieweb: feed URL not found on page", company=self.company.name
                    )
                feed = htmllib.unescape(m.group(1))
            data = http.get_json(
                feed,
                headers={"Accept": "application/json", "Referer": self.config.get("page_url", "")},
            )
            return self.parse(data)
        raise SourceError("custom: nothing to fetch", company=self.company.name)

    def parse(self, payload: Any) -> list[RawPosting]:
        pages = payload if isinstance(payload, list) else [payload]
        out: list[RawPosting] = []
        if self.kind == "glencore":
            for page in pages:
                for j in page.get("data", []):
                    job_id = str(j.get("jobId") or j.get("id") or "")
                    if not job_id:
                        continue
                    loc = ", ".join(
                        x for x in (j.get("city"), j.get("region"), j.get("country")) if x
                    )
                    hl = [h for h in j.get("highlights") or [] if isinstance(h, str)]
                    emp = next(
                        (
                            h
                            for h in hl
                            if re.search(r"full|part|intern|graduate|contract|time", h, re.I)
                        ),
                        "",
                    )
                    desc = htmllib.unescape(_TAG.sub(" ", j.get("description") or ""))
                    out.append(
                        RawPosting(
                            external_id=job_id,
                            title=(j.get("title") or "").strip(),
                            location_raw=loc,
                            department=j.get("feed") or "",
                            posted_at=None,
                            url=f"https://www.glencore.com/en/careers/jobs/{job_id}",
                            description_snippet=" ".join(desc.split())[:400],
                            employment_type_raw=emp,
                        )
                    )
        if self.kind == "intervieweb":
            items = payload if isinstance(payload, list) else payload.get("jobs", [])
            for j in items:
                if not isinstance(j, dict) or not j.get("title"):
                    continue
                loc = ", ".join(x for x in (j.get("city"), j.get("nation")) if x)
                out.append(
                    RawPosting(
                        external_id=str(j.get("id") or j.get("slug") or j.get("url")),
                        title=str(j["title"]).strip(),
                        location_raw=loc,
                        department=j.get("function") or "",
                        posted_at=_intervieweb_date(j.get("published")),
                        url=j.get("url") or "",
                        description_snippet="",
                        employment_type_raw=j.get("contract_type")
                        or j.get("seniority_level")
                        or "",
                    )
                )
        return out


def _intervieweb_date(s):
    """'12-10-2026 (18:01)' -> datetime."""
    from radar.adapters.base import parse_dt

    if not s:
        return None
    m = re.match(r"(\d{2})-(\d{2})-(\d{4})", str(s))
    return parse_dt(f"{m.group(3)}-{m.group(2)}-{m.group(1)}") if m else None
