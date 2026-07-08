from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM"
if str(PKG) not in sys.path:
    sys.path.insert(0, str(PKG))

from ciel_omega.ciel.gguf_overlay import GGUFOverlay
from ciel_omega.ciel.engine import CielEngine


FAKE_STATE = {
    "sector_memory": {
        "governed_retrieval": {
            "ranked": [
                {
                    "channel": "m3",
                    "text": "semantic retrieval prefers repeated meaning",
                    "holonomy_quality": 0.88,
                    "phase_alignment": 0.91,
                }
            ],
            "by_channel": {
                "m3": [
                    {"text": "semantic retrieval prefers repeated meaning"},
                ]
            },
        }
    },
    "semantic_labels": ["memory", "retrieval", "speech"],
    "memory_score": 0.73,
    "nonlocal_runtime": {"semantic_key": "memory bridge", "coherent_fraction": 0.84},
    "euler_bridge": {"memory_semantic_key": "memory bridge"},
    "runtime_policy": {"response_strategy": "truth-aligned-user-intent", "durable_write_allowed": True},
    "immune_surface": {
        "exists": True,
        "coherence_index": 0.87,
        "ethical_score": 0.91,
        "closure_penalty": 0.12,
        "soul_invariant": 0.77,
        "operating_mode": "standard",
    },
    "lingo_frame": {
        "summary": "CIELingo|concepts=bridge, memory|operators=through|deictic=Now:relative_anchor|unresolved=Now|factual=no|noema_conf=0.710",
        "concept_tokens": ["bridge", "memory"],
        "operator_tokens": ["through"],
        "unresolved": ["Now"],
        "deictic_frame": {
            "anchors": [],
            "relative_anchors": [
                {"operator": "Now", "surface": "now", "resolution_state": "relative_anchor"}
            ],
        },
        "noema_route": {"confidence": 0.71, "factual_validation_required": False},
        "phase_projection": {"target_phase": 0.0, "target_phase_shift": 0.0, "phase_confidence": 0.66},
        "tau_bridge": {
            "tau_gradient_mean": 0.12,
            "imaginal_drive": 0.44,
            "tau_curvature_rms": 0.08,
        },
    },
    "intention_vector": [0.1, 0.2, 0.3],
    "simulation": {"coherence": [0.8, 0.9]},
    "cognition": {"phase": 0.2},
    "affect": {"tone": "calm"},
}


class FakePrimary:
    name = "fake-primary"

    def __init__(self) -> None:
        self.calls = []

    def generate_reply(self, dialogue, ciel_state):
        self.calls.append((dialogue, ciel_state))
        return "overlay reply"


class FakeAux:
    def __init__(self, name: str) -> None:
        self.name = name
        self.calls = []

    def analyse_state(self, ciel_state, candidate_reply):
        self.calls.append((ciel_state, candidate_reply))
        return {
            "backend": self.name,
            "available": True,
            "status": "ok",
            "coherence": 0.91,
            "helpfulness": 0.84,
            "keywords": ["overlay", "semantic"],
            "emotion": "calm",
        }


def test_overlay_builds_prompt_from_live_state():
    primary = FakePrimary()
    analysis = FakeAux("analysis")
    validator = FakeAux("validator")
    overlay = GGUFOverlay(
        primary_backend=primary,
        analysis_backend=analysis,
        validator_backend=validator,
        profile="standard",
        system_prompt="You are CIEL/Ω.",
    )

    dialogue = [{"role": "user", "content": "hej, przeprowadź overlay"}]
    report = overlay.generate_report(dialogue, FAKE_STATE)

    assert report.reply == "overlay reply"
    assert "GGUF overlay profile: standard" in report.overlay_prompt
    assert "PhaseNav immune gate:" in report.overlay_prompt
    assert "Immune surface:" in report.overlay_prompt
    assert "PhaseNav brief:" in report.overlay_prompt
    assert "Retrieved semantic memory:" in report.overlay_prompt
    assert "CIELingo summary:" in report.overlay_prompt
    assert "Memory score: 0.730" in report.overlay_prompt
    assert report.state_digest["immune_surface"]["exists"] is True
    assert report.state_digest["phasenav"]["exists"] is True
    assert report.analysis["status"] == "ok"
    assert report.validator["status"] == "ok"
    assert report.semantic_speech["text"].startswith("Retrieved semantic memory:")
    assert report.prompt_messages[0]["role"] == "system"
    assert report.prompt_messages[1]["content"] == "hej, przeprowadź overlay"
    assert primary.calls
    assert analysis.calls
    assert validator.calls
    assert overlay.last_report is report
    assert dialogue == [{"role": "user", "content": "hej, przeprowadź overlay"}]


def test_engine_interact_uses_overlay_report():
    primary = FakePrimary()
    analysis = FakeAux("analysis")
    overlay = GGUFOverlay(
        primary_backend=primary,
        analysis_backend=analysis,
        profile="standard",
        system_prompt="You are CIEL/Ω.",
    )

    engine = CielEngine(language_backend=overlay, aux_backend=analysis)
    engine.step = lambda *args, **kwargs: FAKE_STATE  # type: ignore[assignment]

    result = engine.interact(
        "hej",
        [{"role": "user", "content": "hej"}],
        use_aux_analysis=True,
    )

    assert result["status"] == "ok"
    assert result["reply"] == "overlay reply"
    assert "llm_overlay" in result
    assert result["llm_overlay"]["reply"] == "overlay reply"
    assert result["analysis"]["backend"] == "analysis"
    assert result["analysis"]["status"] == "ok"
