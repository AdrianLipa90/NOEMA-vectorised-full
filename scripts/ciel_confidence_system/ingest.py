#!/usr/bin/env python3
"""
ciel_ingest.py — Data ingestion pipeline z confidence scoringiem.

Każda informacja przechodzi przez:
  1. Parse — wyodrębnij znaczące fragmenty
  2. Score — oceń pewność (source, cross-ref, recency, consistency)
  3. Store — zapisz do Knowledge DB z confidence_score
  4. Flag — jeśli pewność < 60%, dodaj do uncertainty_log

Uruchom:
  python3 scripts/ciel_ingest.py --source academic_paper --url "..." --title "..." --content "..."
  python3 scripts/ciel_ingest.py --source web_search --file /tmp/finding.txt
  python3 scripts/ciel_ingest.py --source user_provided --content "fakt do zapamiętania"

Wymaga: ciel_confidence.py (confidence scoring engine)
"""
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import math
import sqlite3
import json
import sys
import os
import re
import pathlib
import logging
from datetime import datetime, timezone
from typing import Optional

logging.basicConfig(level=logging.INFO, format="[ingest] %(message)s")
log = logging.getLogger("ingest")

# Import confidence engine
from .engine import score_confidence, SOURCE_WEIGHTS

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))
from ciel_geometry.paths import P

# Was hardcoded /tmp/noema_knowledge.db (tmpfs, wiped on reboot) — fixed 2026-07-08.
DEFAULT_DB = pathlib.Path(P.DB.KNOWLEDGE)


def extract_fragments(text: str, max_length: int = 2000) -> list[str]:
    """
    Split text into meaningful fragments for individual scoring.
    Uses sentence boundaries + paragraph breaks.
    """
    # Split into paragraphs first
    paragraphs = re.split(r'\n\s*\n', text.strip())
    fragments = []

    for para in paragraphs:
        para = para.strip()
        if not para or len(para) < 20:
            continue

        if len(para) <= max_length:
            fragments.append(para)
        else:
            # Split long paragraph into sentences
            sentences = re.split(r'(?<=[.!?])\s+', para)
            buffer = ""
            for sent in sentences:
                if len(buffer) + len(sent) < max_length:
                    buffer += " " + sent if buffer else sent
                else:
                    if buffer:
                        fragments.append(buffer)
                    buffer = sent
            if buffer:
                fragments.append(buffer)

    return fragments


def guess_source_type(url: str = "", filename: str = "") -> str:
    """Guess source type from URL or filename."""
    if not url and not filename:
        return "user_provided"

    check_str = (url + " " + filename).lower()

    if any(d in check_str for d in ['.edu', '.gov', '.ac.uk']):
        return "government_edu"
    if any(d in check_str for d in ['arxiv.org', '.pdf', 'research.', 'ieee.',
                                     'acm.org', 'springer.com', 'elsevier.com']):
        return "academic_paper"
    if any(d in check_str for d in ['docs.', 'documentation.', 'spec.',
                                     'developer.', 'wiki.']):
        return "technical_doc"
    if any(d in check_str for d in ['reuters.com', 'bbc.', 'nature.com',
                                     'science.org', 'ap.org']):
        return "news_reputable"
    if any(d in check_str for d in ['blog.', 'medium.com', 'substack.com',
                                     'wordpress.com']):
        return "blog_technical"
    return "web_search"


def ingest_text(
    content: str,
    source_type: str = "unknown",
    source_url: str = "",
    title: str = "",
    themes: Optional[list[str]] = None,
    db_path: str = str(DEFAULT_DB),
    autocommit: bool = True,
) -> dict:
    """
    Ingest a piece of text into Knowledge DB with confidence scoring.

    Returns dict with: doc_idx, confidence, is_uncertain, fragments_count, uncertainty_logged
    """
    if not content.strip():
        return {"error": "empty content"}

    db = sqlite3.connect(db_path, timeout=5)
    db.execute("PRAGMA journal_mode=WAL")

    try:
        # 1. Extract fragments
        fragments = extract_fragments(content)
        if not fragments:
            fragments = [content[:2000]]

        # 2. Score overall confidence (use full text for cross-ref, first fragment for others)
        result = score_confidence(
            content[:3000],
            source_type=source_type,
            source_url=source_url,
            db=db,
        )

        # 3. Get next idx
        cur = db.execute("SELECT COALESCE(MAX(idx), -1) FROM doc_analysis")
        next_idx = cur.fetchone()[0] + 1

        # 4. Store in doc_analysis
        essence = fragments[0][:500] if fragments else content[:500]
        themes_json = json.dumps(themes or [guess_source_type(source_url)],
                                 ensure_ascii=False)
        now_iso = datetime.now(timezone.utc).isoformat()

        db.execute("""
            INSERT INTO doc_analysis
                (idx, filename, themes, affect, anchors, essence, hunch,
                 full_text_len, status,
                 confidence, source_type, source_url, source_reliability,
                 cross_ref_count, recency_days, consistency_score,
                 is_uncertain, ingested_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            next_idx,
            title or f"ingested_{next_idx}",
            themes_json,
            "",
            source_url,
            essence,
            "",  # hunch
            len(content),
            "ingested",
            result.overall,
            source_type,
            source_url,
            result.source_reliability,
            0,  # cross_ref_count will be updated if we recompute
            0,  # recency_days
            result.consistency_score,
            1 if result.is_uncertain else 0,
            now_iso,
        ))

        # 5. Store in confidence_scores
        db.execute("""
            INSERT INTO confidence_scores
                (doc_idx, source_reliability, cross_ref_score, recency_score,
                 consistency_score, self_consistency, overall)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            next_idx,
            result.source_reliability,
            result.cross_ref_score,
            result.recency_score,
            result.consistency_score,
            result.self_consistency,
            result.overall,
        ))

        # 6. Log uncertainty if needed
        uncertainty_logged = False
        if result.is_uncertain:
            db.execute("""
                INSERT INTO uncertainty_log
                    (doc_idx, confidence_score, reason, details)
                VALUES (?, ?, ?, ?)
            """, (
                next_idx,
                result.overall,
                f"low confidence ({result.overall:.2f}) — {source_type}",
                result.details,
            ))
            uncertainty_logged = True
            log.info(f"  ⚠ uncertainty logged for idx={next_idx} (confidence={result.overall:.2f})")

        # 7. Update term_index (basic TF-IDF)
        _update_term_index(db, next_idx, content)

        if autocommit:
            db.commit()

        log.info(f"  → ingested idx={next_idx} confidence={result.overall:.2f} "
                 f"uncertain={result.is_uncertain} fragments={len(fragments)}")

        return {
            "doc_idx": next_idx,
            "confidence": result.overall,
            "uncertainty_margin": result.uncertainty_margin,
            "is_uncertain": result.is_uncertain,
            "fragments_count": len(fragments),
            "uncertainty_logged": uncertainty_logged,
            "details": result.details,
        }

    finally:
        if autocommit:
            db.close()
        else:
            # Return connection for batch operations
            pass


