#!/usr/bin/env python3
"""Tag every document in the knowledge DB with its top PhaseNav concepts.

Uses the lexical concept_classifier (not the hash-based operator mapping in
operator_algebra.py/phase_nav_lang.py, which is semantically blind) against
the TF-IDF term_index already computed by the ingestion pipeline. Writes to
a new `doc_concepts` table — additive, does not touch doc_analysis.

Usage:
    python3 scripts/noema_tag_concepts.py [--top-k 3] [--min-score 0.01]
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
import time
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ciel_geometry.paths import P
from ciel_geometry.phasenav.concept_classifier import score_document

KNOWLEDGE_DB = str(P.DB.KNOWLEDGE)


def build(top_k: int = 3, min_score: float = 0.01) -> int:
    db = sqlite3.connect(KNOWLEDGE_DB)
    db.row_factory = sqlite3.Row

    db.execute("""
        CREATE TABLE IF NOT EXISTS doc_concepts (
            id INTEGER PRIMARY KEY,
            doc_idx INTEGER,
            operator_id TEXT,
            score REAL,
            method TEXT DEFAULT 'concept_classifier_v1',
            tagged_at TEXT DEFAULT (datetime('now'))
        )
    """)
    db.execute("CREATE INDEX IF NOT EXISTS idx_doc_concepts_doc ON doc_concepts(doc_idx)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_doc_concepts_op ON doc_concepts(operator_id)")

    print("[concepts] loading term_index...")
    t0 = time.time()
    doc_terms: dict[int, dict[str, float]] = defaultdict(dict)
    for row in db.execute("SELECT idx, term, tfidf FROM term_index"):
        doc_terms[row["idx"]][row["term"]] = row["tfidf"]
    print(f"[concepts] loaded {len(doc_terms)} docs in {time.time()-t0:.1f}s")

    db.execute("DELETE FROM doc_concepts")
    inserted = 0
    untagged = 0
    t0 = time.time()
    for i, (idx, term_weights) in enumerate(doc_terms.items()):
        ranked = score_document(term_weights, top_k=top_k)
        ranked = [(op, s) for op, s in ranked if s >= min_score]
        if not ranked:
            untagged += 1
        for op_id, score in ranked:
            db.execute(
                "INSERT INTO doc_concepts (doc_idx, operator_id, score) VALUES (?, ?, ?)",
                (idx, op_id, round(score, 6)),
            )
            inserted += 1

        if (i + 1) % 1000 == 0:
            print(f"[concepts] {i+1}/{len(doc_terms)} docs processed, {inserted} tags so far ({time.time()-t0:.1f}s)")
            db.commit()

    db.commit()
    print(f"[concepts] done: {inserted} tags inserted, {untagged} docs with zero anchor match, in {time.time()-t0:.1f}s")
    db.close()
    return inserted


def main() -> int:
    ap = argparse.ArgumentParser(description="Tag documents with PhaseNav concepts via lexical classifier")
    ap.add_argument("--top-k", type=int, default=3)
    ap.add_argument("--min-score", type=float, default=0.01)
    args = ap.parse_args()
    n = build(top_k=args.top_k, min_score=args.min_score)
    print(f"\n{n} concept tags written to {KNOWLEDGE_DB}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
