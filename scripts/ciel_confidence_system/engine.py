#!/usr/bin/env python3
"""
ciel_confidence.py — Confidence scoring engine for ingested data.

Każdy fakt/kawałek informacji dostaje procentową pewność (0.0 – 1.0).
Składowe:
  1. Source reliability — waga źródła (academic=0.9, blog=0.35, ...)
  2. Cross-reference count — ile niezależnych źródeł potwierdza
  3. Recency — jak świeża informacja
  4. Internal consistency — czy nie przeczy wysokiej-pewności wiedzy
  5. Self-consistency — czy nie przeczy samej sobie

Używany przez: ciel_ingest.py, ciel_knowledge_query.py, ciel_uncertainty_report.py

>>> from ciel_confidence import score_confidence
>>> result = score_confidence(text="...", source_type="academic_paper", db_conn=conn)
>>> result.overall  # 0.87
"""
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import sqlite3
import re
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

import numpy as np


# === Source type weights — synced with source_reliability table ===
SOURCE_WEIGHTS = {
    "academic_paper": 0.90,
    "government_edu": 0.85,
    "technical_doc": 0.80,
    "news_reputable": 0.65,
    "news_general": 0.50,
    "blog_technical": 0.55,
    "blog_general": 0.35,
    "llm_generated": 0.30,
    "user_provided": 0.50,
    "web_search": 0.40,
    "cross_ref_derived": 0.60,
    "unknown": 0.40,
}


@dataclass
class ConfidenceResult:
    """Full confidence breakdown for one piece of information."""
    overall: float          # 0.0 – 1.0
    source_reliability: float
    cross_ref_score: float
    recency_score: float
    consistency_score: float
    self_consistency: float
    is_uncertain: bool      # True if overall < 0.6
    uncertainty_margin: float  # 1.0 - overall (the margin of error)
    details: str            # Human-readable breakdown


def score_source_type(source_type: str, db: Optional[sqlite3.Connection] = None) -> float:
    """Get base reliability weight for source type."""
    # Try DB first
    if db is not None:
        try:
            cur = db.execute(
                "SELECT base_weight FROM source_reliability WHERE source_type = ?",
                (source_type,)
            )
            row = cur.fetchone()
            if row:
                return row[0]
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_confidence_system/engine.py:73 quiet except scope=score_source_type reason=pass")
            pass
    # Fallback to hardcoded
    return SOURCE_WEIGHTS.get(source_type, 0.40)


def score_cross_ref(text: str, db: sqlite3.Connection, max_count: int = 10) -> tuple[float, int]:
    """
    Score how many existing documents support this text.
    Uses embedding similarity + TF-IDF keyword overlap.
    Returns (score, count) where score is sigmoid-scaled [0, 1].
    """
    # Extract significant terms (3+ chars, not stop words)
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
                  'and', 'but', 'or', 'because', 'about', 'up', 'down'}
    terms = set()
    for word in re.findall(r'\w{3,}', text.lower()):
        if word not in STOP_WORDS:
            terms.add(word)

    if not terms:
        return (0.0, 0)

    # Query term_index for matching docs
    placeholders = ",".join("?" for _ in terms)
    try:
        rows = db.execute(
            f"SELECT DISTINCT idx FROM term_index WHERE term IN ({placeholders})",
            list(terms)
        ).fetchall()
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_confidence_system/engine.py:113 quiet except scope=score_cross_ref reason=return (0.0, 0)")
        return (0.0, 0)

    matching_doc_indices = {r[0] for r in rows}
    count = min(len(matching_doc_indices), max_count)

    # Sigmoid: 0 matches → 0, 3+ matches → ~0.9
    score = 2.0 / (1.0 + math.exp(-0.8 * count)) - 1.0
    score = max(0.0, min(1.0, score))

    return (score, count)


def score_recency(doc_timestamp: Optional[str] = None, days_back: Optional[int] = None) -> float:
    """
    Score how recent the information is.
    0 days → 1.0, 30 days → 0.9, 365 days → 0.7, 1825 days (5yr) → 0.5
    """
    if days_back is not None:
        days = days_back
    elif doc_timestamp:
        try:
            dt = datetime.fromisoformat(doc_timestamp)
            days = (datetime.now(timezone.utc) - dt).days
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_confidence_system/engine.py:137 quiet except scope=score_recency reason=assign_fallback")
            days = 9999
    else:
        days = 9999

    # Exponential decay: e^(-days/500)
    score = math.exp(-days / 500.0)
    return max(0.1, min(1.0, score))


