"""Sitemap adapter for bespoke portals that expose job pages with schema.org JobPosting JSON-LD.

Config:
  sitemap_url       (optional; otherwise discovered from robots.txt, then /sitemap.xml)
  index_urls        (optional) HTML listing pages whose links are harvested instead of / in
                    addition to the sitemap (set sitemap_url: none to skip the sitemap)
  job_url_pattern   regex a job URL must match
  max_new_pages     cap on job pages fetched per run (default 50)
  url_prefix        (optional) only keep URLs starting with this
  title_strip       (optional) regex removed from fallback titles, e.g. " - Marex Careers$"
  location_regex    (optional) regex with one group applied to the meta description

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
_SITEMAP_RE = re.compile(r"^\s*sitemap:\s*(\S+)", re.I | re.M)


class SitemapAdapter(Adapter):
    name = "sitemap"

    def __init__(self, company, http=None):
        super().__init__(company, http)
        self.pattern = re.compile(self.config["job_url_pattern"], re.I)
        self.max_new = int(self.config.get("max_new_pages", 50))
        self.prefix = self.config.get("url_prefix") or ""
        self.index_urls: list[str] = list(self.config.get("index_urls") or [])
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

    def _harvest_index(self, url: str, out: set[str]) -> None:
        resp = self._http().get(url)
        if resp.status_code != 200:
            raise SourceError(
                f"index page: HTTP {resp.status_code} from {url}", company=self.company.name
            )
        tree = HTMLParser(resp.text)
        for a in tree.css("a[href]"):
            href = urljoin(url, a.attributes.get("href", "")).split("#")[0]
            if self.pattern.search(href) and href.startswith(self.prefix):
                out.add(href)

    def job_urls(self) -> set[str]:
        urls: set[str] = set()
        seen: set[str] = set()
        for sm in self._sitemap_urls():
            self._collect(sm, seen, urls)
        for page in self.index_urls:
            self._harvest_index(page, urls)
        return urls

    def _parse_page(self, html: str, url: str) -> RawPosting | None:
        if extract_job_postings(html):
            return parse_job_page(html, url)
        return parse_fallback(html, url, self.title_strip, self.location_regex)

    # ---- fetch ------------------------------------------------------------
    def fetch(self) -> list[RawPosting]:
        urls = self.job_urls()
        if not urls:
            raise SourceError(
                "sitemap: no job URLs matched job_url_pattern", company=self.company.name
            )
        known = self.known_postings
        out: list[RawPosting] = [known[u] for u in urls if u in known]
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
                out.append(posting)
        return out

    def parse(self, payload: Any) -> list[RawPosting]:
        """Fixture format: {"urls": [...], "pages": {url: html}}."""
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
