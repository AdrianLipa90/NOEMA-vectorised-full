from __future__ import annotations

from pathlib import Path

from src.ciel_sot_agent.knowledge_action_system import KnowledgeActionSystem, run_knowledge_action_system


def _system(tmp_path: Path, lingo_bundle: dict[str, object], doctor_bundle: dict[str, object], policy_bundle: dict[str, object]) -> KnowledgeActionSystem:
    return KnowledgeActionSystem(
        root=tmp_path,
        retriever=lambda text, root, top_k: {
            "root": str(root),
            "wave_hits": [{"text": f"wave:{text}", "score": 0.9}],
            "chat_hits": [{"text": f"chat:{text}", "score": 0.8}],
            "memory_context": "## memory",
            "total_hits": 2,
            "evidence_strength": 0.9,
        },
        lingo_builder=lambda text, **kwargs: dict(lingo_bundle, text=text, phase_nav={"operator": "IDENTITY"}),
        doctor_builder=lambda root: doctor_bundle,
        policy_builder=lambda control_profile=None, truth_axis="truth": dict(policy_bundle, mode=policy_bundle.get("mode", "standard"), response_axis=f"{truth_axis}-aligned-user-intent"),
    )


def test_run_knowledge_action_system_allows_when_gates_clear(tmp_path: Path) -> None:
    system = _system(
        tmp_path,
        {"composition_valid": True, "projection_confidence": 0.92},
        {"status": "PASS", "findings": [], "file_count": 123},
        {"mode": "standard", "truth_over_smoothing": True},
    )

    trace = system.run("hello world")

    assert trace.decision["action"] == "allow"
    assert trace.ui["suggested_next_step"] == "execute"
    assert trace.retrieval["total_hits"] == 2
    assert trace.sapiens["decision"] == "allow"
    assert trace.ui["phase_nav"]["operator"] == "IDENTITY"


def test_run_knowledge_action_system_defers_in_safe_mode(tmp_path: Path) -> None:
    system = _system(
        tmp_path,
        {"composition_valid": True, "projection_confidence": 0.88},
        {"status": "PASS", "findings": [], "file_count": 123},
        {"mode": "safe", "truth_over_smoothing": True},
    )

    trace = system.run("hello world")

    assert trace.decision["action"] == "defer"
    assert trace.decision["reason"] == "safe_mode_read_only"
    assert "safe_mode" in trace.decision["signals"]
    assert trace.ui["suggested_next_step"] == "collect_more_evidence"


def test_run_knowledge_action_system_repairs_invalid_composition(tmp_path: Path) -> None:
    system = _system(
        tmp_path,
        {"composition_valid": False, "projection_confidence": 0.91},
        {"status": "PASS", "findings": [], "file_count": 123},
        {"mode": "standard", "truth_over_smoothing": True},
    )

    trace = system.run("hello world")

    assert trace.decision["action"] == "repair"
    assert trace.decision["reason"] == "lingo_invalid_or_low_confidence"
    assert "composition_invalid" in trace.decision["signals"]
    assert trace.ui["suggested_next_step"] == "repair_surfaces"


def test_run_knowledge_action_system_blocks_when_binding_is_blocked(tmp_path: Path) -> None:
    system = _system(
        tmp_path,
        {"composition_valid": True, "projection_confidence": 0.88, "binding_blocked": True},
        {"status": "PASS", "findings": [], "file_count": 123},
        {"mode": "standard", "truth_over_smoothing": True},
    )

    trace = system.run("hello world")

    assert trace.decision["action"] == "block"
    assert trace.decision["reason"] == "binding_blocked"
    assert trace.ui["suggested_next_step"] == "halt_and_review"


def test_convenience_wrapper_returns_serializable_trace(tmp_path: Path) -> None:
    system = _system(
        tmp_path,
        {"composition_valid": True, "projection_confidence": 0.88},
        {"status": "PASS", "findings": [], "file_count": 123},
        {"mode": "standard", "truth_over_smoothing": True},
    )

    trace = run_knowledge_action_system("hello world", system=system)

    payload = trace.as_dict()
    assert payload["root"] == str(tmp_path)
    assert payload["query"] == "hello world"
    assert payload["decision"]["action"] == "allow"