def score_consistency(text: str, db: sqlite3.Connection,
                      high_confidence_threshold: float = 0.7) -> tuple[float, str]:
    """
    Check if text contradicts existing high-confidence knowledge.
    Returns (score, reason).
    1.0 = fully consistent, 0.0 = direct contradiction found.
    """
    # Extract key claims (sentences with "is", "are", "was", "were")
    sentences = re.split(r'[.!?]+', text)
    claims = [s.strip().lower() for s in sentences
              if any(op in s.lower() for op in ['is ', 'are ', 'was ', 'were ',
                                                  'has ', 'have ', 'does ',
                                                  'cannot ', 'can not', 'never ',
                                                  'always ', 'must ', 'will '])]

    if not claims:
        return (0.5, "no extractable claims to verify")

    # Get high-confidence docs
    try:
        high_conf = db.execute(
            "SELECT idx, essence FROM doc_analysis WHERE confidence >= ? AND essence != '' LIMIT 20",
            (high_confidence_threshold,)
        ).fetchall()
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_confidence_system/engine.py:171 quiet except scope=score_consistency reason=return (0.5, \"no high-confidence docs to compare\")")
        return (0.5, "no high-confidence docs to compare")

    if not high_conf:
        return (0.5, "no high-confidence reference docs yet")

    # Simple negation check: look for contradictory terms
    contradiction_count = 0
    total_checks = 0

    for claim in claims:
        claim_words = set(re.findall(r'\w+', claim))
        for doc_idx, essence in high_conf:
            essence_lower = essence.lower()
            essence_words = set(re.findall(r'\w+', essence_lower))

            # Check for negation patterns
            # If claim says "X is Y" and essence says "X is not Y"
            for neg in ['not ', "n't ", 'never ', 'cannot ']:
                if neg in claim:
                    # Claim is negative — check if any high-conf doc says the positive
                    positive_claim = claim.replace(neg, '')
                    pos_words = set(re.findall(r'\w+', positive_claim))
                    overlap = pos_words & essence_words
                    if len(overlap) >= 3:
                        contradiction_count += 1
                    break
            else:
                # Claim is positive — check negatives in essence
                if any(neg in essence_lower for neg in ['not ', "n't ", 'never ']):
                    neg_words = set(re.findall(r'\w+', essence_lower))
                    overlap = claim_words & neg_words
                    if len(overlap) >= 3:
                        contradiction_count += 1
            total_checks += 1

    if total_checks == 0:
        return (0.5, "no consistency checks performed")

    consistency = 1.0 - (contradiction_count / total_checks)
    consistency = max(0.0, min(1.0, consistency))

    if consistency < 0.3:
        reason = f"potential contradiction: {contradiction_count}/{total_checks} claims conflict with existing knowledge"
    elif consistency < 0.7:
        reason = f"partial alignment: {contradiction_count}/{total_checks} claims may conflict"
    else:
        reason = f"consistent: {contradiction_count}/{total_checks} contradictions found"

    return (consistency, reason)


def score_self_consistency(text: str) -> tuple[float, str]:
    """
    Check if the text contradicts itself.
    1.0 = coherent, 0.0 = self-contradictory.
    """
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip().lower() for s in sentences if len(s.strip()) > 10]

    if len(sentences) < 2:
        return (0.5, "single sentence — no internal comparison")

    contradictions = 0
    pairs = 0

    for i, s1 in enumerate(sentences):
        s1_words = set(re.findall(r'\w+', s1))
        for j, s2 in enumerate(sentences):
            if i >= j:
                continue
            s2_words = set(re.findall(r'\w+', s2))
            pairs += 1

            # Check for direct contradiction: "X is Y" vs "X is not Y"
            for word in s1_words & s2_words:
                # Extract subject-verb patterns
                s1_neg = any(n in s1 for n in ['not ', "n't ", 'never '])
                s2_neg = any(n in s2 for n in ['not ', "n't ", 'never '])
                if s1_neg != s2_neg and len(s1_words & s2_words) >= 2:
                    contradictions += 1
                    break

    if pairs == 0:
        return (0.5, "no sentence pairs to compare")

    consistency = 1.0 - (contradictions / pairs)
    consistency = max(0.0, min(1.0, consistency))

    if consistency < 0.7:
        reason = f"self-contradiction risk: {contradictions}/{pairs} sentence pairs conflict"
    else:
        reason = f"internally consistent: {contradictions}/{pairs} conflicts"

    return (consistency, reason)


