from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ciel_geometry.phasenav.gate_contracts import GateDecision, ObservationClass, PhaseSpace
from ciel_geometry.phasenav.gate_fabric import evaluate_gate
from ciel_sot_agent.pnv_surface_oracle import build_surface_inspection_operation, observe_surface


def _surface():
    return {
        "phi": np.zeros(36, dtype=float),
        "holonomy": np.array([0.0, 36.0, 0.98, 0.0, 0.0, 0.0, 0.0]),
        "gravity": np.array([0.2, 1.0, 3.5, 0.0, 2.0, 1.0, 0.1, 0.25]),
        "flavor": np.array([0.99, 0.8, 0.1, 0.7, 0.2, 0.0]),
        "tick": np.array([42], dtype=np.uint64),
    }


def test_surface_observation_is_measured_and_provenanced():
    observation, state = observe_surface(_surface())
    assert observation.observation_class is ObservationClass.MEASURED
    assert observation.canonical_evidence_eligible is True
    assert observation.phase_space is PhaseSpace.OSCILLATOR_PHASE_36
    assert state.phase_space is PhaseSpace.OSCILLATOR_PHASE_36
    assert len(state.phase36 or ()) == 36
    assert state.order_parameter == 1.0
    assert abs((state.holonomy_defect or 0.0) - 0.02) < 1e-12


def test_surface_slot_contract_is_not_mislabeled():
    observation, _ = observe_surface(_surface())
    flavor = observation.payload["flavor"]
    assert flavor["memory_pressure"] == 0.8
    assert flavor["io_pressure"] == 0.1
    assert flavor["mood"] == 0.7
    assert flavor["entropy_openness"] == 0.2
    assert "ethics" not in flavor
    assert "closure" not in flavor


def test_surface_inspection_operation_stays_in_oscillator_space_and_opens():
    observation, state = observe_surface(_surface())
    operation = build_surface_inspection_operation(state)
    assert operation.phase_signature_space is PhaseSpace.OSCILLATOR_PHASE_36
    gate = evaluate_gate(operation, state)
    assert gate.decision is GateDecision.OPEN
    assert gate.metrics["phase_space_match"] == 1.0
    assert set(operation.evidence) == set(observation.provenance)


def test_surface_rejects_wrong_phi_length():
    surface = _surface()
    surface["phi"] = np.zeros(24)
    try:
        observe_surface(surface)
    except ValueError as exc:
        assert "expected 36" in str(exc)
    else:
        raise AssertionError("24D surface must not be silently accepted")
