"""Adapter interface + a shared, polite HTTP client."""

from __future__ import annotations

import logging
import random
import threading
import time
from abc import ABC, abstractmethod
from datetime import UTC, datetime
from typing import Any
from urllib.parse import urlsplit

import httpx

from radar.models import Company, RawPosting

log = logging.getLogger(__name__)

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 DeskRadar/0.1"
)
TIMEOUT = 20.0
MAX_RETRIES = 3
MIN_INTERVAL_PER_HOST = 1.0  # seconds


class SourceError(Exception):
    """Any failure fetching or parsing a source. The runner logs it and moves on."""

    def __init__(self, message: str, *, company: str = "", retryable: bool = False):
        super().__init__(message)
        self.company = company
        self.retryable = retryable


class _HostThrottle:
    """At most one request per MIN_INTERVAL_PER_HOST per host, process-wide and thread-safe.

    Each caller reserves the next free slot for its host under the lock, then sleeps outside
    the lock, so different hosts never wait for each other."""

    def __init__(self, interval: float = MIN_INTERVAL_PER_HOST) -> None:
        self.interval = interval
        self._lock = threading.Lock()
        self._next_free: dict[str, float] = {}

    @staticmethod
    def bucket(url: str) -> str:
        """Hosts that share one WAF are paced together (all Workday tenants, for instance)."""
        host = urlsplit(url).netloc
        for platform in ("myworkdayjobs.com", "successfactors.eu", "successfactors.com"):
            if host.endswith(platform):
                return platform
        return host

    def wait(self, url: str) -> None:
        host = self.bucket(url)
        with self._lock:
            now = time.monotonic()
            slot = max(now, self._next_free.get(host, 0.0))
            self._next_free[host] = slot + self.interval
        delay = slot - time.monotonic()
        if delay > 0:
            time.sleep(delay)


_throttle = _HostThrottle()


class Http:
    """Thin wrapper around httpx with throttling, retries on 429/5xx and typed errors."""

    def __init__(self, headers: dict[str, str] | None = None, timeout: float = TIMEOUT):
        h = {"User-Agent": USER_AGENT, "Accept-Language": "en-GB,en;q=0.9"}
        if headers:
            h.update(headers)
        self.client = httpx.Client(headers=h, timeout=timeout, follow_redirects=True)

    def close(self) -> None:
        self.client.close()

    def __enter__(self) -> Http:
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()

    def request(self, method: str, url: str, **kw: Any) -> httpx.Response:
        last_exc: Exception | None = None
        for attempt in range(MAX_RETRIES + 1):
            _throttle.wait(url)
            try:
                resp = self.client.request(method, url, **kw)
            except httpx.HTTPError as e:
                last_exc = e
                log.warning("%s %s failed (%s), attempt %d", method, url, e, attempt + 1)
            else:
                if resp.status_code == 429 or 500 <= resp.status_code < 600:
                    last_exc = SourceError(f"HTTP {resp.status_code} from {url}", retryable=True)
                    log.warning(
                        "%s %s -> %d, attempt %d", method, url, resp.status_code, attempt + 1
                    )
                else:
                    return resp
            if attempt < MAX_RETRIES:
                time.sleep((2**attempt) + random.uniform(0, 0.5))
        raise SourceError(f"{method} {url}: giving up after {MAX_RETRIES + 1} attempts: {last_exc}")

    def get(self, url: str, **kw: Any) -> httpx.Response:
        return self.request("GET", url, **kw)

    def post(self, url: str, **kw: Any) -> httpx.Response:
        return self.request("POST", url, **kw)

    def get_json(self, url: str, **kw: Any) -> Any:
        resp = self.get(url, **kw)
        if resp.status_code != 200:
            raise SourceError(f"HTTP {resp.status_code} from {url}: {_snippet(resp)}")
        try:
            return resp.json()
        except ValueError as e:
            raise SourceError(
                f"non-JSON body from {url} (HTTP {resp.status_code}, "
                f"{resp.headers.get('content-type', '?')}): {_snippet(resp)}",
                retryable=True,
            ) from e

    def post_json(self, url: str, **kw: Any) -> Any:
        resp = self.post(url, **kw)
        if resp.status_code != 200:
            raise SourceError(f"HTTP {resp.status_code} from {url}: {_snippet(resp)}")
        try:
            return resp.json()
        except ValueError as e:
            raise SourceError(
                f"non-JSON body from {url} (HTTP {resp.status_code}, "
                f"{resp.headers.get('content-type', '?')}): {_snippet(resp)}",
                retryable=True,
            ) from e


def _snippet(resp: httpx.Response, n: int = 160) -> str:
    text = " ".join((resp.text or "").split())
    import re as _re

    m = _re.search(r"<title>(.*?)</title>", text, _re.I)
    return (f"title={m.group(1)[:80]!r} " if m else "") + f"body={text[:n]!r}"


class Adapter(ABC):
    name: str = "base"

    def __init__(self, company: Company, http: Http | None = None):
        self.company = company
        self.config = company.config
        self.http = http
        # url -> RawPosting already stored for this company (filled by the runner; used by
        # adapters that must avoid re-fetching pages they have seen, e.g. sitemap).
        self.known_postings: dict[str, RawPosting] = {}

    @abstractmethod
    def fetch(self) -> list[RawPosting]:
        """Fetch all current postings from the live source. Raise SourceError on failure."""

    @abstractmethod
    def parse(self, payload: Any) -> list[RawPosting]:
        """Parse one recorded payload (used by tests and --dry-run)."""

    def _http(self) -> Http:
        if self.http is None:
            self.http = Http()
        return self.http


def parse_dt(value: Any) -> datetime | None:
    """Best-effort ISO-8601 / epoch-ms parser returning tz-aware UTC datetimes."""
    if value in (None, ""):
        return None
    if isinstance(value, (int, float)):
        if value > 1e11:  # epoch ms
            value = value / 1000
        return datetime.fromtimestamp(value, tz=UTC)
    s = str(value).strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        for fmt in (
            "%Y-%m-%d",
            "%Y/%m/%d",
            "%d/%m/%Y",
            "%m/%d/%Y",
            "%b %d, %Y",
            "%d %b %Y",
            "%d.%m.%Y",
        ):
            try:
                dt = datetime.strptime(s, fmt)
                break
            except ValueError:
                continue
        else:
            return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)
