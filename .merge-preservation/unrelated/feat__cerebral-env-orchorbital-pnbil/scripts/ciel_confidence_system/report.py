#!/usr/bin/env python3
"""
ciel_uncertainty_report.py — Uncertainty dashboard.

Pokazuje:
  - Dokumenty z niską pewnością (confidence < 0.6)
  - Nierozwiązane wpisy z uncertainty_log
  - Potencjalne konflikty (wysoka podobieństwo, różne confidence)
  - Luki w wiedzy (tematy z małą liczbą dokumentów)

Uruchom:
  python3 scripts/ciel_uncertainty_report.py [--db /tmp/noema_knowledge.db]
  python3 scripts/ciel_uncertainty_report.py --summary   # tylko podsumowanie
"""
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import sqlite3
import json
import sys
import pathlib
from datetime import datetime

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))
from ciel_geometry.paths import P

# Was hardcoded /tmp/noema_knowledge.db (tmpfs, wiped on reboot) — fixed 2026-07-08.
DEFAULT_DB = pathlib.Path(P.DB.KNOWLEDGE)


def _get_db(db_path: str):
    conn = sqlite3.connect(db_path, timeout=5)
    conn.row_factory = sqlite3.Row
    return conn


def low_confidence_docs(db, threshold: float = 0.6, limit: int = 20) -> list[dict]:
    """Docs with confidence below threshold."""
    try:
        rows = db.execute("""
            SELECT idx, essence, confidence, source_type, source_reliability,
                   cross_ref_count, consistency_score, is_uncertain, ingested_at
            FROM doc_analysis
            WHERE confidence IS NOT NULL AND confidence < ?
            ORDER BY confidence ASC
            LIMIT ?
        """, (threshold, limit)).fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_confidence_system/report.py:43 quiet except scope=low_confidence_docs reason=return [{\"error\": str(e)}]")
        raise
        return [{"error": str(e)}]


def unresolved_uncertainty(db, limit: int = 20) -> list[dict]:
    """Unresolved uncertainty log entries."""
    try:
        rows = db.execute("""
            SELECT u.id, u.doc_idx, u.confidence_score, u.reason, u.details,
                   u.created_at, d.essence
            FROM uncertainty_log u
            LEFT JOIN doc_analysis d ON u.doc_idx = d.idx
            WHERE u.resolved_at IS NULL
            ORDER BY u.confidence_score ASC
            LIMIT ?
        """, (limit,)).fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_confidence_system/report.py:60 quiet except scope=unresolved_uncertainty reason=return [{\"error\": str(e)}]")
        raise
        return [{"error": str(e)}]


def potential_conflicts(db, similarity_threshold: float = 0.8, limit: int = 10) -> list[dict]:
    """Docs with high embedding similarity but different confidence."""
    try:
        # Find docs with similar embedding essence but confidence gap > 0.3
        rows = db.execute("""
            SELECT a.idx as idx_a, b.idx as idx_b,
                   a.confidence as conf_a, b.confidence as conf_b,
                   a.essence as essence_a, b.essence as essence_b,
                   ABS(a.confidence - b.confidence) as conf_gap
            FROM doc_analysis a
            JOIN doc_analysis b ON a.idx < b.idx
            WHERE a.confidence IS NOT NULL AND b.confidence IS NOT NULL
              AND ABS(a.confidence - b.confidence) > 0.3
              AND LENGTH(a.essence) > 20 AND LENGTH(b.essence) > 20
            ORDER BY conf_gap DESC
            LIMIT ?
        """, (limit,)).fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_confidence_system/report.py:82 quiet except scope=potential_conflicts reason=return [{\"error\": str(e)}]")
        raise
        return [{"error": str(e)}]


def topic_gaps(db, min_docs: int = 3, limit: int = 15) -> list[dict]:
    """Themes with very few docs (knowledge gaps)."""
    try:
        rows = db.execute("""
            SELECT themes, COUNT(*) as doc_count,
                   AVG(confidence) as avg_confidence
            FROM doc_analysis
            WHERE themes IS NOT NULL AND themes != ''
            GROUP BY themes
            HAVING doc_count < ?
            ORDER BY doc_count ASC
            LIMIT ?
        """, (min_docs, limit)).fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_confidence_system/report.py:100 quiet except scope=topic_gaps reason=return [{\"error\": str(e)}]")
        raise
        return [{"error": str(e)}]


def summary(db) -> dict:
    """Overall uncertainty summary."""
    result = {}
    try:
        result["total_docs"] = db.execute("SELECT COUNT(*) FROM doc_analysis").fetchone()[0]

        # Check if confidence column exists
        cols = [r[1] for r in db.execute("PRAGMA table_info(doc_analysis)").fetchall()]
        if "confidence" not in cols:
            result["note"] = "confidence columns not yet migrated — run ciel_schema_migrate.py"
            return result

        result["avg_confidence"] = round(
            db.execute("SELECT AVG(confidence) FROM doc_analysis WHERE confidence IS NOT NULL").fetchone()[0] or 0, 3)
        result["uncertain_docs"] = db.execute(
            "SELECT COUNT(*) FROM doc_analysis WHERE is_uncertain = 1").fetchone()[0]
        result["lowest_confidence"] = round(
            db.execute("SELECT MIN(confidence) FROM doc_analysis WHERE confidence IS NOT NULL").fetchone()[0] or 0, 3)

        # Uncertainty log
        try:
            result["unresolved_uncertainties"] = db.execute(
                "SELECT COUNT(*) FROM uncertainty_log WHERE resolved_at IS NULL").fetchone()[0]
            result["total_uncertainties_logged"] = db.execute(
                "SELECT COUNT(*) FROM uncertainty_log").fetchone()[0]
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_confidence_system/report.py:129 quiet except scope=summary reason=assign_fallback")
            raise
            result["uncertainty_log"] = "table not found"

        # Source type distribution
        try:
            src_rows = db.execute("""
                SELECT source_type, COUNT(*) as cnt,
                       AVG(confidence) as avg_conf
                FROM doc_analysis
                WHERE source_type IS NOT NULL
                GROUP BY source_type
                ORDER BY cnt DESC
            """).fetchall()
            result["source_distribution"] = [dict(r) for r in src_rows]
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_confidence_system/report.py:143 quiet except scope=summary reason=pass")
            raise
            pass

    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_confidence_system/report.py:146 quiet except scope=summary reason=assign_fallback")
        raise
        result["error"] = str(e)
    return result


def main():
    import argparse
    parser = argparse.ArgumentParser(description="CIEL Uncertainty Report")
    parser.add_argument("--db", default=str(DEFAULT_DB), help="Knowledge DB path")
    parser.add_argument("--summary", action="store_true", help="Only summary")
    parser.add_argument("--threshold", type=float, default=0.6,
                        help="Confidence threshold (default: 0.6)")
    parser.add_argument("--limit", type=int, default=15, help="Max results per section")
    args = parser.parse_args()

    if not pathlib.Path(args.db).exists():
        print(json.dumps({"error": f"DB not found at {args.db}"}, indent=2))
        sys.exit(1)

    db = _get_db(args.db)

    report = {}

    # Summary always
    report["summary"] = summary(db)

    if not args.summary:
        report["low_confidence_docs"] = low_confidence_docs(db, args.threshold, args.limit)
        report["unresolved_uncertainties"] = unresolved_uncertainty(db, args.limit)
        report["potential_conflicts"] = potential_conflicts(db, limit=args.limit)
        report["topic_gaps"] = topic_gaps(db, limit=args.limit)

    db.close()
    print(json.dumps(report, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
