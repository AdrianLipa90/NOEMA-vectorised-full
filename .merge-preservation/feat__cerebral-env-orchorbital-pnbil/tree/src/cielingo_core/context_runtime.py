"""Read-only CIELingo context selection plus PhaseNav dynamics observation."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

import numpy as np

from ciel_geometry.phasenav.context_dynamics import (
    BlochState,
    SemanticHamiltonian,
    StableReductionGate,
    TrajectoryMemory,
)
from ciel_geometry.phasenav.formalism_logic import PhaseLogicEngine, PhaseLogicReport, PhaseLogicState
from cielingo_core.dual_context import ContextLane, DualContextStore


@dataclass(frozen=True)
class ContextObservation:
    lane: str
    source_ids: tuple[str, ...]
    energy: float
    coherence: float
    reduction_state: str
    hypothesis_only: bool = True
    execution_allowed: bool = False
    writeback_allowed: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


class ContextRuntime:
    """A read-only composition of lane retrieval and bounded dynamics."""

    def __init__(self, store: DualContextStore, *, trajectory_window: int = 32) -> None:
        self.store = store
        self.trajectories = TrajectoryMemory(window=trajectory_window)
        self.gate = StableReductionGate()
        self.phase_logic = PhaseLogicEngine()

    def observe(
        self,
        lane: ContextLane,
        query: str,
        phase_vector: Iterable[float],
        *,
        entity_id: str = "default",
        limit: int = 5,
    ) -> ContextObservation:
        if lane not in {ContextLane.PUBLIC, ContextLane.PRIVATE}:
            raise ValueError("context observations require an explicit public or private lane")
        records = self.store.query(lane, query, limit=limit)
        state = BlochState.from_phase_vector(phase_vector)
        confidence = float(np.mean([record.confidence for record in records])) if records else 0.0
        coupling = min(1.0, len(records) / max(limit, 1))
        engine = SemanticHamiltonian(detuning=confidence - 0.5, coupling=coupling)
        report = engine.evolve(state, dt=0.1, damping=0.05)
        self.trajectories.append(entity_id, report)
        history = self.trajectories.window_for(entity_id)
        mean_coherence = float(np.mean([item.coherence for item in history])) if history else 0.0
        reduction_score = min(1.0, abs(report.energy))
        reduction_state = self.gate.observe(reduction_score, report.coherence, mean_coherence)
        return ContextObservation(
            lane=lane.value,
            source_ids=tuple(record.source_id for record in records),
            energy=report.energy,
            coherence=report.coherence,
            reduction_state=reduction_state,
        )

    def observe_phase_logic(
        self,
        phase_vector: Iterable[float],
        *,
        htri_coherence: float,
        cqcl_coherence: float,
        semantic_mass: float,
        tau: float,
    ) -> PhaseLogicReport:
        """Return a pure cross-formalism diagnostic for explicit caller signals.

        The caller owns signal provenance and any downstream decision. This
        method does not write the context store or couple a report to learning.
        """
        state = PhaseLogicState.from_iterable(
            phase_vector,
            htri_coherence=htri_coherence,
            cqcl_coherence=cqcl_coherence,
            semantic_mass=semantic_mass,
            tau=tau,
        )
        return self.phase_logic.observe(state)
