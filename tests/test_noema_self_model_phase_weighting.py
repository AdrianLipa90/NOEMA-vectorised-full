from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "noema_self_model.py"


def _load_self_model_module():
    src_path = str(Path(__file__).resolve().parents[1] / "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

    for name, attr in {
        "ciel_geometry.noema_surface_mmap": {
            "ensure_surface": lambda: {
                "tick": [0],
                "phi": [0.0, 0.0, 0.0, 0.0],
                "omega": [0.0, 0.0, 0.0, 0.0],
                "flavor": [0.0] * 6,
                "gravity": [0.0] * 8,
            },
            "N_OSCILLATORS": 4,
        },
        "ciel_geometry.agent_attractor": {
            "agent_attractor_state": lambda _phi: {"coherence": 0.5, "m2_coherence": 0.5},
        },
        "ciel_geometry.noema_registry": {
            "registry": types.SimpleNamespace(register=lambda *_a, **_k: "token", heartbeat=lambda *_a, **_k: None),
        },
    }.items():
        stub = sys.modules.get(name)
        if stub is None:
            stub = types.ModuleType(name)
            for key, value in attr.items():
                setattr(stub, key, value)
            sys.modules[name] = stub

    spec = importlib.util.spec_from_file_location("noema_self_model", SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["noema_self_model"] = module
    spec.loader.exec_module(module)
    return module


module = _load_self_model_module()


class _StubDB:
    def __init__(self, baselines: dict[str, tuple[float, float, int]]) -> None:
        self.baselines = baselines
        self.writes: list[tuple[str, float, float, float, float, bool]] = []

    def get_baseline_stats(self, metric: str) -> tuple[float, float, int]:
        return self.baselines.get(metric, (0.0, 0.0, 0))

    def write_drift(
        self,
        metric: str,
        baseline_mean: float,
        baseline_std: float,
        current: float,
        z_score: float,
        anomaly: bool,
    ) -> None:
        self.writes.append((metric, baseline_mean, baseline_std, current, z_score, anomaly))


def test_phase_metadata_classifies_locked_vs_saturated() -> None:
    locked_metrics = {
        "coherence_index": 0.94,
        "agent_coherence": 0.93,
        "m2_coherence": 0.91,
        "euler_residual": 0.05,
        "mass_total": 2.7,
        "mood": 0.82,
        "openness": 0.71,
    }
    locked = module._phase_weight_metadata({}, locked_metrics)
    locked_bundle = module._phase_weight_bundle({}, locked_metrics)

    saturated_metrics = {
        "coherence_index": 0.18,
        "agent_coherence": 0.22,
        "m2_coherence": 0.19,
        "euler_residual": 1.20,
        "mass_total": 0.3,
        "mood": 0.21,
        "openness": 0.12,
    }
    saturated = module._phase_weight_metadata({}, saturated_metrics)
    saturated_bundle = module._phase_weight_bundle({}, saturated_metrics)

    assert locked["phase_lane"] == "phase_locked"
    assert saturated["phase_lane"] == "phase_saturated"
    assert 0.0 <= locked["phase_alignment"] <= 1.0
    assert 0.0 <= locked["projection_confidence"] <= 1.0
    assert "conflict" in saturated["semantic_labels"]
    assert locked_bundle["composite"] > saturated_bundle["composite"]
    assert locked_bundle["stability"] > saturated_bundle["stability"]
    assert locked_bundle["contradiction_risk"] < saturated_bundle["contradiction_risk"]


def test_detect_anomalies_uses_phase_bundle_threshold() -> None:
    metrics = {"phi_mean": 0.21}
    baselines = {"phi_mean": (0.0, 0.1, 24)}

    stable_db = _StubDB(baselines)
    stable_bundle = {
        "stability": 0.97,
        "contradiction_risk": 0.04,
        "composite": 0.92,
    }
    stable_anomalies = module.detect_anomalies(
        metrics,
        stable_db,
        threshold=3.0,
        phase_bundle=stable_bundle,
    )

    unstable_db = _StubDB(baselines)
    unstable_bundle = {
        "stability": 0.11,
        "contradiction_risk": 0.89,
        "composite": 0.17,
    }
    unstable_anomalies = module.detect_anomalies(
        metrics,
        unstable_db,
        threshold=3.0,
        phase_bundle=unstable_bundle,
    )

    assert stable_anomalies == []
    assert len(stable_db.writes) == 1
    assert unstable_anomalies and unstable_anomalies[0]["metric"] == "phi_mean"
    assert unstable_anomalies[0]["threshold"] < 3.0
