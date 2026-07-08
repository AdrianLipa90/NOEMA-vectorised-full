from __future__ import annotations

from pathlib import Path
import sys
import types

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM"
PKG_RUNTIME = PKG / "ciel_omega"
if str(PKG) not in sys.path:
    sys.path.insert(0, str(PKG))
if str(PKG_RUNTIME) not in sys.path:
    sys.path.insert(0, str(PKG_RUNTIME))

bootstrap_runtime_mod = types.ModuleType("bootstrap_runtime")
bootstrap_runtime_mod.ensure_runtime_paths = lambda _path: PKG_RUNTIME
sys.modules.setdefault("bootstrap_runtime", bootstrap_runtime_mod)

orchestrator_mod = types.ModuleType("ciel_orchestrator")
orchestrator_mod.CIELOrchestrator = None
sys.modules.setdefault("ciel_orchestrator", orchestrator_mod)

middleware_mod = types.ModuleType("inference.middleware")
middleware_mod.build_orbital_ethical_inference_surface = lambda **kwargs: {"gguf_enabled": bool(kwargs.get("backend")), "status": "ok"}
middleware_mod.build_inference_seed = lambda flow_entry, target_phase=None: {
    "target_phase": float(target_phase or 0.0),
    "mood": float((flow_entry or {}).get("mood", 0.0) or 0.0),
    "soul_invariant": float((flow_entry or {}).get("soul_invariant", 0.0) or 0.0),
    "dominant_affect": "neutral",
    "intention": (flow_entry or {}).get("intention", []),
}
sys.modules.setdefault("inference", types.ModuleType("inference"))
sys.modules["inference.middleware"] = middleware_mod

import ciel_omega.ciel_client as ciel_client_mod
import ciel_omega.ciel_inference_surface as ciel_surface_mod
import ciel_omega.unified_system as unified_system_mod


FAKE_STATE = {
    "sector_memory": {
        "governed_retrieval": {
            "ranked": [
                {"channel": "m3", "text": "surface memory line", "holonomy_quality": 0.9, "phase_alignment": 0.8},
            ],
            "by_channel": {"m3": [{"text": "surface memory line"}]},
        }
    },
    "semantic_labels": ["surface", "overlay"],
    "memory_score": 0.62,
    "nonlocal_runtime": {"semantic_key": "surface bridge", "coherent_fraction": 0.81},
    "euler_bridge": {"memory_semantic_key": "surface bridge", "euler_metrics": {"target_phase": 0.11, "closure_score": 0.44}},
    "runtime_policy": {"response_strategy": "truth-aligned-user-intent", "durable_write_allowed": True},
    "lingo_frame": {
        "summary": "CIELingo|concepts=surface|operators=overlay|deictic=Now:relative_anchor|unresolved=Now|factual=no|noema_conf=0.660",
        "concept_tokens": ["surface"],
        "operator_tokens": ["overlay"],
        "deictic_frame": {"anchors": [], "relative_anchors": [{"operator": "Now", "surface": "now", "resolution_state": "relative_anchor"}]},
        "noema_route": {"confidence": 0.66, "factual_validation_required": False},
        "phase_projection": {"target_phase": 0.11, "target_phase_shift": 0.02, "phase_confidence": 0.67},
        "tau_bridge": {"tau_gradient_mean": 0.18, "imaginal_drive": 0.31, "tau_curvature_rms": 0.04},
    },
    "intention_vector": [0.1, 0.2, 0.3],
    "simulation": {"coherence": [0.8, 0.9]},
    "cognition": {"phase": 0.2},
    "affect": {"tone": "calm"},
}


class FakeOrchestrator:
    def __init__(self, boot: bool = True) -> None:
        self.boot = boot

    def ping(self):
        return {"status": "ok", "timestamp": "2026-07-06T00:00:00Z", "schumann_hz": 7.83}

    def status_snapshot(self):
        return {"status": "ok", "boot": self.boot}

    def process(self, text: str, verbose: bool = False):
        return {"status": "ok", "ciel_state": FAKE_STATE, "ethics_passed": True, "soul_measure": 0.77}

    def shutdown(self):
        return None


class FakePrimary:
    def __init__(self, *args, **kwargs) -> None:
        self.name = "fake-primary"
        self.model_path = "fake.gguf"

    def generate_reply(self, dialogue, ciel_state):
        return "surface reply"


class FakeAux:
    def __init__(self, *args, **kwargs) -> None:
        self.name = "fake-aux"

    def analyse_state(self, ciel_state, candidate_reply):
        return {"backend": self.name, "available": True, "status": "ok", "coherence": 0.88}


class FakeOverlay:
    def __init__(self, primary_backend, analysis_backend=None, validator_backend=None, profile="standard", system_prompt="") -> None:
        self.primary_backend = primary_backend
        self.analysis_backend = analysis_backend
        self.validator_backend = validator_backend
        self.profile = profile
        self.system_prompt = system_prompt
        self.last = None

    def generate_report(self, dialogue, ciel_state):
        self.last = {"dialogue": dialogue, "ciel_state": ciel_state}
        return type(
            "Report",
            (),
            {
                "reply": "surface reply",
                "to_dict": lambda self: {"reply": "surface reply", "analysis": {"status": "ok"}, "profile": "standard"},
            },
        )()


