#!/usr/bin/env python3
"""Szuka istniejących implementacji osi leksykalnych i batchowego ingestion
w /media/adrian/REPOZYTORIA_GIT1/New_Volume/."""
from __future__ import annotations
import json
import re
from pathlib import Path

SEARCH_ROOT = Path("/media/adrian/REPOZYTORIA_GIT1/New_Volume/CIEL_PROJECT_CANON/CIELINGO_CANON")

AXES = [
    "language_detection_axis",
    "case_inflection_axis",
    "open_lexicon_axis",
    "morphology_axis",
    "source_evidence_axis",
]

BATCH_TERMS = [
    "batch_ingest",
    "batch_ingestion",
    "ingest_batch",
    "knowledge_ingestion",
    "thermodynamic",
    "keplerian",
    "semantic_mass",
    "medium_scalar",
]

EXTRA_TERMS = [
    "language_detection",
    "case_inflection",
    "open_lexicon",
    "morphology_axis",
    "source_evidence",
    "word_label",
    "word_mass",
]

def search(root: Path, terms: list[str]) -> dict[str, list[str]]:
    hits: dict[str, list[str]] = {t: [] for t in terms}
    for path in root.rglob("*.py"):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for term in terms:
            if term in text:
                rel = str(path.relative_to(root))
                if rel not in hits[term]:
                    hits[term].append(rel)
    return hits

axes_hits = search(SEARCH_ROOT, AXES + EXTRA_TERMS)
batch_hits = search(SEARCH_ROOT, BATCH_TERMS)

# Skróć do niepustych
axes_found = {k: v for k, v in axes_hits.items() if v}
batch_found = {k: v for k, v in batch_hits.items() if v}

print(json.dumps({
    "search_root": str(SEARCH_ROOT),
    "axes_found": axes_found,
    "batch_terms_found": batch_found,
    "axes_missing": [k for k, v in axes_hits.items() if not v],
    "batch_missing": [k for k, v in batch_hits.items() if not v],
}, ensure_ascii=False, indent=2))
