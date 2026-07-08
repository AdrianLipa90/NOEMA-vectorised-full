from __future__ import annotations

from pathlib import Path

from cielingo.vector_surface import VECTOR_DIM, VECTOR_COMPONENTS, select_vector_cards, vector_surface_report, vectorize_card


ROOT = Path(__file__).resolve().parents[1]


def test_vector_schema_is_36d_and_named():
    assert VECTOR_DIM == 36
    assert len(VECTOR_COMPONENTS) == 36
    assert VECTOR_COMPONENTS[0] == "semantic_mass"
    assert VECTOR_COMPONENTS[-1] == "quantum_entanglement_entropy"


def test_single_card_vector_exports_all_adapters():
    card = select_vector_cards(ROOT, query="word language", limit=1)[0]
    vec = vectorize_card(card)
    data = vec.as_dict()
    assert data["schema"] == "cielingo/vector-surface/v0.1"
    assert data["vector_dim"] == 36
    assert len(data["vector"]) == 36
    assert all(0.0 <= x <= 1.0 for x in data["vector"])
    assert {"resonance", "superposition", "quantum_flux", "entanglement", "coherence"}.issubset(data["cqcl_quantum_variables"])
    assert data["htri_state"]["base_frequency_hz"] == 7.83
    assert "vector_digest" in data["noema_document"]
    assert data["orchorbital_payload"]["schema"] == "cielingo/orchorbital-vector-payload/v0.1"


def test_vector_surface_report_covers_all_lns_cards():
    report = vector_surface_report(ROOT)
    assert report["schema"] == "cielingo/vector-surface-report/v0.1"
    assert report["card_count"] == 114
    assert report["vector_dim"] == 36
    assert report["compatibility"] == {"cqcl": True, "htri": True, "noema": True, "orchorbital": True}
    assert len(report["vectors"]) == 114
    assert report["htri_oscillators"] == 36
    assert report["spare_oscillators"] == max(0, 36 - report["card_count"])


def test_vector_surface_query_uses_noema_lns_selection():
    report = vector_surface_report(ROOT, query="infinitive modal potential", limit=8)
    assert 1 <= report["card_count"] <= 8
    assert all(v["vector_dim"] == 36 for v in report["vectors"])
