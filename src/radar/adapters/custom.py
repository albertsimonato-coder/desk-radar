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

kind: jibe  (iCIMS "Jibe" career sites, e.g. careers.ice.com, careers.sig.com)
  config.host. The API answers an empty list until the /jobs page has set its session cookie,
  so that page is opened first; then GET https://{host}/api/jobs?page=N&limit=100&lang=en-us
  until totalCount is reached. Job URL: https://{host}/jobs/{slug}?lang=en-us

kind: phenom  (Phenom People sites, e.g. jobs.rbc.com, careers.brevanhoward.com)
  config.host, config.lang (en_gb), config.country (gb); optional config.selected_fields
  ({"country": ["United Kingdom", ...]}) narrows the search on the server.
  POST https://{host}/widgets (ddoKey refineSearch), paged with from/size.
  Job URL: https://{host}/{country}/{lang2}/job/{jobSeqNo}/{title-slug}

kind: capgemini
  GET https://www.capgemini.com/wp-json/llm/v1/jobs?page=N&size=50&country_code=a,b
  config.country_codes (list; default the six in-scope countries). Items carry title,
  location, contract_type, department, html_url. No posting date.
"""

from __future__ import annotations

import html as htmllib
import re
from typing import Any

from radar.adapters.base import Adapter, SourceError, parse_dt
from radar.models import RawPosting

_TAG = re.compile(r"<[^>]+>")
GLENCORE_API = (
    "https://www.glencore.com/.rest/api/v2/careers/?locale=en&sortBy=title-asc"
    "&offset={offset}&limit={limit}&keyword="
)
GLENCORE_PAGE = 50
GLENCORE_MAX_PAGES = 40
JIBE_PAGE = 100
JIBE_MAX_PAGES = 60
PHENOM_PAGE = 100
PHENOM_MAX_PAGES = 60
CAPGEMINI_API = "https://www.capgemini.com/wp-json/llm/v1/jobs"
CAPGEMINI_PAGE = 50
CAPGEMINI_MAX_PAGES = 80
CAPGEMINI_DEFAULT_CODES = ["en-gb", "it-it", "fr-fr", "en-ch", "fr-ch", "en-ie", "en-lu", "fr-lu"]
KINDS = ("glencore", "intervieweb", "jibe", "phenom", "capgemini")


class CustomAdapter(Adapter):
    name = "custom"

    def __init__(self, company, http=None):
        super().__init__(company, http)
        self.kind = self.config.get("kind", "")
        if self.kind not in KINDS:
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
        if self.kind == "jibe":
            return self.parse(self._fetch_jibe())
        if self.kind == "phenom":
            return self.parse(self._fetch_phenom())
        if self.kind == "capgemini":
            return self.parse(self._fetch_capgemini())
        raise SourceError("custom: nothing to fetch", company=self.company.name)

    # -- jibe -------------------------------------------------------------------------
    def _jibe_host(self) -> str:
        return self.config["host"]

    def _fetch_jibe(self) -> list[dict]:
        http = self._http()
        host = self._jibe_host()
        lang = self.config.get("lang", "en-us")
        try:
            http.get(f"https://{host}/jobs", headers={"Accept": "text/html,*/*;q=0.8"})
        except SourceError:
            pass  # the API call decides
        pages: list[dict] = []
        total: int | None = None
        got = 0
        for page in range(1, JIBE_MAX_PAGES + 1):
            data = http.get_json(
                f"https://{host}/api/jobs?page={page}&limit={JIBE_PAGE}&lang={lang}",
                headers={"Accept": "application/json", "Referer": f"https://{host}/jobs"},
            )
            if not isinstance(data, dict) or "jobs" not in data:
                raise SourceError("jibe: unexpected payload", company=self.company.name)
            if total is None:
                total = int(data.get("totalCount") or 0)
                if total == 0:
                    # Without the session cookie the API answers an empty list with HTTP 200;
                    # never treat that as "every posting closed".
                    raise SourceError(
                        "jibe: empty answer (no session cookie?)",
                        company=self.company.name,
                        retryable=True,
                    )
            pages.append(data)
            got += len(data["jobs"])
            if got >= total or not data["jobs"]:
                break
        return pages

    # -- phenom -----------------------------------------------------------------------
    def _phenom_parts(self) -> tuple[str, str, str, str]:
        host = self.config["host"]
        lang = self.config.get("lang", "en_gb")
        country = self.config.get("country", lang.split("_")[-1].lower())
        return host, lang, lang.split("_")[0], country

    def _fetch_phenom(self) -> list[dict]:
        http = self._http()
        host, lang, lang2, country = self._phenom_parts()
        pages: list[dict] = []
        total: int | None = None
        offset = 0
        for _ in range(PHENOM_MAX_PAGES):
            body = {
                "lang": lang,
                "deviceType": "desktop",
                "country": country,
                "pageName": "search-results",
                "ddoKey": "refineSearch",
                "sortBy": "",
                "subsearch": "",
                "from": offset,
                "jobs": True,
                "counts": True,
                "all_fields": ["category", "country", "state", "city", "type"],
                "size": PHENOM_PAGE,
                "clearAll": False,
                "jdsource": "facets",
                "isSliderEnable": False,
                "pageId": "page12",
                "siteType": "external",
                "keywords": "",
                "global": True,
                "selected_fields": self.config.get("selected_fields") or {},
                "locationData": {},
            }
            data = http.post_json(
                f"https://{host}/widgets",
                json=body,
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Referer": f"https://{host}/{country}/{lang2}/search-results",
                },
            )
            rs = data.get("refineSearch") if isinstance(data, dict) else None
            if not isinstance(rs, dict) or "data" not in rs:
                raise SourceError("phenom: unexpected payload", company=self.company.name)
            pages.append(data)
            jobs = (rs.get("data") or {}).get("jobs") or []
            if total is None:
                total = int(rs.get("totalHits") or 0)
            offset += PHENOM_PAGE
            if offset >= total or not jobs:
                break
        return pages

    # -- capgemini --------------------------------------------------------------------
    def _fetch_capgemini(self) -> list[dict]:
        http = self._http()
        codes = ",".join(self.config.get("country_codes") or CAPGEMINI_DEFAULT_CODES)
        pages: list[dict] = []
        for page in range(1, CAPGEMINI_MAX_PAGES + 1):
            data = http.get_json(
                f"{CAPGEMINI_API}?page={page}&size={CAPGEMINI_PAGE}&country_code={codes}",
                headers={"Accept": "application/json"},
            )
            if not isinstance(data, dict) or "items" not in data:
                raise SourceError("capgemini: unexpected payload", company=self.company.name)
            pages.append(data)
            if page >= int(data.get("total_pages") or 1) or not data["items"]:
                break
        return pages

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
        if self.kind == "jibe":
            host = self._jibe_host()
            lang = self.config.get("lang", "en-us")
            for page in pages:
                for j in page.get("jobs", []):
                    d = j.get("data") if isinstance(j, dict) else None
                    if not isinstance(d, dict) or not d.get("title"):
                        continue
                    slug = str(d.get("slug") or d.get("req_id") or "")
                    if not slug:
                        continue
                    loc = d.get("full_location") or ", ".join(
                        x for x in (d.get("city"), d.get("country")) if x
                    )
                    cats = [str(x).strip() for x in d.get("category") or [] if str(x).strip()]
                    desc = htmllib.unescape(_TAG.sub(" ", d.get("description") or ""))
                    out.append(
                        RawPosting(
                            external_id=slug,
                            title=str(d["title"]).strip(),
                            location_raw=loc,
                            department=d.get("department") or "",
                            posted_at=parse_dt(d.get("posted_date") or d.get("create_date")),
                            url=f"https://{host}/jobs/{slug}?lang={lang}",
                            description_snippet=" ".join(desc.split())[:400],
                            employment_type_raw=" ".join(cats) or d.get("employment_type") or "",
                        )
                    )
        if self.kind == "phenom":
            host, _lang, lang2, country = self._phenom_parts()
            for page in pages:
                jobs = ((page.get("refineSearch") or {}).get("data") or {}).get("jobs") or []
                for j in jobs:
                    if not isinstance(j, dict) or not j.get("title") or not j.get("jobSeqNo"):
                        continue
                    seq = str(j["jobSeqNo"])
                    slug = re.sub(r"[^A-Za-z0-9]+", "-", str(j["title"])).strip("-")
                    loc = j.get("location") or ", ".join(
                        x for x in (j.get("city"), j.get("state"), j.get("country")) if x
                    )
                    out.append(
                        RawPosting(
                            external_id=seq,
                            title=str(j["title"]).strip(),
                            location_raw=loc,
                            department=j.get("department") or j.get("category") or "",
                            posted_at=parse_dt(j.get("postedDate") or j.get("dateCreated")),
                            url=f"https://{host}/{country}/{lang2}/job/{seq}/{slug}",
                            description_snippet=" ".join(
                                str(j.get("descriptionTeaser") or "").split()
                            )[:400],
                            employment_type_raw=j.get("type") or "",
                        )
                    )
        if self.kind == "capgemini":
            for page in pages:
                for j in page.get("items", []):
                    if not isinstance(j, dict) or not j.get("title") or not j.get("html_url"):
                        continue
                    out.append(
                        RawPosting(
                            external_id=str(j.get("id") or j["html_url"]),
                            title=str(j["title"]).strip(),
                            location_raw=j.get("location") or "",
                            department=j.get("department") or j.get("brand") or "",
                            posted_at=None,
                            url=j["html_url"],
                            description_snippet="",
                            employment_type_raw=j.get("contract_type") or "",
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
