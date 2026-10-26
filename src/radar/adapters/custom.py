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

kind: bamboohr  (BambooHR hosted career pages, e.g. panmure.bamboohr.com)
  config.subdomain. GET https://{subdomain}.bamboohr.com/careers/list -> {"result": [...]}.
  Items carry id, jobOpeningName, departmentLabel, employmentStatusLabel, location{city,state}.
  Job URL: https://{subdomain}.bamboohr.com/careers/{id}. No posting date.

kind: oracle  (Oracle HCM Cloud "CandidateExperience" sites)
  config.host (e.g. fa-euxc-saasfaprod1.fa.ocs.oraclecloud.com), config.site (e.g. CX_1).
  GET https://{host}/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true
      &finder=findReqs;siteNumber={site},limit=100,offset=N,sortBy=POSTING_DATES_DESC
  -> items[0].requisitionList (Id, Title, PostedDate, PrimaryLocation, JobFamily...),
     items[0].TotalJobsCount. Job URL: https://{host}/hcmUI/CandidateExperience/en/sites/{site}/job/{Id}

kind: wordpress  (WordPress sites that publish jobs as a custom post type over the REST API)
  config.base (REST root, e.g. https://iqeq.com/careers/wp-json/wp/v2), config.type (the
  post type's rest base, e.g. vacancy / job), optional config.location_taxonomy and
  config.department_taxonomy (taxonomy rest bases whose term ids the posts carry; the
  terms are fetched once and mapped to names). Items carry title.rendered, link, date.

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
ORACLE_PAGE = 100
ORACLE_MAX_PAGES = 60
WP_PAGE = 100
WP_MAX_PAGES = 40
KINDS = ("glencore", "intervieweb", "jibe", "phenom", "capgemini", "bamboohr", "oracle", "wordpress")


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
        if self.kind == "bamboohr":
            return self.parse(self._fetch_bamboohr())
        if self.kind == "oracle":
            return self.parse(self._fetch_oracle())
        if self.kind == "wordpress":
            return self.parse(self._fetch_wordpress())
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

    # -- bamboohr ---------------------------------------------------------------------
    def _fetch_bamboohr(self) -> dict:
        sub = self.config["subdomain"]
        data = self._http().get_json(
            f"https://{sub}.bamboohr.com/careers/list",
            headers={"Accept": "application/json", "Referer": f"https://{sub}.bamboohr.com/careers"},
        )
        if not isinstance(data, dict) or "result" not in data:
            raise SourceError("bamboohr: unexpected payload", company=self.company.name)
        return data

    # -- oracle -----------------------------------------------------------------------
    def _oracle_parts(self) -> tuple[str, str]:
        return self.config["host"], self.config.get("site", "CX_1")

    def _fetch_oracle(self) -> list[dict]:
        http = self._http()
        host, site = self._oracle_parts()
        pages: list[dict] = []
        total: int | None = None
        got = 0
        for page in range(ORACLE_MAX_PAGES):
            url = (
                f"https://{host}/hcmRestApi/resources/latest/recruitingCEJobRequisitions"
                f"?onlyData=true&expand=requisitionList.secondaryLocations"
                f"&finder=findReqs;siteNumber={site},limit={ORACLE_PAGE},"
                f"offset={page * ORACLE_PAGE},sortBy=POSTING_DATES_DESC"
            )
            data = http.get_json(url, headers={"Accept": "application/json"})
            items = data.get("items") if isinstance(data, dict) else None
            if not items or not isinstance(items[0], dict):
                raise SourceError("oracle: unexpected payload", company=self.company.name)
            reqs = items[0].get("requisitionList") or []
            if total is None:
                total = int(items[0].get("TotalJobsCount") or 0)
            pages.append(data)
            got += len(reqs)
            if got >= total or not reqs:
                break
        return pages

    # -- wordpress --------------------------------------------------------------------
    def _wp_terms(self, taxonomy: str) -> dict[int, str]:
        """Term id -> name for one taxonomy (first 100 terms per page, a few pages)."""
        http = self._http()
        base = self.config["base"].rstrip("/")
        out: dict[int, str] = {}
        for page in range(1, 6):
            data = http.get_json(
                f"{base}/{taxonomy}?per_page=100&page={page}",
                headers={"Accept": "application/json"},
            )
            if not isinstance(data, list) or not data:
                break
            for t in data:
                if isinstance(t, dict) and t.get("id") is not None:
                    out[int(t["id"])] = htmllib.unescape(str(t.get("name") or ""))
            if len(data) < 100:
                break
        return out

    def _fetch_wordpress(self) -> dict:
        http = self._http()
        base = self.config["base"].rstrip("/")
        ptype = self.config["type"]
        posts: list[dict] = []
        for page in range(1, WP_MAX_PAGES + 1):
            resp = http.get(
                f"{base}/{ptype}?per_page={WP_PAGE}&page={page}&_fields=id,date,link,title,excerpt,"
                + ",".join(
                    x
                    for x in (
                        self.config.get("location_taxonomy", ""),
                        self.config.get("department_taxonomy", ""),
                    )
                    if x
                ),
                headers={"Accept": "application/json"},
            )
            if resp.status_code == 400 and page > 1:  # past the last page
                break
            if resp.status_code != 200:
                raise SourceError(
                    f"wordpress: HTTP {resp.status_code} from {resp.url}", company=self.company.name
                )
            data = resp.json()
            if not isinstance(data, list):
                raise SourceError("wordpress: unexpected payload", company=self.company.name)
            posts.extend(x for x in data if isinstance(x, dict))
            if len(data) < WP_PAGE:
                break
        terms: dict[str, dict[int, str]] = {}
        for key in ("location_taxonomy", "department_taxonomy"):
            tax = self.config.get(key)
            if tax:
                terms[tax] = self._wp_terms(tax)
        return {"posts": posts, "terms": terms}

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
                            posted_at=parse_dt(j.get("startDate")),
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
        if self.kind == "bamboohr":
            sub = self.config["subdomain"]
            for page in pages:
                for j in page.get("result", []):
                    if not isinstance(j, dict) or not j.get("jobOpeningName") or not j.get("id"):
                        continue
                    locd = j.get("location") or {}
                    loc = ", ".join(
                        x for x in (locd.get("city"), locd.get("state")) if x
                    ) if isinstance(locd, dict) else ""
                    out.append(
                        RawPosting(
                            external_id=str(j["id"]),
                            title=str(j["jobOpeningName"]).strip(),
                            location_raw=loc,
                            department=j.get("departmentLabel") or "",
                            posted_at=None,
                            url=f"https://{sub}.bamboohr.com/careers/{j['id']}",
                            description_snippet="",
                            employment_type_raw=j.get("employmentStatusLabel") or "",
                        )
                    )
        if self.kind == "oracle":
            host, site = self._oracle_parts()
            for page in pages:
                items = page.get("items") or []
                reqs = items[0].get("requisitionList") or [] if items else []
                for j in reqs:
                    if not isinstance(j, dict) or not j.get("Title") or not j.get("Id"):
                        continue
                    out.append(
                        RawPosting(
                            external_id=str(j["Id"]),
                            title=str(j["Title"]).strip(),
                            location_raw=j.get("PrimaryLocation") or "",
                            department=j.get("JobFamily") or j.get("JobFunction") or "",
                            posted_at=parse_dt(j.get("PostedDate")),
                            url=(
                                f"https://{host}/hcmUI/CandidateExperience/en/sites/{site}"
                                f"/job/{j['Id']}"
                            ),
                            description_snippet=" ".join(
                                htmllib.unescape(_TAG.sub(" ", j.get("ShortDescriptionStr") or "")).split()
                            )[:400],
                            employment_type_raw=j.get("WorkerType") or j.get("JobType") or "",
                        )
                    )
        if self.kind == "wordpress":
            data = payload if isinstance(payload, dict) else {}
            terms = data.get("terms") or {}
            loc_tax = self.config.get("location_taxonomy", "")
            dep_tax = self.config.get("department_taxonomy", "")

            def names(post: dict, tax: str) -> str:
                ids = post.get(tax) if tax else None
                if not isinstance(ids, list):
                    return ""
                tmap = terms.get(tax) or {}
                found = []
                for i in ids:
                    if i is None:
                        continue
                    n = tmap.get(i) or tmap.get(str(i)) or tmap.get(int(i)) if str(i).isdigit() else tmap.get(i)
                    if n:
                        found.append(htmllib.unescape(str(n)))
                return ", ".join(found)

            for j in data.get("posts") or []:
                title = j.get("title")
                title = title.get("rendered") if isinstance(title, dict) else title
                if not isinstance(j, dict) or not title or not j.get("link"):
                    continue
                excerpt = j.get("excerpt")
                excerpt = excerpt.get("rendered") if isinstance(excerpt, dict) else (excerpt or "")
                out.append(
                    RawPosting(
                        external_id=str(j.get("id") or j["link"]),
                        title=htmllib.unescape(_TAG.sub(" ", str(title))).strip(),
                        location_raw=names(j, loc_tax),
                        department=names(j, dep_tax),
                        posted_at=parse_dt(j.get("date")),
                        url=j["link"],
                        description_snippet=" ".join(
                            htmllib.unescape(_TAG.sub(" ", str(excerpt))).split()
                        )[:400],
                        employment_type_raw="",
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
