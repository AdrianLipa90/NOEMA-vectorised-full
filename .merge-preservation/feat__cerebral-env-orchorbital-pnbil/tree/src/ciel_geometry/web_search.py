"""Web search for CIEL response path.

Używa niewymagających klucza API: Wikipedia (PL/EN/DE/FR/ES), DuckDuckGo,
arXiv, Semantic Scholar — bez JS-gate ani captcha. Każde źródło może
rzucić wyjątek; agregator sygnalizuje przez phase_signal_exception.
"""
from __future__ import annotations

import html
import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Any

SEARCH_CACHE: dict[str, list[dict[str, Any]]] = {}

_CAPTCHA_SIGNALS = [
    "javascript is disabled", "enable javascript", "verify you are human",
    "verify that you're not a robot", "checking your browser", "ddos-guard",
    "cloudflare", "just a moment", "please wait while we check", "%pdf-",
    "access denied", "security check",
]


def _is_junk(text: str) -> bool:
    if not text or len(text) < 50:
        return True
    s = text[:300].lower()
    return any(sig in s for sig in _CAPTCHA_SIGNALS)


def _wikipedia_search(query: str, n: int = 3, lang: str = "en") -> list[dict[str, Any]]:
    params = urllib.parse.urlencode({
        "action": "opensearch", "search": query, "limit": n,
        "namespace": 0, "format": "json",
    })
    req = urllib.request.Request(
        f"https://{lang}.wikipedia.org/w/api.php?{params}",
        headers={"User-Agent": "NOEMA-ciel/1.0 (academic)"},
    )
    with urllib.request.urlopen(req, timeout=6) as r:
        data = json.loads(r.read())
    titles, descs, urls = data[1], data[2], data[3]
    snippet_clean = lambda s: not any(sig in s.lower() for sig in _CAPTCHA_SIGNALS)
    return [{"title": t, "snippet": d, "url": u}
            for t, d, u in zip(titles, descs, urls) if t and snippet_clean(d)]


def _arxiv_search(query: str, n: int = 2) -> list[dict[str, Any]]:
    params = urllib.parse.urlencode({
        "search_query": f"all:{query}", "start": 0,
        "max_results": n, "sortBy": "relevance",
    })
    req = urllib.request.Request(
        f"https://export.arxiv.org/api/query?{params}",
        headers={"User-Agent": "NOEMA-ciel/1.0"},
    )
    with urllib.request.urlopen(req, timeout=8) as r:
        root = ET.fromstring(r.read())
    ns = {"a": "http://www.w3.org/2005/Atom"}
    results = []
    for entry in root.findall("a:entry", ns):
        t = entry.find("a:title", ns)
        s = entry.find("a:summary", ns)
        u = entry.find("a:id", ns)
        if t is None or u is None:
            continue
        snippet = (s.text or "").strip()[:400] if s is not None else ""
        if not _is_junk(snippet + (t.text or "")):
            results.append({"title": (t.text or "").strip(), "snippet": snippet, "url": (u.text or "").strip()})
    return results


def _duckduckgo_search(query: str) -> list[dict[str, Any]]:
    """DuckDuckGo Instant Answer API — daje streszczenie Wikipedia + powiązane tematy."""
    params = urllib.parse.urlencode({
        "q": query, "format": "json", "no_html": 1, "skip_disambig": 1,
    })
    req = urllib.request.Request(
        f"https://api.duckduckgo.com/?{params}",
        headers={"User-Agent": "NOEMA-ciel/1.0"},
    )
    with urllib.request.urlopen(req, timeout=8) as r:
        data = json.loads(r.read())
    results = []
    # Główny abstract (z Wikipedii)
    abstract = data.get("AbstractText", "").strip()
    source = data.get("AbstractSource", "")
    url = data.get("AbstractURL", "")
    if abstract and source:
        results.append({"title": f"[{source}] {data.get('Heading','')}", "snippet": abstract[:500], "url": url})
    # Powiązane tematy
    for topic in data.get("RelatedTopics", []):
        if "Text" in topic:
            text = html.unescape(topic["Text"]).strip()
            url2 = topic.get("FirstURL", "")
            title_part = text.split(" - ")[0] if " - " in text else text
            snippet_part = text
            results.append({"title": title_part, "snippet": snippet_part[:400], "url": url2})
        elif "Topics" in topic:
            for sub in topic["Topics"]:
                stext = html.unescape(sub.get("Text", "")).strip()
                sfirst = sub.get("FirstURL", "")
                if stext:
                    stitle = stext.split(" - ")[0] if " - " in stext else stext
                    results.append({"title": stitle, "snippet": stext[:400], "url": sfirst})
    # Wyniki (ogólne)
    for result in data.get("Results", []):
        rtext = html.unescape(result.get("Text", "")).strip()
        rurl = result.get("FirstURL", "")
        if rtext:
            results.append({"title": rtext.split(" - ")[0], "snippet": rtext[:400], "url": rurl})
    return results


