from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import math
from typing import Any, Mapping, Sequence


SCHEMA = "CIEL_INTEROCEPTIVE_READOUT_V1"
VECTOR_ORDER = (
    "mood",
    "soul_invariant",
    "ethical_score",
    "htri_coherence",
    "mnemonic_pressure",
    "symbolic_pull",
    "recurrence_pressure",
    "identity_phase",
    "phi_berry_mean",
    "bridge_target_phase",
    "memory_projection_confidence",
    "lingo_noema_confidence",
    "gate_confidence",
)


def _get(src: Mapping[str, Any] | None, key: str, default: Any = None) -> Any:
    if not isinstance(src, Mapping):
        return default
    return src.get(key, default)


def _float(src: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    try:
        value = float(_get(src, key, default) or 0.0)
    except (TypeError, ValueError):
        return float(default)
    return value if math.isfinite(value) else float(default)


def _unit(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _wrapped_delta(a: float, b: float) -> float:
    """Shortest signed angular delta a-b in [-pi, pi)."""
    return (float(a) - float(b) + math.pi) % (2.0 * math.pi) - math.pi


def _phase_resultant(phases: Sequence[float]) -> tuple[float, float]:
    if not phases:
        return 0.0, 0.0
    z = sum(complex(math.cos(p), math.sin(p)) for p in phases) / len(phases)
    return abs(z), math.atan2(z.imag, z.real)


def _canonical_digest(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


@dataclass(frozen=True)
class InteroceptiveReadout:
    """Read-only projection of already-existing CIEL state.

    The readout does not invent a new memory lane or phenomenology claim. It
    exposes four existing functional sectors as stable AUX-ready triads:

    M5  affective     -> mood, soul_invariant, ethical_score
    M6  relational    -> mnemonic_pressure, symbolic_pull, recurrence_pressure
    M9  holonomic     -> identity_phase, phi_berry_mean, bridge_target_phase
    M11 metacognitive -> memory_projection_confidence, lingo_noema_confidence,
                         gate_confidence

    The holonomic triad is phase-native. ``phase_R`` and ``phase_psi`` are the
    circular resultant of those three existing phase channels.
    """

    schema: str
    interoceptive_id: str
    cycle_index: int
    dominant_emotion: str
    affective_triad: tuple[float, float, float]
    relational_triad: tuple[float, float, float]
    holonomic_triad: tuple[float, float, float]
    metacognitive_triad: tuple[float, float, float]
    phase_R: float
    phase_psi: float
    berry_identity_offset: float
    closure_penalty: float
    coherence_index: float
    factual_validation_required: bool
    vector_order: tuple[str, ...]
    state_vector: tuple[float, ...]
    source_layers: tuple[str, str, str, str]
    source_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_interoceptive_readout(state: Mapping[str, Any]) -> InteroceptiveReadout:
    """Build the CIEL interoceptive layer from existing runtime channels only."""
    mood = _float(state, "mood")
    soul = _float(state, "soul_invariant")
    ethical = _float(state, "ethical_score")
    htri = _float(state, "htri_coherence")

    mnemonic = _float(state, "jokeheal_mnemonic_pressure", _float(state, "mnemonic_pressure"))
    symbolic = _float(state, "jokeheal_symbolic_pull", _float(state, "symbolic_pull"))
    recurrence = _float(state, "jokeheal_recurrence_pressure", _float(state, "recurrence_pressure"))

    identity_phase = _float(state, "identity_phase")
    berry = _float(state, "phi_berry_mean")
    bridge_target = _float(state, "bridge_target_phase")

    memory_conf = _unit(_float(state, "memory_projection_confidence"))
    noema_conf = _unit(_float(state, "lingo_noema_confidence"))
    gate_conf = _unit(_float(state, "gate_confidence", 1.0))

    affective = (mood, soul, ethical)
    relational = (mnemonic, symbolic, recurrence)
    holonomic = (identity_phase, berry, bridge_target)
    metacognitive = (memory_conf, noema_conf, gate_conf)
    phase_R, phase_psi = _phase_resultant(holonomic)

    state_vector = (
        mood,
        soul,
        ethical,
        htri,
        mnemonic,
        symbolic,
        recurrence,
        identity_phase,
        berry,
        bridge_target,
        memory_conf,
        noema_conf,
        gate_conf,
    )

    source_payload = {
        "schema": SCHEMA,
        "cycle_index": int(_get(state, "cycle_index", 0) or 0),
        "dominant_emotion": str(_get(state, "dominant_emotion", "") or ""),
        "vector_order": VECTOR_ORDER,
        "state_vector": state_vector,
        "closure_penalty": _float(state, "closure_penalty"),
        "coherence_index": _float(state, "coherence_index"),
        "factual_validation_required": bool(_get(state, "lingo_factual_validation_required", False)),
    }
    digest = _canonical_digest(source_payload)
    cycle_index = int(source_payload["cycle_index"])

    return InteroceptiveReadout(
        schema=SCHEMA,
        interoceptive_id=f"intero:{cycle_index}:{digest[:16]}",
        cycle_index=cycle_index,
        dominant_emotion=str(source_payload["dominant_emotion"]),
        affective_triad=affective,
        relational_triad=relational,
        holonomic_triad=holonomic,
        metacognitive_triad=metacognitive,
        phase_R=float(phase_R),
        phase_psi=float(phase_psi),
        berry_identity_offset=float(_wrapped_delta(identity_phase, berry)),
        closure_penalty=float(source_payload["closure_penalty"]),
        coherence_index=float(source_payload["coherence_index"]),
        factual_validation_required=bool(source_payload["factual_validation_required"]),
        vector_order=VECTOR_ORDER,
        state_vector=state_vector,
        source_layers=("M5_affective", "M6_relational", "M9_holonomic", "M11_metacognitive"),
        source_digest=digest,
    )


def interoceptive_delta(
    current: InteroceptiveReadout,
    previous: InteroceptiveReadout,
) -> dict[str, Any]:
    """Deterministic delta without interpreting it as emotion or phenomenology."""
    if current.vector_order != previous.vector_order:
        raise ValueError("interoceptive vector orders are incompatible")
    delta = tuple(c - p for c, p in zip(current.state_vector, previous.state_vector, strict=True))
    return {
        "schema": "CIEL_INTEROCEPTIVE_DELTA_V1",
        "from": previous.interoceptive_id,
        "to": current.interoceptive_id,
        "vector_order": current.vector_order,
        "delta": delta,
        "l2": math.sqrt(sum(value * value for value in delta)),
        "phase_delta": _wrapped_delta(current.phase_psi, previous.phase_psi),
        "R_delta": current.phase_R - previous.phase_R,
    }