def _update_term_index(db: sqlite3.Connection, doc_idx: int, content: str) -> None:
    """Basic TF-IDF term index update for the ingested doc."""
    STOP_WORDS = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
                  'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
                  'can', 'could', 'shall', 'should', 'may', 'might', 'must',
                  'i', 'you', 'he', 'she', 'it', 'we', 'they', 'this', 'that',
                  'these', 'those', 'of', 'in', 'on', 'at', 'to', 'for', 'with',
                  'by', 'from', 'as', 'into', 'through', 'during', 'before',
                  'after', 'above', 'below', 'between', 'out', 'off', 'over',
                  'under', 'again', 'further', 'then', 'once', 'here', 'there',
                  'when', 'where', 'why', 'how', 'all', 'each', 'every', 'both',
                  'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
                  'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
                  'and', 'but', 'or', 'hecause', 'about', 'up', 'down', 'also',
                  'just', 'because', 'into', 'over', 'still', 'while'}

    words = re.findall(r'\w{2,}', content.lower())
    word_counts: dict[str, int] = {}
    for w in words:
        if w not in STOP_WORDS:
            word_counts[w] = word_counts.get(w, 0) + 1

    # Get total docs for IDF
    total_docs = db.execute("SELECT COUNT(*) FROM doc_analysis").fetchone()[0]

    for term, count in word_counts.items():
        tf = count / max(len(words), 0.1)

        # Doc frequency for IDF
        existing = db.execute(
            "SELECT COUNT(DISTINCT idx) FROM term_index WHERE term = ?",
            (term,)
        ).fetchone()[0]
        df = existing + 1  # +1 for this new doc
        idf = max(0.0, math.log((total_docs + 1) / df)) if df > 0 else 0.0

        try:
            db.execute(
                "INSERT INTO term_index (term, idx, tf, idf, tfidf) VALUES (?, ?, ?, ?, ?)",
                (term, doc_idx, tf, idf, tf * idf)
            )
        except sqlite3.IntegrityError:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_confidence_system/ingest.py:269 quiet except scope=_update_term_index reason=pass")
            raise
            pass  # conflicting entry, skip


def main():
    import argparse
    parser = argparse.ArgumentParser(description="CIEL Data Ingestion Pipeline")
    parser.add_argument("--content", default="", help="Text content to ingest")
    parser.add_argument("--file", default="", help="Read content from file")
    parser.add_argument("--source", default="web_search",
                        choices=list(SOURCE_WEIGHTS.keys()),
                        help="Source type (default: web_search)")
    parser.add_argument("--url", default="", help="Source URL")
    parser.add_argument("--title", default="", help="Document title")
    parser.add_argument("--themes", default="", help="Comma-separated themes")
    parser.add_argument("--db", default=str(DEFAULT_DB), help="Knowledge DB path")
    parser.add_argument("--no-commit", action="store_true",
                        help="Don't commit (dry-run-ish)")
    args = parser.parse_args()

    # Get content
    content = args.content
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            log.debug(f"can't read file {args.file}: {e}")
            sys.exit(1)

    if not content:
        # Read from stdin
        print("Wpisz treść do ingestion (Ctrl+D kończy):", file=sys.stderr)
        content = sys.stdin.read().strip()

    if not content:
        parser.print_help()
        sys.exit(1)

    themes = [t.strip() for t in args.themes.split(",") if t.strip()] if args.themes else []

    result = ingest_text(
        content=content,
        source_type=args.source,
        source_url=args.url,
        title=args.title or f"ingested_{datetime.now().strftime('%H%M%S')}",
        themes=themes,
        db_path=args.db,
        autocommit=not args.no_commit,
    )

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    import math  # needed by _update_term_index
    main()