def _wikipedia_summary_search(query: str, lang: str = "pl") -> list[dict[str, Any]]:
    """Wikipedia summary API — pełny akapit ze strony, nie tylko opensearch.

    Jeśli direct-title nie znajdzie strony (missing), próbuje opensearch
    żeby zgadnąć poprawny tytuł, potem ponawia summary.
    """
    params = urllib.parse.urlencode({
        "action": "query", "format": "json", "prop": "extracts",
        "exintro": 1, "explaintext": 1, "exchars": 500,
        "titles": query, "redirects": 1,
    })
    req = urllib.request.Request(
        f"https://{lang}.wikipedia.org/w/api.php?{params}",
        headers={"User-Agent": "NOEMA-ciel/1.0 (academic)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=6) as r:
            data = json.loads(r.read())
    except Exception:
        return []
    pages = data.get("query", {}).get("pages", {})
    results = []
    found_missing = False
    for page_id, page in pages.items():
        if page_id == "-1":
            found_missing = True
            continue
        title = page.get("title", "")
        extract = page.get("extract", "").strip()
        if title and extract:
            results.append({
                "title": title,
                "snippet": extract[:500],
                "url": f"https://{lang}.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}",
            })
    if found_missing and not results:
        # Fallback: opensearch → znajdź pierwszy pasujący tytuł → summary
        fallback = _wikipedia_search(query, n=3, lang=lang)
        for entry in fallback:
            title = entry.get("title", "")
            if title:
                deeper = _wikipedia_summary_search(title, lang=lang)
                if deeper:
                    return deeper
    return results


def _semantic_scholar_search(query: str, n: int = 2) -> list[dict[str, Any]]:
    params = urllib.parse.urlencode({"query": query, "limit": n, "fields": "title,abstract,url"})
    req = urllib.request.Request(
        f"https://api.semanticscholar.org/graph/v1/paper/search?{params}",
        headers={"User-Agent": "NOEMA-ciel/1.0"},
    )
    with urllib.request.urlopen(req, timeout=6) as r:
        data = json.loads(r.read())
    results = []
    for p in data.get("data", []):
        title = p.get("title", "")
        snippet = (p.get("abstract") or "")[:400]
        url = p.get("url") or f"https://www.semanticscholar.org/paper/{p.get('paperId','')}"
        if not _is_junk(snippet + title):
            results.append({"title": title, "snippet": snippet, "url": url})
    return results


def search(query: str, max_results: int = 7) -> list[dict[str, Any]]:
    """Agregator wielu źródeł — bez captcha, bez API keys.

    Strategia:
    1. DuckDuckGo (1 call, bogaty JSON z Wikipedia abstract + related topics)
    2. Jeśli DDG nie dał wyników → Wikipedia summary (PL, potem EN)
    3. Jeśli nadal pusto → Wikipedia opensearch (PL, EN, DE, FR, ES)
    4. Zawsze: arXiv + Semantic Scholar

    Ogranicza liczbę zapytań do Wikipedii (rate limit ~200/min, ale
    bezpieczniej <5/sesję).
    """
    clean_q = query.strip()[:300]
    if clean_q in SEARCH_CACHE:
        return SEARCH_CACHE[clean_q][:max_results]

    import time as _time
    from ciel_geometry.phasenav_exception_bridge import phase_signal_exception

    results: list[dict[str, Any]] = []

    # 1. DuckDuckGo — główne źródło
    try:
        results += _duckduckgo_search(clean_q)
    except Exception as e:
        phase_signal_exception(f"web_search.search.duckduckgo:query={clean_q!r}", e, operator_id="SOURCE")

    # 2. Wikipedia summary — tylko jeśli DDG nie dał wyników
    if not results:
        for lang in ("pl", "en"):
            try:
                results += _wikipedia_summary_search(clean_q, lang=lang)
                if results:
                    break
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    _time.sleep(2)
                phase_signal_exception(f"web_search.search.wikipedia_summary.{lang}:query={clean_q!r}", e, operator_id="SOURCE")
            except Exception as e:
                phase_signal_exception(f"web_search.search.wikipedia_summary.{lang}:query={clean_q!r}", e, operator_id="SOURCE")

    # 3. Wikipedia opensearch — tylko gdy summary nie dało wyników
    if not results:
        for lang in ("pl", "en", "de", "fr", "es"):
            try:
                results += _wikipedia_search(clean_q, n=3, lang=lang)
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    _time.sleep(2)
                phase_signal_exception(f"web_search.search.wikipedia_opensearch.{lang}:query={clean_q!r}", e, operator_id="SOURCE")
            except Exception as e:
                phase_signal_exception(f"web_search.search.wikipedia_opensearch.{lang}:query={clean_q!r}", e, operator_id="SOURCE")

    # 4. Źródła akademickie (zawsze)
    for name, fn in [
        ("arxiv",            lambda: _arxiv_search(clean_q, n=2)),
        ("semantic_scholar", lambda: _semantic_scholar_search(clean_q, n=2)),
    ]:
        try:
            results += fn()
        except Exception as e:
            phase_signal_exception(f"web_search.search.{name}:query={clean_q!r}", e, operator_id="SOURCE")

    # Deduplikuj (pierwsze wystąpienie wygrywa)
    seen: set[str] = set()
    unique = []
    for r in results:
        u = r.get("url", "")
        if u and u not in seen:
            seen.add(u)
            unique.append(r)

    unique = unique[:max_results]
    SEARCH_CACHE[clean_q] = unique
    return unique


__all__ = ["search"]
