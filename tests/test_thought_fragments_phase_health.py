from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "ciel_sot_agent" / "thought_fragments.py"


def _load_module():
    src_path = str(Path(__file__).resolve().parents[1] / "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

    spec = importlib.util.spec_from_file_location("ciel_sot_agent.thought_fragments", MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["ciel_sot_agent.thought_fragments"] = module
    spec.loader.exec_module(module)
    return module


module = _load_module()


def _durable(confidence: float, status: str = "durable"):
    return module.DurableMemoryObject(
        durable_id="dur:test",
        source_candidate_id="cand:test",
        memory_type="semantic",
        summary="summary",
        semantic_summary="semantic:summary",
        affective_signature="calm",
        phase_anchor="phase:test",
        qualisensing_residue="quali:test",
        provenance_refs=["evt:test"],
        noema_refs=["noema:test"],
        timeline_refs=["phase:test"],
        crosslink_refs=["cross:test"],
        consolidation_confidence=confidence,
        reconsolidation_needed=False,
        status=status,
        ts_created="2026-07-06T00:00:00Z",
        ts_updated="2026-07-06T00:00:00Z",
    )


def test_durable_health_tracks_phase_weight_bundle() -> None:
    healthy_state = {
        "system_health": 0.92,
        "coherence_index": 0.94,
        "closure_penalty": 0.09,
        "lingo_noema_confidence": 0.91,
        "dominant_emotion": "warmth",
        "ts": "2026-07-06T00:00:00Z",
    }
    unhealthy_state = {
        "system_health": 0.38,
        "coherence_index": 0.42,
        "closure_penalty": 0.64,
        "lingo_noema_confidence": 0.41,
        "dominant_emotion": "fear",
        "ts": "2026-07-06T00:00:01Z",
    }

    healthy_link = module.NoemaMemoryLink(
        link_id="link:healthy",
        memory_id="dur:test",
        noema_object_id="noema:healthy",
        relation_type="semantic_anchor",
        link_weight=0.88,
        activation_policy="phase_resonant",
        provenance_refs=["evt:test"],
        ts="2026-07-06T00:00:00Z",
    )
    unhealthy_link = module.NoemaMemoryLink(
        link_id="link:unhealthy",
        memory_id="dur:test",
        noema_object_id="noema:unhealthy",
        relation_type="context_anchor",
        link_weight=0.28,
        activation_policy="phase_pending",
        provenance_refs=["evt:test"],
        ts="2026-07-06T00:00:01Z",
    )

    healthy_updated, healthy_health = module.assess_durable_memory_health(
        healthy_state,
        durable=_durable(0.91, status="promoted"),
        noema_link=healthy_link,
    )
    unhealthy_updated, unhealthy_health = module.assess_durable_memory_health(
        unhealthy_state,
        durable=_durable(0.61),
        noema_link=unhealthy_link,
    )

    assert healthy_health.health_state == "healthy"
    assert healthy_health.reconsolidation_needed is False
    assert healthy_updated.status == "promoted"
    assert unhealthy_health.health_state == "reconsolidate"
    assert unhealthy_health.reconsolidation_needed is True
    assert unhealthy_updated.status == "reconsolidate"
    assert healthy_health.health_score > unhealthy_health.health_score
    assert healthy_health.health_reason == "stable"
    assert "candidate_confidence_low" in unhealthy_health.health_reason


def test_memory_link_relation_type_is_phase_weighted() -> None:
    healthy_state = {
        "system_health": 0.91,
        "coherence_index": 0.93,
        "closure_penalty": 0.08,
        "lingo_noema_confidence": 0.90,
        "dominant_emotion": "warmth",
        "cycle_index": 2,
        "lingo_frame": {"noema_route": {"bundle": {"confidence": 0.72}}},
        "ts": "2026-07-06T00:00:00Z",
    }
    healthy_durable = _durable(0.92, status="promoted")
    healthy_link = module.build_noema_memory_link(healthy_state, durable=healthy_durable)

    soft_state = {
        "system_health": 0.53,
        "coherence_index": 0.57,
        "closure_penalty": 0.31,
        "lingo_noema_confidence": 0.49,
        "dominant_emotion": "neutral",
        "cycle_index": 3,
        "lingo_frame": {"noema_route": {"bundle": {"confidence": 0.49}}},
        "ts": "2026-07-06T00:00:01Z",
    }
    soft_durable = _durable(0.64)
    soft_link = module.build_noema_memory_link(soft_state, durable=soft_durable)

    assert healthy_link.relation_type == "semantic_anchor"
    assert soft_link.relation_type == "context_anchor"
    assert 0.0 <= healthy_link.link_weight <= 1.0
    assert 0.0 <= soft_link.link_weight <= 1.0
    assert healthy_link.link_weight > soft_link.link_weight
