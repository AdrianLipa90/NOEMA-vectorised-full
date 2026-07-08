#!/usr/bin/env python3
"""Populate semantic_affinity in the knowledge DB — the document-neighbor
mapping table that has existed in the schema but was never written to by
any script in this repo (confirmed 2026-07-08: only read call sites exist).

Reuses the TF-IDF vectors already computed in term_index (759918 rows,
7472 documents) rather than re-parsing source documents. For each document,
finds candidate neighbors via an inverted term index (skipping overly
common terms that don't discriminate), computes cosine similarity, and
keeps the top-K neighbors per document.

Usage:
    python3 scripts/noema_build_semantic_affinity.py [--top-k 8] [--max-df 400]
"""
from __future__ import annotations

import argparse
import sqlite3
import time
from collections import defaultdict

KNOWLEDGE_DB = "/tmp/noema_knowledge.db"


def build(top_k: int = 8, max_df: int = 400, min_affinity: float = 0.05) -> int:
    db = sqlite3.connect(KNOWLEDGE_DB)
    db.row_factory = sqlite3.Row

    print("[affinity] loading term_index...")
    t0 = time.time()
    doc_vecs: dict[int, dict[str, float]] = defaultdict(dict)
    term_docs: dict[str, list[int]] = defaultdict(list)
    for row in db.execute("SELECT idx, term, tfidf FROM term_index"):
        doc_vecs[row["idx"]][row["term"]] = row["tfidf"]
        term_docs[row["term"]].append(row["idx"])
    print(f"[affinity] loaded {len(doc_vecs)} docs, {len(term_docs)} terms in {time.time()-t0:.1f}s")

    # Drop terms that appear in too many documents — they inflate candidate
    # sets without discriminating (the same reason max_df cutoffs exist in
    # any TF-IDF pipeline).
    discriminating_terms = {t: docs for t, docs in term_docs.items() if len(docs) <= max_df}
    print(f"[affinity] {len(discriminating_terms)}/{len(term_docs)} terms kept after max_df={max_df} cutoff")

    doc_norms = {idx: sum(v * v for v in vec.values()) ** 0.5 for idx, vec in doc_vecs.items()}

    db.execute("DELETE FROM semantic_affinity")
    inserted = 0
    t0 = time.time()
    for i, (idx, vec) in enumerate(doc_vecs.items()):
        candidates: set[int] = set()
        for term in vec:
            if term in discriminating_terms:
                candidates.update(discriminating_terms[term])
        candidates.discard(idx)
        if not candidates:
            continue

        scored = []
        na = doc_norms[idx]
        if na == 0:
            continue
        for cand in candidates:
            cvec = doc_vecs[cand]
            common = vec.keys() & cvec.keys()
            if not common:
                continue
            dot = sum(vec[t] * cvec[t] for t in common)
            nb = doc_norms[cand]
            if nb == 0:
                continue
            sim = dot / (na * nb)
            if sim >= min_affinity:
                scored.append((sim, cand))

        scored.sort(reverse=True)
        for sim, cand in scored[:top_k]:
            db.execute(
                "INSERT INTO semantic_affinity (neighbor_idx, center_idx, affinity, phase_diff) VALUES (?, ?, ?, NULL)",
                (cand, idx, round(sim, 6)),
            )
            inserted += 1

        if (i + 1) % 1000 == 0:
            print(f"[affinity] {i+1}/{len(doc_vecs)} docs processed, {inserted} pairs so far ({time.time()-t0:.1f}s)")
            db.commit()

    db.commit()
    print(f"[affinity] done: {inserted} pairs inserted in {time.time()-t0:.1f}s")
    db.close()
    return inserted


def main() -> int:
    ap = argparse.ArgumentParser(description="Build semantic_affinity from existing TF-IDF term_index")
    ap.add_argument("--top-k", type=int, default=8)
    ap.add_argument("--max-df", type=int, default=400, help="skip terms appearing in more than this many docs")
    ap.add_argument("--min-affinity", type=float, default=0.05)
    args = ap.parse_args()
    n = build(top_k=args.top_k, max_df=args.max_df, min_affinity=args.min_affinity)
    print(f"\n{n} affinity pairs written to {KNOWLEDGE_DB}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
