#!/usr/bin/env python3
"""
ciel_backfill_confidence.py — Backfill confidence scores for existing docs.

Dla każdego dokumentu w doc_analysis który ma confidence=NULL lub confidence=0.5:
  1. Określ source_type na podstawie filename/essence
  2. Sprawdź cross-reference z innymi dokumentami
  3. Oblicz recency (brak daty → neutral 0.5)
  4. Zapisz confidence + wpis w confidence_scores

Uruchom:
    python3 scripts/ciel_backfill_confidence.py [--db /tmp/noema_knowledge.db] [--dry-run]
"""

import sqlite3
import json
import sys
import pathlib
import logging
import re
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="[backfill] %(message)s")
log = logging.getLogger("backfill")

from .engine import score_confidence, SOURCE_WEIGHTS

DEFAULT_DB = pathlib.Path("/tmp/noema_knowledge.db")


def guess_source_type(filename: str, essence: str) -> str:
    """Guess source type based on filename and essence content."""
    text = (filename + " " + essence[:500]).lower()
    if any(d in text for d in ['.edu', '.gov', '.ac.uk']):
        return "government_edu"
    if any(d in text for d in ['arxiv', '.pdf', 'ieee', 'acm', 'springer',
                                'elsevier', 'nature.com', 'science.']):
        return "academic_paper"
    if any(d in text for d in ['blog.', 'medium.com', 'substack', 'wordpress']):
        return "blog_technical"
    if any(d in text for d in ['reuters', 'bbc.', 'ap.org', 'theguardian']):
        return "news_reputable"
    if any(d in text for d in ['docs.', 'documentation', 'wiki.', 'manual']):
        return "technical_doc"
    return "unknown"


def backfill(db_path: str, dry_run: bool = False) -> dict:
    """Backfill confidence for all docs with default confidence."""
    conn = sqlite3.connect(db_path, timeout=5)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.row_factory = sqlite3.Row

    # Check if confidence column exists
    cols = [r[1] for r in conn.execute("PRAGMA table_info(doc_analysis)").fetchall()]
    if "confidence" not in cols:
        log.error("confidence column missing — run ciel_schema_migrate.py first")
        conn.close()
        return {"error": "schema not migrated"}

    # Get docs with default confidence (0.5) or NULL
    docs = conn.execute("""
        SELECT idx, filename, essence, status
        FROM doc_analysis
        WHERE confidence IS NULL OR confidence = 0.5
        ORDER BY idx
    """).fetchall()

    log.info(f"Found {len(docs)} docs to backfill")

    stats = {"processed": 0, "skipped": 0, "errors": 0, "uncertain": 0}
    updated_confs = []

    for doc in docs:
        idx = doc["idx"]
        filename = doc["filename"] or ""
        essence = doc["essence"] or ""

        if not essence and not filename:
            stats["skipped"] += 1
            continue

        content = essence[:2000]
        source_type = guess_source_type(filename, essence)

        try:
            result = score_confidence(
                content,
                source_type=source_type,
                db=conn,
            )

            if dry_run:
                updated_confs.append({
                    "idx": idx,
                    "source_type": source_type,
                    "confidence": result.overall,
                    "uncertain": result.is_uncertain,
                    "details": result.details,
                })
            else:
                conn.execute("""
                    UPDATE doc_analysis SET
                        confidence = ?,
                        source_type = ?,
                        source_reliability = ?,
                        consistency_score = ?,
                        is_uncertain = ?
                    WHERE idx = ?
                """, (
                    result.overall,
                    source_type,
                    result.source_reliability,
                    result.consistency_score,
                    1 if result.is_uncertain else 0,
                    idx,
                ))

                # Also insert into confidence_scores
                conn.execute("""
                    INSERT OR IGNORE INTO confidence_scores
                        (doc_idx, source_reliability, cross_ref_score, recency_score,
                         consistency_score, self_consistency, overall)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    idx,
                    result.source_reliability,
                    result.cross_ref_score,
                    result.recency_score,
                    result.consistency_score,
                    result.self_consistency,
                    result.overall,
                ))

                # Log uncertainty
                if result.is_uncertain:
                    conn.execute("""
                        INSERT OR IGNORE INTO uncertainty_log
                            (doc_idx, confidence_score, reason, details)
                        VALUES (?, ?, ?, ?)
                    """, (
                        idx,
                        result.overall,
                        f"backfill: low confidence ({result.overall:.2f}) — {source_type}",
                        result.details,
                    ))

            stats["processed"] += 1
            if result.is_uncertain:
                stats["uncertain"] += 1

        except Exception as e:
            log.warning(f"error processing idx={idx}: {e}")
            stats["errors"] += 1

    if not dry_run:
        conn.commit()

    conn.close()

    stats["updated_confs"] = updated_confs if dry_run else []
    log.info(f"Done: {stats['processed']} processed, {stats['uncertain']} uncertain, "
             f"{stats['errors']} errors, {stats['skipped']} skipped")
    return stats


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Backfill confidence for existing docs")
    parser.add_argument("--db", default=str(DEFAULT_DB), help="Knowledge DB path")
    parser.add_argument("--dry-run", action="store_true", help="Don't write, just show")
    args = parser.parse_args()

    result = backfill(args.db, dry_run=args.dry_run)
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
