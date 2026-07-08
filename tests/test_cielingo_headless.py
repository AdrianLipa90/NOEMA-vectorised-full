from __future__ import annotations

from types import SimpleNamespace

from src.ciel_geometry import cielingo_headless as headless_mod


def test_generate_headless_response_uses_engine_answer(monkeypatch) -> None:
    fake_frame = {
        "summary": "CIELingo|concepts=bridge|operators=memory|deictic=-|unresolved=-|factual=no|noema_conf=0.710",
        "phase_nav": {"operator": "MEMORY", "holonomy": 0.5, "urgency": 0.1},
        "concept_tokens": ["bridge"],
        "operator_tokens": ["memory"],
        "deictic_frame": {"anchors": [], "relative_anchors": []},
        "unresolved": [],
        "noema_route": {"confidence": 0.71, "factual_validation_required": False},
        "mnemonic_atlas": {"mnemonic_pressure": 0.2},
        "phase_projection": {"target_phase": 0.5, "target_phase_shift": 0.5, "phase_confidence": 0.7},
        "tau_bridge": {"tau_gradient_mean": 0.12, "imaginal_drive": 0.44, "tau_curvature_rms": 0.08},
    }

    class FakeEngine:
        def answer(self, question: str, k: int = 5):
            return {
                "answer": "headless answer",
                "operator": "MEMORY",
                "decision": {"action": "retrieve_memory", "confidence": "medium"},
                "sources": [{"text": "memory source", "sim": 0.81, "source": "phase-memory"}],
            }

    monkeypatch.setattr(headless_mod, "_engine_for", lambda _path: FakeEngine())
    monkeypatch.setattr(headless_mod, "build_lingo_frame", lambda *args, **kwargs: dict(fake_frame))
    monkeypatch.setattr(headless_mod, "render_lingo_summary", lambda frame: frame["summary"])
    monkeypatch.setattr(headless_mod, "render_phasenav_summary", lambda frame: "PhaseNav|op=MEMORY")

    result = headless_mod.generate_headless_response("hej", ciel_state={"language": "pl"})

    assert result.schema == headless_mod.HEADLESS_SCHEMA
    assert result.answer == "headless answer"
    assert result.operator == "MEMORY"
    assert result.decision["action"] == "retrieve_memory"
    assert result.lingo_summary.startswith("CIELingo|")
    assert result.phase_summary == "PhaseNav|op=MEMORY"
    assert result.sources[0]["text"] == "memory source"


def test_headless_system_message_renders_block(monkeypatch) -> None:
    response = SimpleNamespace(
        schema=headless_mod.HEADLESS_SCHEMA,
        generated_at="2026-07-06T00:00:00Z",
        render_block=lambda: "CIELINGO_HEADLESS:\n  answer: | \n    headless answer",
    )
    monkeypatch.setattr(headless_mod, "generate_headless_response", lambda *args, **kwargs: response)

    _, system_message = headless_mod.build_headless_system_message("hej", ciel_state={"language": "pl"})

    assert "NOEMA_CIELINGO_HEADLESS" in system_message
    assert "headless answer" in system_message
