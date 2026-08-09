"""Oracle adapter for the live NOEMA shared PhaseNav surface.

This module reads the current 36-oscillator phase surface and emits typed,
provenance-bearing observations. It does not infer semantic operator vectors
from oscillator angles and performs no mutation.
"""
from __future__ import annotations

from typing import Any, Mapping

import numpy as np

from ciel_geometry.phasenav.gate_contracts import (
    ObservationClass,
    PhaseOperation,
    PhaseSpace,
    RelationalObservation,
    RelationalState,
)


_SURFACE_PROVENANCE = (
    "ciel_geometry.noema_surface_mmap:phi",
    "ciel_geometry.noema_surface_mmap:holonomy",
)


def _array(source: Mapping[str, Any], key: str, size: int | None = None) -> np.ndarray | None:
    if key not in source:
        return None
    arr = np.asarray(source[key], dtype=np.float64).reshape(-1).copy()
    if size is not None and arr.size != size:
        raise ValueError(f"surface[{key!r}] expected {size} values, got {arr.size}")
    return arr


def observe_surface(surface: Mapping[str, Any]) -> tuple[RelationalObservation, RelationalState]:
    """Convert one already-open surface mapping into typed Oracle output."""

    phi = _array(surface, "phi", 36)
    if phi is None:
        raise ValueError("surface has no phi vector")

    z = np.exp(1j * phi)
    order_parameter = float(np.abs(np.mean(z)))

    holonomy = _array(surface, "holonomy")
    closure_score: float | None = None
    holonomy_defect: float | None = None
    if holonomy is not None and holonomy.size >= 3:
        closure_score = max(0.0, min(1.0, float(holonomy[2])))
        holonomy_defect = 1.0 - closure_score

    gravity = _array(surface, "gravity")
    flavor = _array(surface, "flavor")

    tick = 0
    if "tick" in surface:
        tick_arr = np.asarray(surface["tick"]).reshape(-1)
        if tick_arr.size:
            tick = int(tick_arr[0])

    payload: dict[str, Any] = {
        "tick": tick,
        "order_parameter": order_parameter,
        "closure_score": closure_score,
    }

    # Preserve current surface slot names exactly. Do not reinterpret these as
    # ethics/closure: the current mmap contract assigns flavor[1..5] to memory
    # pressure, I/O pressure, mood, entropy/openness and mode.
    if flavor is not None and flavor.size >= 6:
        payload["flavor"] = {
            "coherence": float(flavor[0]),
            "memory_pressure": float(flavor[1]),
            "io_pressure": float(flavor[2]),
            "mood": float(flavor[3]),
            "entropy_openness": float(flavor[4]),
            "mode": float(flavor[5]),
        }

    mass: float | None = None
    if gravity is not None and gravity.size >= 8:
        mass = float(gravity[2])
        payload["gravity"] = {
            "semantic_density": float(gravity[0]),
            "tau_dilation": float(gravity[1]),
            "mass_total": mass,
            "unruh_power": float(gravity[3]),
            "cielingo_scars": float(gravity[4]),
            "agent_ok": float(gravity[5]),
            "scar_rate": float(gravity[6]),
            "scar_impact": float(gravity[7]),
        }

    phase36 = tuple(float(value) for value in phi)
    observation = RelationalObservation(
        observation_id=f"obs:noema-surface:{tick}",
        source="NOEMA_SHARED_SURFACE",
        observation_class=ObservationClass.MEASURED,
        payload=payload,
        provenance=_SURFACE_PROVENANCE,
        confidence=1.0,
        phase36=phase36,
        phase_space=PhaseSpace.OSCILLATOR_PHASE_36,
        metadata={"read_only": True},
    )

    state = RelationalState(
        identity="noema:shared-surface",
        kind="runtime_surface",
        phase36=phase36,
        phase_space=PhaseSpace.OSCILLATOR_PHASE_36,
        order_parameter=order_parameter,
        mass=mass,
        holonomy_defect=holonomy_defect,
        provenance=_SURFACE_PROVENANCE,
        authority_state="OBSERVED_ONLY",
        lifecycle="OBSERVED",
        metadata={"tick": tick, "closure_score": closure_score},
    )
    return observation, state


def observe_live_surface() -> tuple[RelationalObservation, RelationalState]:
    """Read the canonical mmap surface without modifying it."""

    from ciel_geometry.noema_surface_mmap import ensure_surface

    surface = ensure_surface()
    return observe_surface(surface)


def build_surface_inspection_operation(state: RelationalState) -> PhaseOperation:
    """Build a zero-displacement read-only operation in the state's own phase space."""

    if state.phase36 is None:
        raise ValueError("surface state has no phase36")
    return PhaseOperation(
        operation_id="op:noema-surface:inspect",
        relation_type="inspect",
        source_id=state.identity,
        phase_signature36=state.phase36,
        phase_signature_space=state.phase_space,
        mutation_class="READ_ONLY",
        evidence=state.provenance,
        provenance_requirements=state.provenance,
        authority_requirements=(),
        reversible=True,
        return_required=True,
        metadata={"oracle": "NOEMA_SHARED_SURFACE", "phase_displacement": 0.0},
    )


__all__ = ["observe_surface", "observe_live_surface", "build_surface_inspection_operation"]
