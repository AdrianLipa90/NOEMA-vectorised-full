from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ciel_geometry.phasenav.gate_contracts import ObservationClass, PhaseSpace
from ciel_sot_agent.pnv_rag_arm import circular_phase_alignment, query_knowledge_arm


def test_circular_phase_alignment_equal_and_opposite():
    a = np.zeros(36)
    equal = np.zeros(36)
    opposite = np.full(36, np.pi)
    assert circular_phase_alignment(a, equal) == 1.0
    assert abs(circular_phase_alignment(a, opposite)) < 1e-12


def test_rag_arm_preserves_lexical_evidence_and_adds_precise_phase_geometry():
    def fake_query(text: str, top_n: int):
        assert text == "phase memory"
        assert top_n == 2
        return [
            {
                "idx": 7,
                "filename": "memory.md",
                "themes": ["memory", "phase"],
                "affect": "neutral",
                "essence": "phase memory return",
                "similarity": 0.83,
                "phase_similarity": 0.12,
            }
        ]

    def fake_encoder(text: str):
        if text == "phase memory":
            return np.zeros(36)
        return np.full(36, np.pi / 3.0)

    observations = query_knowledge_arm(
        "phase memory",
        top_n=2,
        query_fn=fake_query,
        encoder=fake_encoder,
    )
    assert len(observations) == 1
    obs = observations[0]
    assert obs.observation_class is ObservationClass.RETRIEVED
    assert obs.phase_space is PhaseSpace.PNV_PRECISE_PHASE_36
    assert obs.canonical_evidence_eligible is True
    assert obs.confidence == 0.83
    assert obs.payload["retrieval_score"] == 0.83
    assert obs.payload["legacy_phase_similarity"] == 0.12
    assert abs(obs.payload["phase_alignment"] - 0.75) < 1e-12
    assert obs.metadata["retrieval_authority"] == "TFIDF"
    assert obs.metadata["phase_signal"] == "PNV_PRECISE_CIRCULAR_ALIGNMENT_ADDITIVE"
    assert obs.metadata["phase_encoder"] == "PHASENAV_PNV_RUNTIME_CANON_PRECISE_V1"


def test_rag_arm_rejects_non_36d_encoder_without_padding():
    def fake_query(text: str, top_n: int):
        return []

    def legacy_encoder(text: str):
        return np.zeros(24)

    try:
        query_knowledge_arm("legacy", query_fn=fake_query, encoder=legacy_encoder)
    except ValueError as exc:
        assert "canonical 36D PNV phases" in str(exc)
    else:
        raise AssertionError("24D retrieval must not be silently projected into 36D")
