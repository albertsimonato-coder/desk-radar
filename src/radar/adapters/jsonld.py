"""Shared schema.org JobPosting (JSON-LD) parser for employer job pages."""

from __future__ import annotations

import html as htmllib
import json
import re
from typing import Any

from selectolax.lexbor import LexborHTMLParser as HTMLParser

from radar.adapters.base import parse_dt
from radar.models import RawPosting

_TAG = re.compile(r"<[^>]+>")


def _walk(node: Any):
    """Yield every dict in a JSON-LD document (handles lists and @graph)."""
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from _walk(v)
    elif isinstance(node, list):
        for v in node:
            yield from _walk(v)


def _is_job_posting(d: dict) -> bool:
    t = d.get("@type")
    if isinstance(t, list):
        return "JobPosting" in t
    return t == "JobPosting"


def _text(v: Any) -> str:
    if isinstance(v, dict):
        return str(v.get("name") or v.get("value") or v.get("@value") or "")
    if isinstance(v, list):
        return ", ".join(_text(x) for x in v if _text(x))
    return str(v or "")


def _location(job: dict) -> str:
    locs = job.get("jobLocation")
    if not locs:
        if job.get("jobLocationType") == "TELECOMMUTE":
            return "Remote"
        return ""
    if isinstance(locs, dict):
        locs = [locs]
    parts: list[str] = []
    for loc in locs:
        if not isinstance(loc, dict):
            continue
        addr = loc.get("address") or {}
        if isinstance(addr, str):
            parts.append(addr)
            continue
        if not isinstance(addr, dict):
            continue
        bits = [
            _text(addr.get("addressLocality")),
            _text(addr.get("addressRegion")),
            _text(addr.get("addressCountry")),
        ]
        s = ", ".join(b for b in bits if b)
        if not s:
            s = _text(loc.get("name"))
        if s:
            parts.append(s)
    return "; ".join(dict.fromkeys(parts))


def _snippet(desc: Any, n: int = 400) -> str:
    text = htmllib.unescape(_TAG.sub(" ", htmllib.unescape(str(desc or ""))))
    return " ".join(text.split())[:n]


def extract_job_postings(html: str) -> list[dict]:
    tree = HTMLParser(html)
    jobs: list[dict] = []
    for node in tree.css('script[type="application/ld+json"]'):
        raw = node.text(strip=True)
        if not raw:
            continue
        try:
            doc = json.loads(raw)
        except json.JSONDecodeError:
            # Some sites emit trailing commas or comments; try a lenient cleanup once.
            try:
                doc = json.loads(re.sub(r",\s*([}\]])", r"\1", raw))
            except json.JSONDecodeError:
                continue
        jobs.extend(d for d in _walk(doc) if _is_job_posting(d))
    return jobs


def parse_job_page(html: str, url: str) -> RawPosting | None:
    """Return a RawPosting from the page's JSON-LD JobPosting, or a title-only fallback."""
    jobs = extract_job_postings(html)
    if jobs:
        job = jobs[0]
        ident = job.get("identifier")
        if isinstance(ident, dict):
            ext = str(ident.get("value") or ident.get("name") or "")
        else:
            ext = _text(ident) if ident else ""
        return RawPosting(
            external_id=ext or url,
            title=_text(job.get("title")).strip(),
            location_raw=_location(job),
            department=_text(job.get("occupationalCategory") or job.get("industry")),
            posted_at=parse_dt(job.get("datePosted")),
            url=url,
            description_snippet=_snippet(job.get("description")),
            employment_type_raw=_text(job.get("employmentType")),
        )
    return parse_fallback(html, url)


def _meta(tree: HTMLParser, *names: str) -> str:
    for n in names:
        node = tree.css_first(f'meta[property="{n}"]') or tree.css_first(f'meta[name="{n}"]')
        if node and node.attributes.get("content"):
            return node.attributes["content"].strip()
    return ""


def _itemprop(tree: HTMLParser, name: str) -> str:
    node = tree.css_first(f'[itemprop="{name}"]')
    if not node:
        return ""
    return (node.attributes.get("content") or node.text(separator=" ", strip=True) or "").strip()


def parse_fallback(
    html: str, url: str, title_strip: str = "", location_regex: str = ""
) -> RawPosting | None:
    """No JSON-LD: use og:title / <title>, schema.org microdata and the meta description.

    SuccessFactors "career site builder" pages describe themselves as
    "<location> <title>, <postcode>", so the location is what is left of the description
    once the title is removed. `location_regex` (one capture group) overrides that heuristic.
    """
    tree = HTMLParser(html)
    title = (
        _itemprop(tree, "title")
        or _meta(tree, "og:title")
        or (tree.css_first("title").text(strip=True) if tree.css_first("title") else "")
    )
    title = " ".join(title.split())
    if title_strip:
        title = re.sub(title_strip, "", title).strip(" -|:")
    if not title:
        return None
    desc = _meta(tree, "description", "og:description")
    location = _itemprop(tree, "jobLocation") or _itemprop(tree, "addressLocality")
    if not location and desc:
        if location_regex:
            m = re.search(location_regex, desc)
            location = m.group(1).strip() if m else ""
        elif title in desc:
            left = desc.replace(title, " ")
            left = re.sub(r",?\s*\d{4,}\s*$", "", left)  # trailing postcode
            location = left.strip(" ,;-")
    return RawPosting(
        external_id=_itemprop(tree, "identifier") or url,
        title=title,
        location_raw=location,
        posted_at=parse_dt(_itemprop(tree, "datePosted")),
        url=url,
        description_snippet=" ".join(desc.split())[:400],
        employment_type_raw=_itemprop(tree, "employmentType"),
    )
