#!/usr/bin/env python3
"""Legacy 24D library-index migration tool plus live-search compatibility shim.

The historical `library_index.npy` remains 24D.  This script may still convert
that legacy artifact into the zip-catalog format, but it is NOT the canonical
live retrieval geometry.

Live `query_text()` delegates to the typed Octopus-RAG knowledge arm, which
uses the persistent knowledge DB for retrieval evidence and 36-oscillator
PhaseNav geometry as an additive signal.

Usage:
    .venv/bin/python3 scripts/noema_library_indexer.py   # legacy migration
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.phasenav.operator_algebra import operator_signature

LIBRARY_INDEX = "/media/adrian/New Volume1/NOEMA_PHASE_DATA/PHASE_INDEX/library_index.npy"
LIBRARY_META = "/media/adrian/New Volume1/NOEMA_PHASE_DATA/PHASE_INDEX/library_meta.npy"
OUTPUT = Path("/dev/shm/ciel_noema/zip_catalog/index.jsonl")

OPERATORS = [
    "ACTION_REQUEST", "ADDITION", "AFFECT", "ASSERTION", "BOUNDARY",
    "CANON_BLOCK", "CAUSE", "COMPOSITION", "CONDITION", "CONSENT",
    "CONSENT_REQUIRED", "DIFFERENCE", "FOLD", "FORCE", "HYPOTHESIS",
    "IDENTITY", "MEMORY", "MODAL_NECESSITY", "MODAL_OBLIGATION",
    "MODAL_PERMISSION", "MODAL_POSSIBILITY", "NEGATION", "ORDER",
    "PAUSE", "PREFERENCE", "QUESTION", "REFUSAL", "RETURN", "RISK",
    "SCOPE", "SIMULATION_BOUNDARY", "SOURCE", "SOURCE_REQUIRED",
    "TRANSFORM", "UNCERTAINTY", "UNRUH_DRIVE", "WARP_DRIFT",
]


def query_text(text: str, top_k: int = 10) -> list[dict[str, Any]]:
    """Compatibility API used by `CIEL_CANON.py --search`.

    Retrieval no longer uses the legacy 24D hash index.  New code should call
    `ciel_sot_agent.pnv_rag_arm.query_knowledge_arm()` directly to retain typed
    provenance and phase-space information.
    """

    from ciel_sot_agent.pnv_rag_arm import query_text as _query_text

    return _query_text(text, top_k=top_k)


def _normalize(v: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(v)
    return v / n if n > 1e-12 else v


def _nearest_operator(vec: np.ndarray) -> tuple[str, float]:
    """Legacy-only comparison for migration reports.

    A dimension mismatch is intentionally retained as a legacy projection by
    truncation and must not be used as a canonical 36D gate signal.
    """

    v_norm = _normalize(vec)
    best_op = "IDENTITY"
    best_sim = -1.0
    for op in OPERATORS:
        sig = operator_signature(op)
        if sig.shape[0] != v_norm.shape[0]:
            n = min(sig.shape[0], v_norm.shape[0])
            sig = sig[:n]
            v_cmp = v_norm[:n]
        else:
            v_cmp = v_norm
        sig_norm = _normalize(sig)
        sim = float(np.dot(v_cmp, sig_norm))
        if sim > best_sim:
            best_sim = sim
            best_op = op
    return best_op, best_sim


def main() -> int:
    """Convert the historical 24D library index for archival compatibility."""

    vectors = np.load(LIBRARY_INDEX)  # historical (1284, 24) float64
    meta = np.load(LIBRARY_META)      # structured array

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    op_counts: dict[str, int] = {}

    with open(OUTPUT, "w") as f:
        for i in range(len(vectors)):
            vec = vectors[i]
            op_id, sim = _nearest_operator(vec)
            op_counts[op_id] = op_counts.get(op_id, 0) + 1

            entry = {
                "zip_path": str(meta[i]["disk_path"]),
                "total_files": 1,
                "phasenav": {
                    "operator_id": op_id,
                    "operator_vector_24d": vec.tolist(),
                    "cosine_similarity": round(sim, 4),
                    "status": "LEGACY_24D_NONCANONICAL",
                },
                "meta": {
                    "id": str(meta[i]["id"]),
                    "filename": str(meta[i]["filename"]),
                    "author": str(meta[i]["author"]),
                    "topic": str(meta[i]["topic"]),
                },
            }
            f.write(json.dumps(entry) + "\n")
            count += 1

    print(f"Zapisano {count} wpisów do {OUTPUT}")
    print("UWAGA: wygenerowane wektory mają status LEGACY_24D_NONCANONICAL")
    print(f"Rozkład operatorów ({len(op_counts)} unikalnych):")
    for op, c in sorted(op_counts.items(), key=lambda x: -x[1]):
        print(f"  {op}: {c} ({100*c/count:.1f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