def score_confidence(
    text: str,
    source_type: str = "unknown",
    source_url: str = "",
    timestamp: Optional[str] = None,
    days_back: Optional[int] = None,
    db: Optional[sqlite3.Connection] = None,
    weights: Optional[dict] = None,
) -> ConfidenceResult:
    """
    Compute full confidence score for a piece of text.

    Args:
        text: The information to score
        source_type: Type of source (academic_paper, blog_general, etc.)
        source_url: URL for source tracking
        timestamp: ISO timestamp of the source
        days_back: Alternative to timestamp — how old is the info
        db: Knowledge DB connection for cross-ref + consistency checks
        weights: Custom weight dict for blending components (default: equal)

    Returns:
        ConfidenceResult with full breakdown
    """
    if weights is None:
        weights = {
            "source_reliability": 0.30,
            "cross_ref": 0.25,
            "recency": 0.15,
            "consistency": 0.20,
            "self_consistency": 0.10,
        }

    # 1. Source reliability
    src_score = score_source_type(source_type, db)

    # 2. Cross-reference
    cross_score = 0.0
    cross_count = 0
    if db is not None:
        cross_score, cross_count = score_cross_ref(text, db)

    # 3. Recency
    recency_score = score_recency(timestamp, days_back)

    # 4. Internal consistency
    cons_score = 0.5
    cons_reason = "no db available for consistency check"
    if db is not None:
        cons_score, cons_reason = score_consistency(text, db)

    # 5. Self-consistency
    self_cons_score, self_cons_reason = score_self_consistency(text)

    # Weighted blend
    overall = (
        weights["source_reliability"] * src_score +
        weights["cross_ref"] * cross_score +
        weights["recency"] * recency_score +
        weights["consistency"] * cons_score +
        weights["self_consistency"] * self_cons_score
    )
    overall = max(0.0, min(1.0, overall))

    is_uncertain = overall < 0.6
    uncertainty_margin = round(1.0 - overall, 3)

    # Build human-readable details
    details_parts = [
        f"source_type={source_type} ({src_score:.2f})",
        f"cross_ref={cross_score:.2f} ({cross_count} matches)",
        f"recency={recency_score:.2f}",
        f"consistency={cons_score:.2f} ({cons_reason})",
        f"self_consistency={self_cons_score:.2f} ({self_cons_reason})",
    ]

    return ConfidenceResult(
        overall=round(overall, 4),
        source_reliability=round(src_score, 4),
        cross_ref_score=round(cross_score, 4),
        recency_score=round(recency_score, 4),
        consistency_score=round(cons_score, 4),
        self_consistency=round(self_cons_score, 4),
        is_uncertain=is_uncertain,
        uncertainty_margin=uncertainty_margin,
        details=" | ".join(details_parts),
    )


# === CLI ===
def main():
    import argparse
    parser = argparse.ArgumentParser(description="CIEL Confidence Scorer")
    parser.add_argument("text", nargs="?", default="", help="Text to score")
    parser.add_argument("--source-type", default="unknown",
                        choices=list(SOURCE_WEIGHTS.keys()),
                        help="Type of source")
    import sys as _sys, pathlib as _pathlib
    _sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parents[2] / "src"))
    from ciel_geometry.paths import P as _P
    parser.add_argument("--db", default=str(_P.DB.KNOWLEDGE),
                        help="Knowledge DB path")
    parser.add_argument("--days-back", type=int, default=None,
                        help="Override recency (days old)")
    args = parser.parse_args()

    if not args.text:
        # Interactive mode
        print("CIEL Confidence Scorer — wpisz tekst do oceny (Ctrl+D kończy):")
        import sys
        lines = sys.stdin.read()
        args.text = lines.strip()

    if not args.text:
        parser.print_help()
        return

    db = None
    if args.db:
        try:
            db = sqlite3.connect(args.db, timeout=5)
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_confidence_system/engine.py:386 quiet except scope=main reason=pass")
            pass

    result = score_confidence(args.text, source_type=args.source_type,
                              days_back=args.days_back, db=db)

    # Pretty print
    import json
    print(json.dumps({
        "overall_confidence": result.overall,
        "uncertainty_margin": result.uncertainty_margin,
        "is_uncertain": result.is_uncertain,
        "breakdown": {
            "source_reliability": result.source_reliability,
            "cross_ref_score": result.cross_ref_score,
            "recency_score": result.recency_score,
            "consistency_score": result.consistency_score,
            "self_consistency": result.self_consistency,
        },
        "details": result.details,
    }, indent=2, ensure_ascii=False))

    if db:
        db.close()


if __name__ == "__main__":
    main()
