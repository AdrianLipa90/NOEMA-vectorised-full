from __future__ import annotations

from typing import Any
import re

from duckduckgo_search import DDGS

SEARCH_CACHE: dict[str, list[dict[str, Any]]] = {}


def search(query: str, max_results: int = 5) -> list[dict[str, Any]]:
    """Search the web via DuckDuckGo. Returns list of {title, snippet, url}."""
    clean_q = query.strip()[:300]
    if clean_q in SEARCH_CACHE:
        return SEARCH_CACHE[clean_q][:max_results]

    results: list[dict[str, Any]] = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(clean_q, max_results=max_results):
                results.append({
                    "title": str(r.get("title", "")),
                    "snippet": str(r.get("body", "")),
                    "url": str(r.get("href", "")),
                })
    except Exception:
        return []

    SEARCH_CACHE[clean_q] = results
    return results


__all__ = ["search"]
