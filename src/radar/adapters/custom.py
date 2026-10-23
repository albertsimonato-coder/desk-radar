"""Bespoke employer APIs that are too simple to deserve their own ATS type.

ats: custom, config.kind selects the fetcher.

kind: glencore
  GET https://www.glencore.com/.rest/api/v2/careers/?locale=en&sortBy=title-asc&offset=N&limit=50
  Items carry jobId, title, city, region, country, highlights, description.
  Job URL: https://www.glencore.com/en/careers/jobs/{jobId}
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
        if self.kind not in ("glencore",):
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
        return out
