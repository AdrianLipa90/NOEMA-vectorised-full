"""PhaseNav solver — find operator paths between concepts through phase space.

Maps concept → phase → operator edge → next concept via 33×24D algebra.
"""
from __future__ import annotations
import math
from dataclasses import dataclass, field
from typing import Any

from .loader import PhaseNavData, load_phasenav

@dataclass
class PhaseNavStep:
    source_card_id: str
    target_card_id: str
    operator_hook: str
    operator_card_id: str
    phase_start: float
    phase_end: float
    phase_delta: float
    holonomic_viscosity: float
    phasenav_affordance: float
    transition_lane: str
    path_integral: float = 0.0


@dataclass
class PhaseNavTrace:
    steps: list[PhaseNavStep] = field(default_factory=list)
    total_path_integral: float = 0.0
    mean_viscosity: float = 0.0
    mean_affordance: float = 0.0
    card_sequence: list[str] = field(default_factory=list)


@dataclass
class PhaseNavSolver:
    data: PhaseNavData

    @classmethod
    def load(cls, base_path=None) -> PhaseNavSolver:
        return cls(data=load_phasenav(base_path))

    def get_phase(self, card_id: str) -> float | None:
        cp = self.data.concept_phases.get(card_id)
        if cp:
            value = cp.get("geometric_phase_rad")
            return float(value) if value is not None else None
        nm = self.data.name_mass_by_card_id.get(card_id)
        if nm:
            value = nm.get("geometric_phase_rad")
            return float(value) if value is not None else None
        return None

    def get_orbit(self, card_id: str) -> list[float] | None:
        orbit = self.data.orbits.get(card_id)
        return [float(x) for x in orbit] if orbit else None

    def get_operator_vector(self, op_id: str) -> list[float] | None:
        vector = self.data.operator_vectors.get(op_id)
        return [float(x) for x in vector] if vector else None

    def best_edge_from(self, concept_id: str) -> dict | None:
        edges = self.data.edges_by_concept.get(concept_id)
        if not edges:
            return None
        valid_edges = [edge for edge in edges if edge.get("phasenav_affordance") is not None]
        if not valid_edges:
            return None
        return max(valid_edges, key=lambda e: float(e["phasenav_affordance"]))

    def trace(self, card_ids: list[str]) -> PhaseNavTrace:
        trace = PhaseNavTrace(card_sequence=list(card_ids))
        for i in range(len(card_ids) - 1):
            step = self._step_between(card_ids[i], card_ids[i + 1])
            if step:
                trace.steps.append(step)
        if trace.steps:
            trace.total_path_integral = sum(s.path_integral for s in trace.steps)
            trace.mean_viscosity = sum(s.holonomic_viscosity for s in trace.steps) / len(trace.steps)
            trace.mean_affordance = sum(s.phasenav_affordance for s in trace.steps) / len(trace.steps)
        return trace

    def _step_between(self, src_card_id: str, tgt_card_id: str) -> PhaseNavStep | None:
        src_phase = self.get_phase(src_card_id)
        tgt_phase = self.get_phase(tgt_card_id)
        if src_phase is None or tgt_phase is None:
            return None
        edge = self.best_edge_from(src_card_id)
        if edge is None:
            return None
        op_card_id = edge.get("operator_card_id", "")
        op_hook = edge.get("operator_hook", "")
        if edge.get("holonomic_viscosity") is None or edge.get("phasenav_affordance") is None:
            return None
        lane = edge.get("transition_lane")
        if lane is None:
            return None
        visc = float(edge["holonomic_viscosity"])
        afford = float(edge["phasenav_affordance"])
        phase_delta = tgt_phase - src_phase
        path_contrib = visc * abs(phase_delta)
        return PhaseNavStep(
            source_card_id=src_card_id,
            target_card_id=tgt_card_id,
            operator_hook=op_hook,
            operator_card_id=op_card_id,
            phase_start=src_phase,
            phase_end=tgt_phase,
            phase_delta=phase_delta,
            holonomic_viscosity=visc,
            phasenav_affordance=afford,
            transition_lane=lane,
            path_integral=path_contrib,
        )
