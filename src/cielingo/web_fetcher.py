"""CIELingo web fetcher — zero zależności, tylko stdlib.

Używa urllib.request do pobierania stron i RSS.
Wbudowany parser RSS (XML/ETree), fallback do regex dla surowego tekstu.
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import html
import json
import re
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import Any
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


_USER_AGENT = "CIELingo/0.1 (linguistic phase topology; +https://github.com/ciel)"
_TIMEOUT = 15
_MAX_TEXT = 100000
_CACHE: dict[str, tuple[float, Any]] = {}
_CACHE_TTL = 600.0  # 10 min


@dataclass
class FetchResult:
    url: str
    status: int
    text: str
    content_type: str
    elapsed: float
    error: str = ""
    articles: list[dict[str, str]] = field(default_factory=list)


def fetch(url: str, *, timeout: int = _TIMEOUT, cache: bool = True) -> FetchResult:
    now = time.monotonic()
    if cache and url in _CACHE:
        ts, data = _CACHE[url]
        if now - ts < _CACHE_TTL:
            return data

    t0 = time.time()
    try:
        req = Request(url, headers={"User-Agent": _USER_AGENT})
        with urlopen(req, timeout=timeout) as resp:
            status = resp.status
            ctype = (resp.headers.get("Content-Type", "") or "").split(";")[0]
            raw = resp.read(_MAX_TEXT * 4)
            text = raw.decode("utf-8", errors="replace")[:_MAX_TEXT]
        elapsed = time.time() - t0
    except HTTPError as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/cielingo/web_fetcher.py:53 quiet except scope=fetch reason=no_log_no_raise")
        result = FetchResult(url=url, status=e.code, text="", content_type="", elapsed=time.time()-t0, error=str(e))
        return result
    except URLError as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/cielingo/web_fetcher.py:56 quiet except scope=fetch reason=no_log_no_raise")
        result = FetchResult(url=url, status=0, text="", content_type="", elapsed=time.time()-t0, error=str(e))
        return result
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/cielingo/web_fetcher.py:59 quiet except scope=fetch reason=no_log_no_raise")
        result = FetchResult(url=url, status=0, text="", content_type="", elapsed=time.time()-t0, error=str(e))
        return result

    articles: list[dict[str, str]] = []
    if "xml" in ctype or "rss" in ctype or "atom" in ctype:
        articles = _parse_rss(text)

    result = FetchResult(url=url, status=status, text=_strip_html(text), content_type=ctype, elapsed=elapsed, articles=articles)
    if cache:
        _CACHE[url] = (time.monotonic(), result)
    return result


def _parse_rss(xml_text: str) -> list[dict[str, str]]:
    articles = []
    try:
        root = ET.fromstring(xml_text)
        # RSS 2.0
        for item in root.iter("item"):
            title = _clean((item.findtext("title") or ""))
            link = (item.findtext("link") or "")
            desc = _clean((item.findtext("description") or ""))[:500]
            if title:
                articles.append({"title": title, "url": link, "summary": desc, "source": "rss"})
        # Atom
        for entry in root.iter("{http://www.w3.org/2005/Atom}entry"):
            title = _clean((entry.findtext("{http://www.w3.org/2005/Atom}title") or ""))
            link_el = entry.find("{http://www.w3.org/2005/Atom}link")
            link = link_el.get("href", "") if link_el is not None else ""
            summary = _clean((entry.findtext("{http://www.w3.org/2005/Atom}summary") or ""))[:500]
            if title:
                articles.append({"title": title, "url": link, "summary": summary, "source": "atom"})
    except ET.ParseError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/cielingo/web_fetcher.py:92 quiet except scope=_parse_rss reason=pass")
        pass
    return articles


def _strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return html.unescape(text).strip()


def _clean(text: str) -> str:
    return html.unescape(re.sub(r"\s+", " ", text).strip())


# ── News feeds (bez zależności) ────────────────────────────────────────────

RSS_FEEDS: dict[str, str] = {
    "BBC World":      "https://feeds.bbci.co.uk/news/world/rss.xml",
    "Reuters":        "https://feeds.reuters.com/reuters/topNews",
    "Al Jazeera":     "https://www.aljazeera.com/xml/rss/all.xml",
    "RMF24":          "https://www.rmf24.pl/feed",
    "PAP Nauka":      "https://www.pap.pl/rss/nauka.xml",
}


def fetch_news(*, sources: list[str] | None = None, max_articles: int = 5) -> list[dict[str, str]]:
    articles: list[dict[str, str]] = []
    feed_urls = {name: url for name, url in RSS_FEEDS.items() if sources is None or name in sources}
    for name, url in feed_urls.items():
        result = fetch(url, timeout=10)
        if result.articles:
            articles.extend(result.articles[:3])
        if len(articles) >= max_articles:
            break
    return articles[:max_articles]


__all__ = ["fetch", "fetch_news", "FetchResult", "RSS_FEEDS"]