class FakeBridge:
    def step(self, text, metadata=None):
        return type(
            "Cycle",
            (),
            {
                "input_text": text,
                "memory_semantic_key": "surface bridge",
                "memory_cycle_index": 12,
                "core_metrics": {"closure_score": 0.44},
                "vocabulary_metrics": {"vocab": 1.0},
                "euler_metrics": {"target_phase": 0.11},
            },
        )()


class FakeClient:
    def __init__(self, *args, **kwargs) -> None:
        self.orchestrator = FakeOrchestrator()

    def process(self, text, use_llm=False):
        payload = {
            "status": "ok",
            "ciel_state": FAKE_STATE,
            "ethics_passed": True,
            "soul_measure": 0.77,
            "llm_response": "surface reply" if use_llm else None,
            "llm_overlay": {"reply": "surface reply", "analysis": {"status": "ok"}} if use_llm else None,
        }
        return payload

    def handshake(self):
        return {"status": "ok", "surface": "CIELClient"}

    def shutdown(self):
        return None


def test_ciel_client_exposes_overlay_payload(monkeypatch):
    monkeypatch.setattr(ciel_client_mod, "CIELOrchestrator", FakeOrchestrator)
    monkeypatch.setattr(ciel_client_mod, "GGUFPrimaryBackend", FakePrimary)
    monkeypatch.setattr(ciel_client_mod, "GGUFAuxBackend", FakeAux)
    monkeypatch.setattr(ciel_client_mod, "GGUFOverlay", FakeOverlay)

    client = ciel_client_mod.CIELClient(model_path="fake.gguf", boot=False)
    result = client.process("hej", use_llm=True)

    assert result["llm_response"] == "surface reply"
    assert result["llm_overlay"]["reply"] == "surface reply"
    assert result["llm_overlay"]["analysis"]["status"] == "ok"
    assert result["handshake"]["gguf_overlay_enabled"] is True


def test_ciel_inference_surface_exposes_overlay_payload(monkeypatch):
    monkeypatch.setattr(ciel_surface_mod, "CIELOrchestrator", FakeOrchestrator)
    monkeypatch.setattr(ciel_surface_mod, "GGUFPrimaryBackend", FakePrimary)
    monkeypatch.setattr(ciel_surface_mod, "GGUFAuxBackend", FakeAux)
    monkeypatch.setattr(ciel_surface_mod, "GGUFOverlay", FakeOverlay)

    surface = ciel_surface_mod.CIELInferenceSurface(model_path="fake.gguf", boot=False)
    result = surface.process("hej", use_llm=True)

    assert result["gguf_overlay_enabled"] is True
    assert result["llm_overlay"]["reply"] == "surface reply"
    assert result["inference_runtime"]["gguf_enabled"] is True


def test_ciel_inference_surface_uses_runtime_response_text(monkeypatch):
    calls = []

    class TracingOverlay:
        def __init__(
            self,
            primary_backend,
            analysis_backend=None,
            validator_backend=None,
            profile="standard",
            system_prompt="",
        ) -> None:
            self.primary_backend = primary_backend
            self.analysis_backend = analysis_backend
            self.validator_backend = validator_backend
            self.profile = profile
            self.system_prompt = system_prompt

        def generate_report(self, dialogue, ciel_state, candidate_reply=None):
            calls.append(candidate_reply)
            reply = candidate_reply or "backend fallback"

            class _Report:
                def __init__(self, reply_text: str, candidate: str | None) -> None:
                    self.reply = reply_text
                    self._candidate_reply = candidate

                def to_dict(self) -> dict[str, object]:
                    return {
                        "reply": self.reply,
                        "candidate_reply": self._candidate_reply,
                        "analysis": {"status": "ok"},
                    }

            return _Report(reply, candidate_reply)

    def runtime_surface(**kwargs):
        return {
            "gguf_enabled": bool(kwargs.get("backend")),
            "status": "ok",
            "response_text": "runtime answer",
        }

    monkeypatch.setattr(ciel_surface_mod, "CIELOrchestrator", FakeOrchestrator)
    monkeypatch.setattr(ciel_surface_mod, "GGUFPrimaryBackend", FakePrimary)
    monkeypatch.setattr(ciel_surface_mod, "GGUFAuxBackend", FakeAux)
    monkeypatch.setattr(ciel_surface_mod, "GGUFOverlay", TracingOverlay)
    monkeypatch.setattr(ciel_surface_mod, "build_orbital_ethical_inference_surface", runtime_surface)

    surface = ciel_surface_mod.CIELInferenceSurface(model_path="fake.gguf", boot=False)
    result = surface.process("hej", use_llm=True)

    assert calls == [None, "runtime answer"]
    assert result["llm_overlay"]["reply"] == "runtime answer"
    assert result["llm_overlay"]["candidate_reply"] == "runtime answer"
    assert result["inference_runtime"]["response_text"] == "runtime answer"
    assert result["use_llm"] is True


def test_unified_system_cycle_carries_overlay_payload():
    system = unified_system_mod.UnifiedSystem(
        orchestrator=FakeOrchestrator(),
        client=FakeClient(),
        bridge=FakeBridge(),
    )

    result = system.run_text_cycle("hej", use_llm=True)

    assert result["surface"] == "UnifiedSystem"
    assert result["llm_response"] == "surface reply"
    assert result["llm_overlay"]["reply"] == "surface reply"
    assert result["orchestrator_status"] == "ok"
