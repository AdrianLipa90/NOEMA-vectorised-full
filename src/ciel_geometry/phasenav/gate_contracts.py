"""Substrate-neutral contracts for the NOEMA PhaseNav Gate Fabric.

These types intentionally contain no actuator logic. They define the common
language shared by Oracle observations, MegaSorter proposals, the PhaseNav gate
fabric, Doctor verdicts, Return receipts and unresolved relational debt.

A critical invariant is that equal dimensionality does not imply equal
coordinates. Raw 36-oscillator phase angles, canonical precise PNV36 phases,
36D operator signatures and other 36D vectors are explicitly tagged with a
PhaseSpace and may not be compared without a declared projection.

M2 invariant: contracts are read-only data boundaries; no mutation authority is
introduced by this module.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Sequence

PHASENAV_DIM = 36


class EpistemicState(str, Enum):
    OBSERVATION = "observation"
    HYPOTHESIS = "hypothesis"
    CANDIDATE = "candidate"
    IMPLEMENTED = "implemented"
    TESTED = "tested"
    VALIDATED = "validated"
    PROMOTED_SOT = "promoted_sot"


class ObservationClass(str, Enum):
    MEASURED = "measured"
    PARSED = "parsed"
    RETRIEVED = "retrieved"
    SIMULATED = "simulated"


class PhaseSpace(str, Enum):
    """Named 36D coordinate spaces used by PhaseNav.

    A projection between different spaces must be explicit. In particular,
    OSCILLATOR_PHASE_36 contains the live mmap oscillator state,
    PNV_PRECISE_PHASE_36 contains M_sentence_phase_precise coordinates, while
    OPERATOR_SIGNATURE_36 contains semantic/operator feature coordinates.
    """

    UNKNOWN = "unknown"
    OSCILLATOR_PHASE_36 = "oscillator_phase_36"
    PNV_PRECISE_PHASE_36 = "pnv_precise_phase_36"
    OPERATOR_SIGNATURE_36 = "operator_signature_36"
    CARD_VECTOR_36 = "card_vector_36"
    RELATIONAL_VECTOR_36 = "relational_vector_36"


class GateDecision(str, Enum):
    OPEN = "OPEN"
    HOLD = "HOLD"
    REJECT = "REJECT"


class DoctorDecision(str, Enum):
    PASS = "PASS"
    HOLD = "HOLD"
    REJECT = "REJECT"
    DEBT = "DEBT"
    UNKNOWN = "UNKNOWN"


def _phase36(values: Sequence[float] | None, *, field_name: str) -> tuple[float, ...] | None:
    if values is None:
        return None
    result = tuple(float(v) for v in values)
    if len(result) != PHASENAV_DIM:
        raise ValueError(f"{field_name} must contain exactly {PHASENAV_DIM} components; got {len(result)}")
    return result


def _tuple_str(values: Sequence[str] | None) -> tuple[str, ...]:
    return tuple(str(v) for v in (values or ()))


def _validate_phase_space(vector: tuple[float, ...] | None, space: PhaseSpace, *, field_name: str) -> None:
    if vector is not None and space is PhaseSpace.UNKNOWN:
        raise ValueError(f"{field_name} requires an explicit PhaseSpace")


@dataclass(frozen=True)
class RelationalObservation:
    observation_id: str
    source: str
    observation_class: ObservationClass
    payload: Mapping[str, Any]
    provenance: tuple[str, ...] = ()
    confidence: float | None = None
    phase36: tuple[float, ...] | None = None
    phase_space: PhaseSpace = PhaseSpace.UNKNOWN
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "provenance", _tuple_str(self.provenance))
        phase = _phase36(self.phase36, field_name="phase36")
        object.__setattr__(self, "phase36", phase)
        _validate_phase_space(phase, self.phase_space, field_name="phase36")
        if self.confidence is not None and not 0.0 <= float(self.confidence) <= 1.0:
            raise ValueError("confidence must be in [0, 1]")

    @property
    def canonical_evidence_eligible(self) -> bool:
        """Simulation is never canonical evidence without a separate validated promotion."""
        return self.observation_class is not ObservationClass.SIMULATED and bool(self.provenance)


@dataclass(frozen=True)
class RelationalState:
    identity: str
    kind: str
    phase36: tuple[float, ...] | None = None
    phase_space: PhaseSpace = PhaseSpace.UNKNOWN
    order_parameter: float | None = None
    mass: float | None = None
    attractor_id: str | None = None
    sector_id: str | None = None
    lineage: tuple[str, ...] = ()
    relations: tuple[str, ...] = ()
    holonomy_defect: float | None = None
    associator_defect: float | None = None
    conflict: float | None = None
    provenance: tuple[str, ...] = ()
    epistemic_state: EpistemicState = EpistemicState.OBSERVATION
    authority_state: str = "NONE"
    lifecycle: str = "OBSERVED"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        phase = _phase36(self.phase36, field_name="phase36")
        object.__setattr__(self, "phase36", phase)
        _validate_phase_space(phase, self.phase_space, field_name="phase36")
        object.__setattr__(self, "lineage", _tuple_str(self.lineage))
        object.__setattr__(self, "relations", _tuple_str(self.relations))
        object.__setattr__(self, "provenance", _tuple_str(self.provenance))

    @property
    def has_provenance(self) -> bool:
        return bool(self.provenance)


@dataclass(frozen=True)
class PhaseOperation:
    operation_id: str
    relation_type: str
    source_id: str
    target_id: str | None = None
    phase_signature36: tuple[float, ...] | None = None
    phase_signature_space: PhaseSpace = PhaseSpace.UNKNOWN
    mutation_class: str = "READ_ONLY"
    evidence: tuple[str, ...] = ()
    provenance_requirements: tuple[str, ...] = ()
    authority_requirements: tuple[str, ...] = ()
    reversible: bool = True
    return_required: bool = True
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        phase = _phase36(self.phase_signature36, field_name="phase_signature36")
        object.__setattr__(self, "phase_signature36", phase)
        _validate_phase_space(phase, self.phase_signature_space, field_name="phase_signature36")
        object.__setattr__(self, "evidence", _tuple_str(self.evidence))
        object.__setattr__(self, "provenance_requirements", _tuple_str(self.provenance_requirements))
        object.__setattr__(self, "authority_requirements", _tuple_str(self.authority_requirements))

    @property
    def mutates(self) -> bool:
        return self.mutation_class.upper() != "READ_ONLY"


@dataclass(frozen=True)
class GateResult:
    operation_id: str
    decision: GateDecision
    score: float | None = None
    reasons: tuple[str, ...] = ()
    hard_failures: tuple[str, ...] = ()
    metrics: Mapping[str, float] = field(default_factory=dict)
    evidence: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "reasons", _tuple_str(self.reasons))
        object.__setattr__(self, "hard_failures", _tuple_str(self.hard_failures))
        object.__setattr__(self, "evidence", _tuple_str(self.evidence))
        if self.score is not None and not 0.0 <= float(self.score) <= 1.0:
            raise ValueError("gate score must be in [0, 1]")
        if self.hard_failures and self.decision is GateDecision.OPEN:
            raise ValueError("a gate with hard failures cannot be OPEN")


@dataclass(frozen=True)
class DoctorVerdict:
    operation_id: str
    decision: DoctorDecision
    reasons: tuple[str, ...] = ()
    checks: Mapping[str, str] = field(default_factory=dict)
    evidence: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "reasons", _tuple_str(self.reasons))
        object.__setattr__(self, "evidence", _tuple_str(self.evidence))


@dataclass(frozen=True)
class ReturnReceipt:
    receipt_id: str
    operation_id: str
    before_hash: str
    after_hash: str | None
    gate_decision: GateDecision
    doctor_decision: DoctorDecision
    actuator_status: str = "NOT_RUN"
    promoted: bool = False
    debt_id: str | None = None
    evidence: tuple[str, ...] = ()
    provenance: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "evidence", _tuple_str(self.evidence))
        object.__setattr__(self, "provenance", _tuple_str(self.provenance))
        if self.promoted and self.actuator_status != "APPLIED":
            raise ValueError("promotion requires actuator_status='APPLIED'")
        if self.promoted and self.doctor_decision is not DoctorDecision.PASS:
            raise ValueError("promotion requires Doctor PASS")
        if self.promoted and self.gate_decision is not GateDecision.OPEN:
            raise ValueError("promotion requires Gate OPEN")


@dataclass(frozen=True)
class UnresolvedRelationalDebt:
    debt_id: str
    origin: str
    operation_id: str | None = None
    failed_gate: str | None = None
    phase36: tuple[float, ...] | None = None
    phase_space: PhaseSpace = PhaseSpace.UNKNOWN
    associator_defect: float | None = None
    closure_defect: float | None = None
    missing_provenance: tuple[str, ...] = ()
    failed_validation: tuple[str, ...] = ()
    candidate_returns: tuple[str, ...] = ()
    reasons: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        phase = _phase36(self.phase36, field_name="phase36")
        object.__setattr__(self, "phase36", phase)
        _validate_phase_space(phase, self.phase_space, field_name="phase36")
        object.__setattr__(self, "missing_provenance", _tuple_str(self.missing_provenance))
        object.__setattr__(self, "failed_validation", _tuple_str(self.failed_validation))
        object.__setattr__(self, "candidate_returns", _tuple_str(self.candidate_returns))
        object.__setattr__(self, "reasons", _tuple_str(self.reasons))


__all__ = [
    "PHASENAV_DIM",
    "EpistemicState",
    "ObservationClass",
    "PhaseSpace",
    "GateDecision",
    "DoctorDecision",
    "RelationalObservation",
    "RelationalState",
    "PhaseOperation",
    "GateResult",
    "DoctorVerdict",
    "ReturnReceipt",
    "UnresolvedRelationalDebt",
]
