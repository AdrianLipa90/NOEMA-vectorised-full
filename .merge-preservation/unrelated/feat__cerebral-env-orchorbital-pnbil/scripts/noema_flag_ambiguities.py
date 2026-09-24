#!/usr/bin/env python3
"""Extend uncertainty_log with ambiguity categories beyond low confidence.

ciel_confidence_system/backfill.py already logs low-confidence docs
(overall < 0.6). This adds three more categories Adrian explicitly asked
to have flagged, reusing the same table (one queue, not scattered ad hoc
tables):
  - source_type == 'unknown' (no real provenance signal at all)
  - zero PhaseNav concept tags matched (doc_concepts has no rows for it)
  - missing source_url for a source type where a URL is expected
    (i.e. not library_scan/pdf, which are file-based, URL-less by nature)

Idempotent: skips a doc+reason-category pair if already logged.

Usage:
    python3 scripts/noema_flag_ambiguities.py
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ciel_geometry.paths import P

KNOWLEDGE_DB = str(P.DB.KNOWLEDGE)

# URL-less-by-nature source types — file ingested directly, no web origin expected.
FILE_BASED_TYPES = {"library_scan", "pdf"}


def _already_flagged(db: sqlite3.Connection, doc_idx: int, reason_prefix: str) -> bool:
    row = db.execute(
        "SELECT 1 FROM uncertainty_log WHERE doc_idx=? AND reason LIKE ?",
        (doc_idx, f"{reason_prefix}%"),
    ).fetchone()
    return row is not None


def flag_unknown_source(db: sqlite3.Connection) -> int:
    n = 0
    for row in db.execute("SELECT idx, confidence FROM doc_analysis WHERE source_type = 'unknown'"):
        idx, conf = row
        if _already_flagged(db, idx, "unknown_source"):
            continue
        db.execute(
            "INSERT INTO uncertainty_log (doc_idx, confidence_score, reason, details) VALUES (?, ?, ?, ?)",
            (idx, conf, "unknown_source: source_type is 'unknown' — no provenance signal", ""),
        )
        n += 1
    return n


def flag_no_concept_tags(db: sqlite3.Connection) -> int:
    n = 0
    rows = db.execute("""
        SELECT da.idx, da.confidence FROM doc_analysis da
        LEFT JOIN doc_concepts dc ON da.idx = dc.doc_idx
        WHERE dc.id IS NULL
    """).fetchall()
    for idx, conf in rows:
        if _already_flagged(db, idx, "no_concept_match"):
            continue
        db.execute(
            "INSERT INTO uncertainty_log (doc_idx, confidence_score, reason, details) VALUES (?, ?, ?, ?)",
            (idx, conf, "no_concept_match: zero PhaseNav operator anchors matched essence/themes", ""),
        )
        n += 1
    return n


def flag_missing_source_url(db: sqlite3.Connection) -> int:
    n = 0
    placeholders = ",".join("?" * len(FILE_BASED_TYPES))
    rows = db.execute(f"""
        SELECT idx, confidence, source_type FROM doc_analysis
        WHERE (source_url IS NULL OR TRIM(source_url) = '')
          AND source_type NOT IN ({placeholders})
    """, tuple(FILE_BASED_TYPES)).fetchall()
    for idx, conf, source_type in rows:
        if _already_flagged(db, idx, "missing_source_url"):
            continue
        db.execute(
            "INSERT INTO uncertainty_log (doc_idx, confidence_score, reason, details) VALUES (?, ?, ?, ?)",
            (idx, conf, f"missing_source_url: source_type='{source_type}' but no source_url recorded", ""),
        )
        n += 1
    return n


def main() -> int:
    db = sqlite3.connect(KNOWLEDGE_DB)
    n1 = flag_unknown_source(db)
    n2 = flag_no_concept_tags(db)
    n3 = flag_missing_source_url(db)
    db.commit()

    total = db.execute("SELECT COUNT(*) FROM uncertainty_log").fetchone()[0]
    unresolved = db.execute("SELECT COUNT(*) FROM uncertainty_log WHERE resolved_at IS NULL").fetchone()[0]
    print(f"[flags] unknown_source: {n1} new")
    print(f"[flags] no_concept_match: {n2} new")
    print(f"[flags] missing_source_url: {n3} new")
    print(f"[flags] uncertainty_log total: {total} rows, {unresolved} unresolved")
    db.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
