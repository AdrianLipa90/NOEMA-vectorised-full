"""Shared phase gate for reviewed ingestion and bounded semantic context.

The gate wraps the diagnostic PhaseLogicEngine in an explicit admission
contract.  It has no persistence or execution capability; callers must inspect
the returned disposition before creating context or semantic records.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Iterable

from ciel_geometry.phasenav.formalism_logic import PhaseLogicEngine, PhaseLogicState


class GateDisposition(StrEnum):
    ACCEPT = "accept"
    QUARANTINE = "quarantine"
    HOLD = "hold"


@dataclass(frozen=True)
class PhaseGateDecision:
    disposition: GateDisposition
    score: float
    tension: float
    phase_coherence: float
    recommendation: str
    graph_digest: str
    evidence_source: str
    admitted: bool
    hypothesis_only: bool = True

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["disposition"] = self.disposition.value
        return payload


class ContextSemanticPhaseGate:
    """Map bounded cross-formalism diagnostics to a fail-closed disposition."""

    def __init__(self, *, minimum_score: float = 0.45, maximum_tension: float = 0.65) -> None:
        if not 0.0 <= minimum_score <= 1.0:
            raise ValueError("minimum_score must be within [0, 1]")
        if not 0.0 <= maximum_tension <= 1.0:
            raise ValueError("maximum_tension must be within [0, 1]")
        self.minimum_score = float(minimum_score)
        self.maximum_tension = float(maximum_tension)
        self.engine = PhaseLogicEngine()

    def evaluate(
        self,
        phase_vector: Iterable[float],
        *,
        htri_coherence: float,
        cqcl_coherence: float,
        semantic_mass: float,
        tau: float,
        evidence_source: str,
    ) -> PhaseGateDecision:
        if not evidence_source.strip():
            raise ValueError("phase gate evidence_source is required")
        report = self.engine.observe(
            PhaseLogicState.from_iterable(
                phase_vector,
                htri_coherence=htri_coherence,
                cqcl_coherence=cqcl_coherence,
                semantic_mass=semantic_mass,
                tau=tau,
            )
        )
        if report.recommendation == "hold" or report.tension > self.maximum_tension:
            disposition = GateDisposition.HOLD
        elif report.recommendation == "reduce" or report.score < self.minimum_score:
            disposition = GateDisposition.QUARANTINE
        else:
            disposition = GateDisposition.ACCEPT
        return PhaseGateDecision(
            disposition=disposition,
            score=report.score,
            tension=report.tension,
            phase_coherence=report.phase_coherence,
            recommendation=report.recommendation,
            graph_digest=report.graph_digest,
            evidence_source=evidence_source,
            admitted=disposition is GateDisposition.ACCEPT,
        )


__all__ = ["ContextSemanticPhaseGate", "GateDisposition", "PhaseGateDecision"]
