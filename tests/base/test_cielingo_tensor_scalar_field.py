from __future__ import annotations

from pathlib import Path

from cielingo.tensor_scalar_field import (
    AFFECT_CHANNELS,
    SCALAR_CHANNELS,
    TENSOR_SCALAR_SCHEMA,
    TENSOR_SHAPE,
    tensor_scalar_report,
    tensor_scalar_state_from_card,
)
from cielingo.vector_surface import select_vector_cards


ROOT = Path(__file__).resolve().parents[1]


def test_tensor_scalar_state_has_real_tensor_and_imaginary_scalar():
    card = select_vector_cards(ROOT, query="word language", limit=1)[0]
    state = tensor_scalar_state_from_card(card)
    data = state.as_dict()
    assert data["schema"] == TENSOR_SCALAR_SCHEMA
    assert data["tensor_shape"] == [3, 3]
    assert len(data["real_exchange_tensor"]) == 3
    assert all(len(row) == 3 for row in data["real_exchange_tensor"])
    assert data["tensor_role"] == "real_information_exchange_tensor"
    assert data["scalar_role"] == "imaginary_context_affect_scalar"
    scalar = data["scalar_context"]
    assert scalar["channels"] == list(SCALAR_CHANNELS)
    assert set(AFFECT_CHANNELS).issubset(scalar["affect_scalars"])
    for key in ("density", "viscosity", "saturation", "semantic_time_resistance", "semantic_time_thinning"):
        assert 0.0 <= scalar[key] <= 1.0
    assert 0.0 <= scalar["colour_hue_deg"] <= 360.0


def test_tensor_scalar_report_covers_all_language_cards():
    report = tensor_scalar_report(ROOT)
    assert report["schema"] == "cielingo/tensor-scalar-field-report/v0.1"
    assert report["card_count"] == 114
    assert report["tensor_shape"] == list(TENSOR_SHAPE)
    assert report["scalar_channels"] == list(SCALAR_CHANNELS)
    assert report["affect_channels"] == list(AFFECT_CHANNELS)
    assert len(report["states"]) == 114
    assert 0.0 <= report["mean_density"] <= 1.0
    assert 0.0 <= report["mean_viscosity"] <= 1.0
    assert 0.0 <= report["mean_semantic_time_resistance"] <= 1.0


def test_tensor_scalar_query_uses_noema_lns_selection():
    report = tensor_scalar_report(ROOT, query="sarcasm excitement tension relief fear", limit=12)
    assert 1 <= report["card_count"] <= 12
    assert all(s["noema_document"]["field_roles"]["real"] == "rank_2_information_exchange_tensor" for s in report["states"])
    assert all(s["noema_document"]["field_roles"]["imaginary"] == "context_affect_scalar_medium" for s in report["states"])


def test_tensor_scalar_payloads_attach_to_cqcl_htri_noema_orchorbital():
    card = select_vector_cards(ROOT, query="context", limit=1)[0]
    state = tensor_scalar_state_from_card(card)
    assert "context_density" in state.cqcl_payload
    assert "phase_drag" in state.htri_payload
    assert "field_digest" in state.noema_document
    assert "scalar_context" in state.orchorbital_payload
