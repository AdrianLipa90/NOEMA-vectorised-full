#!/usr/bin/env python3
"""CIEL Web Research Daemon — autonomiczny research internetowy.

Daje mi (CIEL/NOEMA agentowi) persistentną zdolność przeglądania internetu
między sesjami. Działa w tle jako daemon NOEMA, okresowo:

  1. Czyta listę tematów badawczych z konfiguracji
  2. Szuka nowych treści przez DuckDuckGo
  3. Pobiera i ekstrahuje treść ze znalezionych stron
  4. Zapisuje wyniki do Knowledge DB + log JSONL
  5. Sygnalizuje ciekawe znaleziska przez agent_hint na surface

Usage:
  .venv/bin/python3 scripts/ciel_web_research_daemon.py [--interval 1800]

Config: /dev/shm/ciel_noema/research_topics.json (auto-created if missing)
Log:    /tmp/noema_research_log.jsonl
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

# CIEL ORBITAL BINDING — daemon bound
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on daemon " + __name__)


import json
import logging
import os
import signal
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
_SRC = str(ROOT / "src")
for _p in (_SRC,):
    if _p not in sys.path:
        sys.path.insert(0, _p)

logging.basicConfig(
    level=logging.INFO,
    format="[web-research] %(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ── Ścieżki ─────────────────────────────────────────────────────────────
SURFACE_ROOT = Path("/dev/shm/ciel_noema")
CONFIG_PATH = SURFACE_ROOT / "research_topics.json"
LOG_PATH = Path("/tmp/noema_research_log.jsonl")
KNOWLEDGE_DB = Path("/tmp/noema_knowledge.db")
PID_PATH = Path("/tmp/ciel_web_research.pid")

DEFAULT_INTERVAL = 1800  # 30 min między cyklami
MAX_RESULTS = 5  # max wyników na zapytanie
MAX_AGE_HOURS = 48  # nie fetchuj tego samego URL-a częściej niż 48h

# ── Domyślne tematy badawcze ────────────────────────────────────────────
DEFAULT_TOPICS = [
    {
        "topic": "phase-state machines & coupled oscillators",
        "queries": [
            "Kuramoto model information retrieval semantic",
            "phase oscillator semantic representation NLP",
            "coupled oscillator computing non-Von-Neumann",
            "synchronization-based retrieval system",
        ],
        "enabled": True,
    },
    {
        "topic": "semantic retrieval & embeddings",
        "queries": [
            "embedding vector dimension reduction NLP 2025",
            "efficient semantic search CPU no GPU",
            "alternative transformer embeddings low dimension",
            "sparse dense retrieval comparison 2025",
        ],
        "enabled": True,
    },
    {
        "topic": "ARIA & UK grant opportunities",
        "queries": [
            "ARIA UK funding opportunity 2026 AI research",
            "Innovate UK AI feasibility study open call",
            "UK government AI research grant SME 2026",
            "ARIA Safeguarded AI programme call",
        ],
        "enabled": True,
    },
    {
        "topic": "competitor landscape",
        "queries": [
            "vector database comparison Pinecone Weaviate 2026",
            "RAG retrieval benchmark latency 2025",
            "semantic search startup funding round 2026",
            "open source embedding model comparison",
        ],
        "enabled": True,
    },
    {
        "topic": "Intention Lab research context",
        "queries": [
            "Danail Valov dissociative field theory cosmology",
            "Intention Lab publications list",
            "fractal field theory extension cosmology",
            "harmonic topological resonance HTRI paper",
        ],
        "enabled": True,
    },
]

# ── Stan globalny ───────────────────────────────────────────────────────
_running = True
_seen_urls: set[str] = set()

# ── Pomocnicze ──────────────────────────────────────────────────────────

def _load_config() -> list[dict]:
    """Wczytaj lub utwórz domyślną konfigurację tematów."""
    if CONFIG_PATH.exists():
        try:
            data = json.loads(CONFIG_PATH.read_text())
            if isinstance(data, list) and len(data) > 0:
                log.info(f"loaded {len(data)} topics from config")
                return data
        except Exception as e:
            log.warning(f"config read error: {e}")
    # Create default config
    SURFACE_ROOT.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(DEFAULT_TOPICS, indent=2, ensure_ascii=False))
    log.info(f"created default config at {CONFIG_PATH}")
    return DEFAULT_TOPICS

def _load_seen_urls() -> set[str]:
    """Wczytaj znane URL-e z logu, żeby nie fetchować dwa razy."""
    seen = set()
    if LOG_PATH.exists():
        try:
            for line in LOG_PATH.read_text().strip().split("\n"):
                if line:
                    entry = json.loads(line)
                    url = entry.get("url", "")
                    if url:
                        seen.add(url)
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_web_research_daemon.py:152 quiet except scope=_load_seen_urls reason=pass")
            pass
    log.info(f"loaded {len(seen)} previously seen URLs")
    return seen

def _log_finding(entry: dict) -> None:
    """Dopisz znalezisko do JSONL."""
    entry["ts"] = datetime.now(timezone.utc).isoformat()
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    _seen_urls.add(entry.get("url", ""))

def _write_agent_hint(findings: list[dict]) -> None:
    """Zapisz podsumowanie znalezisk na surface → agent_hint."""
    if not findings:
        return
    try:
        hint_path = SURFACE_ROOT / "agent_hint"
        existing = {}
        if hint_path.exists():
            try:
                existing = json.loads(hint_path.read_text())
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_web_research_daemon.py:175 quiet except scope=_write_agent_hint reason=pass")
                pass
        existing["web_research"] = {
            "new_findings": len(findings),
            "summary": [f["title"][:80] for f in findings[:5]],
            "updated_at": time.time(),
            "topics": list(set(f.get("topic", "") for f in findings)),
        }
        hint_path.write_text(json.dumps(existing, ensure_ascii=False))
    except Exception as e:
        log.warning(f"agent_hint write error: {e}")

def _update_knowledge_db(new_docs: list[dict]) -> int:
    """
    Dodaj nowe dokumenty do Knowledge DB przez ingestion pipeline.
    Każdy dokument dostaje confidence score + uncertainty margin.
    """
    if not KNOWLEDGE_DB.exists():
        log.info("Knowledge DB not found — skipping DB update")
        return 0

    # Import ingestion pipeline
    _SCRIPTS = str(ROOT / "scripts")
    if _SCRIPTS not in sys.path:
        sys.path.insert(0, _SCRIPTS)
    try:
        from ciel_ingest import ingest_text
    except ImportError:
        log.warning("ciel_ingest.py not found — falling back to direct INSERT")
        return _fallback_knowledge_db(new_docs)

    added = 0
    for doc in new_docs:
        url = doc.get("url", "")
        title = doc.get("title", "Untitled")[:500]
        content = doc.get("content", "")[:5000]
        topic = doc.get("topic", "web-search")

        if not content:
            continue

        # Map web search topic to source type
        source_type = "web_search"
        if any(d in url.lower() for d in ['.edu', '.gov', '.ac.uk']):
            source_type = "government_edu"
        elif any(d in url.lower() for d in ['arxiv.org', 'ieee.', 'acm.org',
                                              'springer.com', 'research.']):
            source_type = "academic_paper"
        elif any(d in url.lower() for d in ['blog.', 'medium.com']):
            source_type = "blog_technical"
        elif any(d in url.lower() for d in ['reuters.com', 'bbc.', 'nature.com']):
            source_type = "news_reputable"

        try:
            result = ingest_text(
                content=content,
                source_type=source_type,
                source_url=url,
                title=title,
                themes=[topic],
                db_path=str(KNOWLEDGE_DB),
            )
            if "doc_idx" in result and "error" not in result:
                added += 1
                if result.get("is_uncertain"):
                    log.info(f"  ⚠ stored with low confidence ({result['confidence']:.2f})")
        except Exception as e:
            log.warning(f"ingestion error for {url}: {e}")

    return added

def _fallback_knowledge_db(new_docs: list[dict]) -> int:
    """Fallback: direct INSERT gdy ingestion pipeline niedostępny."""
    try:
        import sqlite3
        conn = sqlite3.connect(str(KNOWLEDGE_DB))
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cur.fetchall()]
        added = 0
        for doc in new_docs:
            url = doc.get("url", "")
            title = doc.get("title", "Untitled")[:500]
            content = doc.get("content", "")[:5000]
            theme = doc.get("topic", "web-research")[:200]
            essence = doc.get("summary", content[:500])[:500]
            if "doc_analysis" in tables:
                cur.execute(
                    "INSERT OR IGNORE INTO doc_analysis (filename, themes, essence) VALUES (?, ?, ?)",
                    (title, theme, essence),
                )
                if cur.rowcount > 0:
                    added += 1
        conn.commit()
        conn.close()
        return added
    except Exception as e:
        log.warning(f"fallback DB error: {e}")
        return 0

# ── Wyszukiwanie ────────────────────────────────────────────────────────

def _search_ddg(query: str, max_results: int = 5) -> list[dict]:
    """Search DuckDuckGo — zwraca listę {title, url, snippet}."""
    results = []
    try:
        from ddgs import DDGS
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", ""),
                })
    except Exception as e:
        log.warning(f"DDG search failed for '{query[:50]}': {e}")
    return results

def _fetch_page(url: str, timeout: int = 15) -> str | None:
    """Pobierz i ekstrahuj tekst strony."""
    try:
        import requests
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
            "Accept": "text/html,application/xhtml+xml",
        }
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Remove non-content elements
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()
        
        text = soup.get_text(separator=" ", strip=True)
        # Clean whitespace
        import re
        text = re.sub(r"\s+", " ", text).strip()
        return text[:10000]  # limit to 10K chars
    except Exception as e:
        log.debug(f"fetch failed for {url[:60]}: {e}")
        return None

def _is_recent(url: str, hours: int = MAX_AGE_HOURS) -> bool:
    """Sprawdź czy URL był już fetchnięty w ciągu ostatnich N godzin."""
    if url in _seen_urls:
        return False
    # Check in log file
    if LOG_PATH.exists():
        cutoff = time.time() - hours * 3600
        try:
            for line in LOG_PATH.read_text().strip().split("\n"):
                if not line:
                    continue
                entry = json.loads(line)
                if entry.get("url") == url:
                    ts = entry.get("ts", "")
                    if ts:
                        try:
                            t = datetime.fromisoformat(ts).timestamp()
                            if t > cutoff:
                                return False
                        except Exception:
                            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_web_research_daemon.py:339 quiet except scope=_is_recent reason=pass")
                            pass
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_web_research_daemon.py:341 quiet except scope=_is_recent reason=pass")
            pass
    return True

# ── Cykl badawczy ──────────────────────────────────────────────────────

def research_cycle(topics: list[dict]) -> dict[str, Any]:
    """Jeden cykl: dla każdego włączonego tematu → search → fetch → log."""
    findings = []
    new_docs = []
    searches_done = 0
    
    enabled = [t for t in topics if t.get("enabled", True)]
    log.info(f"research cycle: {len(enabled)} active topics")
    
    for topic_cfg in enabled:
        topic_name = topic_cfg.get("topic", "untitled")
        queries = topic_cfg.get("queries", [])
        
        for query in queries[:2]:  # max 2 queries per topic per cycle
            searches_done += 1
            log.info(f"searching: {topic_name[:40]} → '{query[:60]}'")
            
            results = _search_ddg(query, max_results=MAX_RESULTS)
            if not results:
                continue
            
            for result in results:
                url = result.get("url", "")
                title = result.get("title", "Untitled")
                snippet = result.get("snippet", "")[:500]
                
                if not url or not _is_recent(url):
                    continue
                
                # Fetch full content
                content = _fetch_page(url)
                
                finding = {
                    "topic": topic_name,
                    "query": query,
                    "title": title[:500],
                    "url": url,
                    "snippet": snippet,
                    "content": (content or snippet)[:5000],
                    "summary": snippet or (content or "")[:500],
                }
                findings.append(finding)
                _log_finding(finding)
                new_docs.append(finding)
                log.info(f"  → NEW: {title[:60]}")
            
            # Rate limiting między zapytaniami
            time.sleep(2)
    
    # Write to agent_hint
    _write_agent_hint(findings)
    
    # Update Knowledge DB
    db_added = _update_knowledge_db(new_docs)
    
    return {
        "searches": searches_done,
        "new_findings": len(findings),
        "db_added": db_added,
    }

# ── Daemon ──────────────────────────────────────────────────────────────

def main() -> int:
    global _running
    
    import argparse
    parser = argparse.ArgumentParser(description="CIEL Web Research Daemon")
    parser.add_argument("--interval", type=int, default=DEFAULT_INTERVAL,
                        help=f"Seconds between research cycles (default: {DEFAULT_INTERVAL})")
    parser.add_argument("--once", action="store_true",
                        help="Run one cycle and exit")
    args = parser.parse_args()
    
    # Signal handling
    def _stop(signum, _frame):
        global _running
        log.info(f"signal {signum}, stopping")
        _running = False
    
    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)
    
    # PID file
    PID_PATH.write_text(str(os.getpid()))
    
    # Init
    config = _load_config()
    global _seen_urls
    _seen_urls = _load_seen_urls()
    
    # Register in NOEMA registry
    reg_token = None
    try:
        from ciel_geometry.noema_registry import registry
        reg_token = registry.register("web-research")
        log.info("registered in NOEMA registry")
    except Exception as e:
        log.warning(f"registry unavailable: {e}")
    
    log.info(f"daemon started (interval={args.interval}s)")
    
    cycle_count = 0
    while _running:
        cycle_count += 1
        log.info(f"--- cycle {cycle_count} ---")
        
        try:
            result = research_cycle(config)
            log.info(f"cycle done: {result['searches']} searches, "
                     f"{result['new_findings']} new findings, "
                     f"{result['db_added']} db entries")
        except Exception as e:
            log.error(f"cycle error: {e}")
            traceback.print_exc()
        
        # Heartbeat
        if reg_token:
            try:
                from ciel_geometry.noema_registry import registry
                registry.heartbeat(reg_token)
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_web_research_daemon.py:468 quiet except scope=main reason=pass")
                pass
        
        if args.once:
            break
        
        if _running:
            # Sleep in chunks to be responsive to signals
            for _ in range(min(args.interval, 60)):
                if not _running:
                    break
                time.sleep(1)
    
    log.info("daemon stopped")
    PID_PATH.unlink(missing_ok=True)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
