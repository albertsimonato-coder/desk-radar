"""Sitemap adapter for bespoke portals that expose job pages with schema.org JobPosting JSON-LD.

Config:
  sitemap_url       (optional; otherwise discovered from robots.txt, then /sitemap.xml)
  rss_url           (optional) an RSS/Atom feed of jobs; items become postings directly
                    (title, link, description, pubDate, g:location) without fetching pages
  index_urls        (optional) HTML listing pages whose links are harvested instead of / in
                    addition to the sitemap (set sitemap_url: none to skip the sitemap)
  index_url_pattern (optional) paginated listing URL with an {offset} placeholder, walked with
                    index_step (default 15) until a page adds no new job links or
                    index_max_pages (default 40) is reached
  index_item_regex  (optional) regex run over each listing page (whitespace collapsed) with a
                    named group `url` and optional `location`, `department`, `employment_type`;
                    the values fill fields the job page itself does not provide
  job_url_pattern   regex a job URL must match
  max_new_pages     cap on job pages fetched per run (default 50)
  url_prefix        (optional) only keep URLs starting with this
  title_strip       (optional) regex removed from fallback titles, e.g. " - Marex Careers$"
  location_regex    (optional) regex applied to the meta description, or to the raw page when
                    the JSON-LD has no jobLocation; its capture groups are joined with ", "

The adapter diffs the sitemap's job URLs against the postings the runner already knows
(`self.known_postings`, url -> RawPosting). Known URLs are returned as-is without a fetch; new
URLs are fetched (up to the cap) and parsed. URLs beyond the cap are left for the next run.
"""

from __future__ import annotations

import logging
import re
from typing import Any
from urllib.parse import urljoin, urlsplit

from selectolax.lexbor import LexborHTMLParser as HTMLParser

from radar.adapters.base import Adapter, SourceError
from radar.adapters.jsonld import extract_job_postings, parse_fallback, parse_job_page
from radar.models import RawPosting

log = logging.getLogger(__name__)

MAX_SITEMAPS = 50
_LOC_RE = re.compile(r"<loc>\s*(.*?)\s*</loc>", re.I | re.S)
_ITEM_RE = re.compile(r"<(?:item|entry)>(.*?)</(?:item|entry)>", re.I | re.S)
_TITLE_LOC_RE = re.compile(r"^(.*?)\s*\(([^()]{2,80})\)\s*$")


def _tag(block: str, *names: str) -> str:
    for n in names:
        m = re.search(rf"<{n}[^>]*>(.*?)</{n}>", block, re.S | re.I)
        if m:
            v = m.group(1).strip()
            if v.startswith("<![CDATA["):
                v = v[9:-3] if v.endswith("]]>") else v[9:]
            return html_unescape(v.strip())
    return ""


def parse_rss(
    xml: str, pattern: re.Pattern | None = None, location_from_title: bool = True
) -> list[RawPosting]:
    """Turn a job RSS/Atom feed into postings. SuccessFactors feeds put the location in
    <g:location> and repeat it in parentheses at the end of the title."""
    out: list[RawPosting] = []
    for block in _ITEM_RE.findall(xml):
        link = _tag(block, "link", "guid")
        if not link:
            m = re.search(r'<link[^>]*href="([^"]+)"', block)
            link = m.group(1) if m else ""
        if not link or (pattern and not pattern.search(link)):
            continue
        title = _tag(block, "title")
        location = _tag(block, "g:location", "location")
        m = _TITLE_LOC_RE.match(title)
        if m and location_from_title:
            if not location:
                location = m.group(2)
            if m.group(2) == location or location in m.group(2):
                title = m.group(1).strip()
        desc = _tag(block, "description", "summary", "content")
        desc = re.sub(r"<[^>]+>", " ", html_unescape(desc))
        out.append(
            RawPosting(
                external_id=_tag(block, "g:id", "guid") or link,
                title=title,
                location_raw=location,
                department=_tag(block, "category"),
                posted_at=parse_dt_rfc(_tag(block, "pubDate", "published", "updated")),
                url=link,
                description_snippet=" ".join(desc.split())[:400],
                employment_type_raw=_tag(block, "g:job_type", "employmentType"),
            )
        )
    return out


def parse_dt_rfc(s: str):
    from email.utils import parsedate_to_datetime

    from radar.adapters.base import parse_dt

    if not s:
        return None
    try:
        dt = parsedate_to_datetime(s)
        return dt if dt.tzinfo else dt.replace(tzinfo=__import__("datetime").UTC)
    except (TypeError, ValueError):
        return parse_dt(s)


_SITEMAP_RE = re.compile(r"^\s*sitemap:\s*(\S+)", re.I | re.M)


