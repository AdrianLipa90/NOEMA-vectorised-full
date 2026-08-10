"""Canonical first Octopus-RAG arm for NOEMA.

Retrieval evidence comes from the existing knowledge_bridge TF-IDF index.
PhaseNav is additive geometry, not a replacement for lexical evidence.

New retrieval geometry uses the consolidated `M_sentence_phase_precise`
compatible PNV36 kernel.  The historical fast text oscillator hash and the
legacy 24D library index are not canonical signals for this arm.

This module is read-only: it emits RelationalObservation records and never
promotes retrieved material to NOEMA memory/SoT.
"""
from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any

import numpy as np

from ciel_geometry.phasenav.gate_contracts import (
    ObservationClass,
    PhaseSpace,
    RelationalObservation,
)
from ciel_geometry.phasenav.pnv_precise import ENCODER_ID, SOURCE, circular_alignment, sentence_phase_precise


KnowledgeQuery = Callable[[str, int], list[dict[str, Any]]]
TextEncoder = Callable[[str], Sequence[float]]


def circular_phase_alignment(a: Sequence[float], b: Sequence[float]) -> float:
    """Compatibility name for the canonical precise circular alignment."""

    return circular_alignment(list(a), list(b))


def _default_query(text: str, top_n: int) -> list[dict[str, Any]]:
    from cielingo_core.bridge.knowledge_bridge import query

    return query(text, top_n=top_n)


def _default_encoder(text: str) -> tuple[float, ...]:
    return sentence_phase_precise(text)


def query_knowledge_arm(
    text: str,
    *,
    top_n: int = 5,
    query_fn: KnowledgeQuery | None = None,
    encoder: TextEncoder | None = None,
) -> list[RelationalObservation]:
    """Retrieve typed observations from the canonical knowledge database.

    `similarity` from knowledge_bridge remains the retrieval/evidence score.
    `phase_alignment` is recomputed using canonical precise PNV36 circular
    geometry and is not a ranking authority by itself.
    """

    if not text.strip() or top_n <= 0:
        return []

    query_impl = query_fn or _default_query
    encode = encoder or _default_encoder
    query_phase = np.asarray(tuple(encode(text)), dtype=np.float64).reshape(-1)
    if query_phase.size != 36:
        raise ValueError(f"query encoder must return canonical 36D PNV phases; got {query_phase.size}")

    rows = query_impl(text, top_n)
    observations: list[RelationalObservation] = []

    for rank, row in enumerate(rows[:top_n], start=1):
        idx = row.get("idx")
        filename = str(row.get("filename") or "")
        essence = str(row.get("essence") or "")
        document_text = essence or filename
        doc_phase = np.asarray(tuple(encode(document_text)), dtype=np.float64).reshape(-1)
        if doc_phase.size != 36:
            raise ValueError(f"document encoder must return canonical 36D PNV phases; got {doc_phase.size}")

        lexical = float(row.get("similarity", 0.0) or 0.0)
        lexical = max(0.0, min(1.0, lexical))
        phase_alignment = circular_phase_alignment(query_phase, doc_phase)

        record_id = str(idx) if idx is not None else f"rank-{rank}"
        provenance = (
            f"knowledge-db:doc_analysis:{record_id}",
            "cielingo_core.bridge.knowledge_bridge:query",
            SOURCE,
        )
        if filename:
            provenance += (f"document:{filename}",)

        payload = {
            "idx": idx,
            "filename": filename,
            "themes": row.get("themes", []),
            "affect": row.get("affect", "unknown"),
            "essence": essence,
            "retrieval_score": lexical,
            "phase_alignment": phase_alignment,
            "rank": rank,
            # Preserve the bridge's older fast-encoder value for audit only.
            # It is not used by the canonical PNV arm's decision.
            "legacy_phase_similarity": row.get("phase_similarity"),
        }

        observations.append(
            RelationalObservation(
                observation_id=f"obs:rag:knowledge:{record_id}",
                source="OCTOPUS_RAG:KNOWLEDGE_DB",
                observation_class=ObservationClass.RETRIEVED,
                payload=payload,
                provenance=provenance,
                confidence=lexical,
                phase36=tuple(float(x) for x in doc_phase),
                phase_space=PhaseSpace.PNV_PRECISE_PHASE_36,
                metadata={
                    "query": text,
                    "retrieval_authority": "TFIDF",
                    "phase_signal": "PNV_PRECISE_CIRCULAR_ALIGNMENT_ADDITIVE",
                    "phase_encoder": ENCODER_ID,
                    "read_only": True,
                },
            )
        )

    return observations


def query_text(text: str, top_k: int = 10) -> list[dict[str, Any]]:
    """Compatibility rendering for the historical `CIEL_CANON.py --search` surface.

    New callers should consume `query_knowledge_arm()` directly. This adapter
    intentionally does not fabricate author/disk-path fields absent from the
    knowledge DB result.
    """

    rendered: list[dict[str, Any]] = []
    for observation in query_knowledge_arm(text, top_n=top_k):
        payload = dict(observation.payload)
        rendered.append(
            {
                "id": observation.observation_id,
                "filename": payload.get("filename", ""),
                "topic": ", ".join(str(x) for x in payload.get("themes", [])[:3]),
                "author": "",
                "gamma": float(payload.get("phase_alignment", 0.0)),
                "similarity": float(payload.get("retrieval_score", 0.0)),
                "phase_alignment": float(payload.get("phase_alignment", 0.0)),
                "on_disk": None,
                "disk_path": None,
                "provenance": list(observation.provenance),
            }
        )
    return rendered


__all__ = ["circular_phase_alignment", "query_knowledge_arm", "query_text"]