class SitemapAdapter(Adapter):
    name = "sitemap"

    def __init__(self, company, http=None):
        super().__init__(company, http)
        self.pattern = re.compile(self.config["job_url_pattern"], re.I)
        self.max_new = int(self.config.get("max_new_pages", 50))
        self.prefix = self.config.get("url_prefix") or ""
        self.index_urls: list[str] = list(self.config.get("index_urls") or [])
        self.index_url_pattern: str = self.config.get("index_url_pattern") or ""
        self.index_step = int(self.config.get("index_step", 15))
        self.index_max_pages = int(self.config.get("index_max_pages", 40))
        self.index_item_re = (
            re.compile(self.config["index_item_regex"], re.S)
            if self.config.get("index_item_regex")
            else None
        )
        self._index_meta: dict[str, dict[str, str]] = {}
        self.title_strip = self.config.get("title_strip") or ""
        self.location_regex = self.config.get("location_regex") or ""

    # ---- discovery --------------------------------------------------------
    def _sitemap_urls(self) -> list[str]:
        if self.config.get("sitemap_url"):
            if str(self.config["sitemap_url"]).lower() == "none":
                return []
            return [self.config["sitemap_url"]]
        base = str(self.company.careers_url)
        root = f"{urlsplit(base).scheme}://{urlsplit(base).netloc}/"
        http = self._http()
        resp = http.get(urljoin(root, "robots.txt"))
        found = _SITEMAP_RE.findall(resp.text) if resp.status_code == 200 else []
        return found or [urljoin(root, "sitemap.xml")]

    def _collect(self, url: str, seen: set[str], out: set[str], depth: int = 0) -> None:
        if url in seen or len(seen) >= MAX_SITEMAPS:
            return
        seen.add(url)
        resp = self._http().get(url)
        if resp.status_code != 200:
            raise SourceError(
                f"sitemap: HTTP {resp.status_code} from {url}", company=self.company.name
            )
        body = resp.text
        locs = [html_unescape(x) for x in _LOC_RE.findall(body)]
        is_index = "<sitemapindex" in body[:2000].lower()
        for loc in locs:
            if is_index or loc.lower().endswith((".xml", ".xml.gz")):
                if depth < 2:
                    self._collect(loc, seen, out, depth + 1)
            elif self.pattern.search(loc) and loc.startswith(self.prefix):
                out.add(loc)

    def _harvest_index(self, url: str, out: set[str]) -> int:
        """Add job links found on one listing page; returns how many were new."""
        resp = self._http().get(url)
        if resp.status_code != 200:
            raise SourceError(
                f"index page: HTTP {resp.status_code} from {url}", company=self.company.name
            )
        tree = HTMLParser(resp.text)
        before = len(out)
        for a in tree.css("a[href]"):
            href = urljoin(url, a.attributes.get("href", "")).split("#")[0]
            if self.pattern.search(href) and href.startswith(self.prefix):
                out.add(href)
        if self.index_item_re:
            flat = " ".join(resp.text.split())
            for m in self.index_item_re.finditer(flat):
                g = m.groupdict()
                href = urljoin(url, html_unescape(g.get("url") or "")).split("#")[0]
                if href:
                    self._index_meta[href] = {
                        k: html_unescape(v).strip() for k, v in g.items() if k != "url" and v
                    }
        return len(out) - before

    def _apply_meta(self, posting: RawPosting) -> RawPosting:
        meta = self._index_meta.get(posting.url)
        if not meta:
            return posting
        if meta.get("location") and not posting.location_raw:
            posting.location_raw = meta["location"]
        if meta.get("department") and not posting.department:
            posting.department = meta["department"]
        if meta.get("employment_type") and not posting.employment_type_raw:
            posting.employment_type_raw = meta["employment_type"]
        return posting

    def job_urls(self) -> set[str]:
        urls: set[str] = set()
        seen: set[str] = set()
        for sm in self._sitemap_urls():
            self._collect(sm, seen, urls)
        for page in self.index_urls:
            self._harvest_index(page, urls)
        if self.index_url_pattern:
            for i in range(self.index_max_pages):
                added = self._harvest_index(
                    self.index_url_pattern.format(offset=i * self.index_step), urls
                )
                if added == 0:
                    break
        return urls

    def _parse_page(self, html: str, url: str) -> RawPosting | None:
        if extract_job_postings(html):
            posting = parse_job_page(html, url)
            if posting and not posting.location_raw and self.location_regex:
                m = re.search(self.location_regex, html, re.S)
                if m:
                    posting.location_raw = ", ".join(
                        g.strip() for g in m.groups() if g and g.strip()
                    )
            if posting and self.title_strip:
                posting.title = re.sub(self.title_strip, "", posting.title).strip(" -|:")
            return posting
        return parse_fallback(html, url, self.title_strip, self.location_regex)

    # ---- fetch ------------------------------------------------------------
    def fetch(self) -> list[RawPosting]:
        if self.config.get("rss_url"):
            resp = self._http().get(self.config["rss_url"])
            if resp.status_code != 200:
                raise SourceError(f"rss: HTTP {resp.status_code}", company=self.company.name)
            postings = parse_rss(resp.text, self.pattern)
            if not postings:
                raise SourceError(
                    "rss: no items matched job_url_pattern", company=self.company.name
                )
            return postings
        urls = self.job_urls()
        if not urls:
            raise SourceError(
                "sitemap: no job URLs matched job_url_pattern", company=self.company.name
            )
        known = self.known_postings
        out: list[RawPosting] = [self._apply_meta(known[u]) for u in urls if u in known]
        new = sorted(u for u in urls if u not in known)
        fetched = 0
        for u in new:
            if fetched >= self.max_new:
                log.info(
                    "%s: %d new job pages left for next run", self.company.name, len(new) - fetched
                )
                break
            fetched += 1
            try:
                resp = self._http().get(u)
            except SourceError as e:
                log.warning("%s: %s", self.company.name, e)
                continue
            if resp.status_code != 200:
                continue
            posting = self._parse_page(resp.text, u)
            if posting:
                out.append(self._apply_meta(posting))
        return out

    def parse(self, payload: Any) -> list[RawPosting]:
        """Fixture format: {"urls": [...], "pages": {url: html}} or {"rss": "<xml>"}."""
        if isinstance(payload, dict) and payload.get("rss"):
            return parse_rss(payload["rss"], self.pattern)
        out: list[RawPosting] = []
        for u in payload.get("urls", []):
            if u in self.known_postings:
                out.append(self.known_postings[u])
                continue
            html = payload.get("pages", {}).get(u)
            if html:
                p = self._parse_page(html, u)
                if p:
                    out.append(p)
        return out


def html_unescape(s: str) -> str:
    return HTMLParser(f"<a>{s}</a>").text() if "&" in s else s
