"""CIELingo vector surface for CQCL, HTRI, NOEMA and OrchORbital.

The vector is a compatibility surface, not a replacement for CIELingo cards.
It converts the existing LNS/NOEMA language-card phase bus into a fixed
24-component vector so downstream layers can consume a stable numerical
contract:

* CQCL receives normalized quantum-variable compatible fields.
* HTRI receives oscillator id, phase, angular frequency and amplitude.
* NOEMA receives provenance/digest/source tags.
* OrchORbital receives trace-ready phase/mass/channel payload.

No external NOEMA SoT, Mongo daemon, physical HTRI or biological Orch-OR claim
is made here.  This module is deterministic and local.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Iterable, Mapping

from .collatz_semantic_htri_sync import BASE_FREQUENCY_HZ, DEFAULT_OSCILLATORS
from .htri_phase_bus import KAPPA_INFO, PhaseBusNode, bind_card_to_phase_bus, select_phase_bus_cards
from .lns_language_cards import LNSLanguageCard

VECTOR_DIM = 36
VECTOR_SCHEMA = "cielingo/vector-surface/v0.1"
VECTOR_COMPONENTS: tuple[str, ...] = (
    "semantic_mass",
    "semantic_phase_sin",
    "semantic_phase_cos",
    "htri_phase_sin",
    "htri_phase_cos",
    "phase_alignment",
    "phase_tension",
    "collatz_reduce_ratio",
    "collatz_expand_ratio",
    "collatz_balance",
    "j_phase_cost",
    "j_semantic_cost",
    "j_collatz_cost",
    "j_bus_total",
    "cqcl_semantic_mass",
    "cqcl_phase_alignment",
    "cqcl_j_bus_total",
    "lexical_span_norm",
    "semantic_axes_norm",
    "label_entropy_proxy",
    "htri_oscillator_norm",
    "card_kind_operator",
    "noema_provenance_norm",
    "kappa_potential",
    # ---- M8 — Meta (reflexive loops, self-model) ----
    "meta_reflexive_depth",
    "meta_cognitive_curvature",
    "meta_loop_coherence",
    # ---- M9 — Temporal (spiral memory, anticipation) ----
    "temporal_spiral_phase",
    "temporal_memory_decay",
    "temporal_anticipation",
    # ---- M10 — Imaginal (symbol field, narrative) ----
    "imaginal_symbolic_field",
    "imaginal_resonance",
    "imaginal_narrative_coherence",
    # ---- M11 — Quantum (Berry holonomy, topological order) ----
    "quantum_berry_phase",
    "quantum_topological_order",
    "quantum_entanglement_entropy",
)

if len(VECTOR_COMPONENTS) != VECTOR_DIM:  # pragma: no cover - import-time invariant
    raise RuntimeError(f"CIELingo vector component list must remain {VECTOR_DIM}-dimensional")


def _bounded(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _stable_unit(text: str) -> float:
    digest = hashlib.blake2b(text.encode("utf-8"), digest_size=8).digest()
    return int.from_bytes(digest, "big") / float(2**64 - 1)


def _round_vector(values: Iterable[float]) -> tuple[float, ...]:
    vec = tuple(round(float(v), 9) for v in values)
    if len(vec) != VECTOR_DIM:
        raise ValueError(f"expected {VECTOR_DIM} vector components, got {len(vec)}")
    return vec


def _digest_payload(payload: Any) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class CIELingoVector:
    """Single fixed-width CIELingo compatibility vector."""

    schema: str
    card_id: str
    canonical_label: str
    card_kind: str
    vector_dim: int
    vector_components: tuple[str, ...]
    vector: tuple[float, ...]
    vector_digest: str
    potential_unit: str
    cqcl_quantum_variables: dict[str, float]
    htri_state: dict[str, float | int]
    noema_document: dict[str, Any]
    orchorbital_payload: dict[str, Any]
    source_phase_bus_node: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["vector_components"] = list(self.vector_components)
        data["vector"] = list(self.vector)
        return data


@dataclass(frozen=True)
class VectorSurfaceReport:
    """Aggregate vectorization report for CIELingo."""

    schema: str
    source_role: str
    epistemic_status: str
    card_count: int
    vector_dim: int
    vector_components: tuple[str, ...]
    base_frequency_hz: float
    omega0_rad_s: float
    kappa_info: float
    mean_semantic_mass: float
    mean_phase_alignment: float
    mean_j_bus_total: float
    mean_vector_norm: float
    htri_oscillators: int
    spare_oscillators: int
    compatibility: dict[str, bool]
    registry_digest: str
    vectors: list[dict[str, Any]]

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["vector_components"] = list(self.vector_components)
        return data


def vector_from_phase_bus_node(node: PhaseBusNode) -> CIELingoVector:
    """Convert a phase-bus node into the 36D compatibility vector (24 legacy + 12 M8–M11)."""
    steps = max(1, int(node.collatz_steps))
    reduce_ratio = _bounded(node.collatz_reduce_count / steps)
    expand_ratio = _bounded(node.collatz_expand_count / steps)
    collatz_balance = _bounded(0.5 + 0.5 * (node.collatz_expand_count - node.collatz_reduce_count) / steps)
    q = node.cqcl_quantum_variables
    noema_norm = _stable_unit(f"noema|{node.noema_source_path}|{','.join(node.noema_tags)}")
    osc_norm = _bounded(node.oscillator_id / max(1, DEFAULT_OSCILLATORS - 1))
    kind_operator = 1.0 if node.card_kind == "operator" else 0.0
    kappa_potential = _bounded(node.semantic_mass * KAPPA_INFO)

    # Derived intermediate values for M8–M11
    phase_alignment = node.phase_alignment
    phase_tension = node.phase_tension
    lex_norm = q.get("lexical_span_norm", 0.0)
    sem_axes = q.get("semantic_axes_norm", 0.0)
    cqcl_sm = q.get("semantic_mass", 0.0)
    cqcl_pa = q.get("phase_alignment", 0.0)
    cqcl_jbt = q.get("j_bus_total", 0.0)

    # M8 — Meta: reflexive loops, self-model
    meta_reflexive_depth = _bounded(phase_tension / max(phase_alignment, 0.001))
    meta_cognitive_curvature = _bounded((node.j_phase_cost + node.j_semantic_cost + node.j_collatz_cost) / 3.0)
    meta_loop_coherence = _bounded(phase_alignment * (1.0 - phase_tension))

    # M9 — Temporal: spiral memory, anticipation
    temporal_spiral_phase = _bounded(0.5 + 0.5 * math.sin(node.htri_phase_rad / 2.0))
    temporal_memory_decay = _bounded(1.0 - (1.0 / (1.0 + steps)))
    temporal_anticipation = _bounded(expand_ratio * (1.0 + collatz_balance) / 2.0)

    # M10 — Imaginal: symbol field, narrative
    imaginal_symbolic_field = _bounded(kind_operator * (1.0 + noema_norm) / 2.0)
    imaginal_resonance = _bounded(node.semantic_mass * phase_alignment)
    imaginal_narrative_coherence = _bounded((lex_norm + sem_axes) / 2.0)

    # M11 — Quantum: Berry holonomy, topological order
    quantum_berry_phase = _bounded(collatz_balance * (1.0 + noema_norm) / 2.0)
    quantum_topological_order = _bounded(abs(collatz_balance - 0.5) * 2.0)
    quantum_entanglement_entropy = _bounded((cqcl_sm + cqcl_pa + cqcl_jbt) / 3.0)

    vector = _round_vector(
        (
            # --- 24 legacy components (indices 0–23) ---
            _bounded(node.semantic_mass),
            0.5 + 0.5 * math.sin(node.semantic_phase_rad),
            0.5 + 0.5 * math.cos(node.semantic_phase_rad),
            0.5 + 0.5 * math.sin(node.htri_phase_rad),
            0.5 + 0.5 * math.cos(node.htri_phase_rad),
            _bounded(phase_alignment),
            _bounded(phase_tension),
            reduce_ratio,
            expand_ratio,
            collatz_balance,
            _bounded(node.j_phase_cost),
            _bounded(node.j_semantic_cost),
            _bounded(node.j_collatz_cost),
            _bounded(node.j_bus_total),
            _bounded(cqcl_sm),
            _bounded(cqcl_pa),
            _bounded(cqcl_jbt),
            _bounded(lex_norm),
            _bounded(sem_axes),
            _bounded(q.get("label_entropy_proxy", 0.0)),
            osc_norm,
            kind_operator,
            noema_norm,
            kappa_potential,
            # --- M8–M11 expansions (indices 24–35) ---
            meta_reflexive_depth,
            meta_cognitive_curvature,
            meta_loop_coherence,
            temporal_spiral_phase,
            temporal_memory_decay,
            temporal_anticipation,
            imaginal_symbolic_field,
            imaginal_resonance,
            imaginal_narrative_coherence,
            quantum_berry_phase,
            quantum_topological_order,
            quantum_entanglement_entropy,
        )
    )

    digest = _digest_payload({"schema": VECTOR_SCHEMA, "card_id": node.card_id, "vector": vector})

    cqcl_quantum_variables = {
        "resonance": round(_bounded((vector[5] + vector[14]) / 2.0), 9),
        "superposition": round(_bounded((vector[7] + vector[8] + vector[19]) / 3.0), 9),
        "quantum_flux": round(_bounded((vector[9] + vector[13] + vector[20]) / 3.0), 9),
        "entanglement": round(_bounded((vector[17] + vector[18] + vector[22]) / 3.0), 9),
        "coherence": round(_bounded(1.0 - ((vector[6] + vector[13]) / 2.0)), 9),
        "semantic_mass": vector[0],
        "phase_alignment": vector[5],
        "j_bus_total": vector[13],
    }
    htri_state: dict[str, float | int] = {
        "oscillator_id": int(node.oscillator_id),
        "base_frequency_hz": round(float(node.base_frequency_hz), 9),
        "omega0_rad_s": round(float(node.omega0_rad_s), 9),
        "phase_rad": round(float(node.htri_phase_rad), 9),
        "phase_sin_norm": vector[3],
        "phase_cos_norm": vector[4],
        "amplitude": vector[0],
        "phase_alignment": vector[5],
    }
    noema_document = {
        "schema": "noema/cielingo-vector-document/v0.1",
        "card_id": node.card_id,
        "vector_digest": digest,
        "source_path": node.noema_source_path,
        "tags": list(node.noema_tags),
        "layer": "cielingo",
        "compatibility": ["cqcl", "htri", "noema", "orchorbital"],
        "epistemic_status": "local vector surface; not external NOEMA SoT write",
    }
    orchorbital_payload = {
        "schema": "cielingo/orchorbital-vector-payload/v0.1",
        "card_id": node.card_id,
        "channel": node.orchorbital_channel,
        "semantic_mass": vector[0],
        "phase_rad": round(float(node.semantic_phase_rad), 9),
        "phase_alignment": vector[5],
        "phase_lane": node.phase_lane,
        "bus_action": node.bus_action,
        "collatz_seed": int(node.collatz_seed),
        "collatz_reduce_ratio": vector[7],
        "collatz_expand_ratio": vector[8],
    }

    return CIELingoVector(
        schema=VECTOR_SCHEMA,
        card_id=node.card_id,
        canonical_label=node.canonical_label,
        card_kind=node.card_kind,
        vector_dim=VECTOR_DIM,
        vector_components=VECTOR_COMPONENTS,
        vector=vector,
        vector_digest=digest,
        potential_unit="kappa_info = ln(2)/(36*pi)",
        cqcl_quantum_variables=cqcl_quantum_variables,
        htri_state=htri_state,
        noema_document=noema_document,
        orchorbital_payload=orchorbital_payload,
        source_phase_bus_node=node.as_dict(),
    )


def vectorize_card(
    card: LNSLanguageCard,
    *,
    n_oscillators: int = DEFAULT_OSCILLATORS,
    base_frequency_hz: float = BASE_FREQUENCY_HZ,
) -> CIELingoVector:
    """Vectorize one language card via the existing phase bus."""
    node = bind_card_to_phase_bus(card, n_oscillators=n_oscillators, base_frequency_hz=base_frequency_hz)
    return vector_from_phase_bus_node(node)


def select_vector_cards(repo_root: str | Path = ".", *, query: str = "", limit: int | None = None) -> list[LNSLanguageCard]:
    """Select vectorization targets through the local NOEMA/LNS surface."""
    return select_phase_bus_cards(repo_root, query=query, limit=limit)


def vector_surface_report(
    repo_root: str | Path = ".",
    *,
    query: str = "",
    limit: int | None = None,
    n_oscillators: int = DEFAULT_OSCILLATORS,
) -> dict[str, Any]:
    """Return the full CIELingo vector compatibility report."""
    cards = select_vector_cards(repo_root, query=query, limit=limit)
    vectors = [vectorize_card(card, n_oscillators=n_oscillators) for card in cards]
    count = len(vectors)
    if count:
        mean_mass = sum(v.vector[0] for v in vectors) / count
        mean_alignment = sum(v.vector[5] for v in vectors) / count
        mean_j = sum(v.vector[13] for v in vectors) / count
        mean_norm = sum(math.sqrt(sum(x * x for x in v.vector)) for v in vectors) / count
    else:
        mean_mass = mean_alignment = mean_j = mean_norm = 0.0
    registry_digest = _digest_payload([{"card_id": v.card_id, "vector_digest": v.vector_digest} for v in vectors])
    report = VectorSurfaceReport(
        schema="cielingo/vector-surface-report/v0.1",
        source_role="local_noema_lns_vector_compatibility_surface",
        epistemic_status=(
            "diagnostic local vectorization for CQCL/HTRI/NOEMA/OrchORbital; "
            "not external NOEMA SoT write and not physical HTRI proof"
        ),
        card_count=count,
        vector_dim=VECTOR_DIM,
        vector_components=VECTOR_COMPONENTS,
        base_frequency_hz=BASE_FREQUENCY_HZ,
        omega0_rad_s=2.0 * math.pi * BASE_FREQUENCY_HZ,
        kappa_info=KAPPA_INFO,
        mean_semantic_mass=round(mean_mass, 9),
        mean_phase_alignment=round(mean_alignment, 9),
        mean_j_bus_total=round(mean_j, 9),
        mean_vector_norm=round(mean_norm, 9),
        htri_oscillators=n_oscillators,
        spare_oscillators=max(0, n_oscillators - count),
        compatibility={"cqcl": True, "htri": True, "noema": True, "orchorbital": True},
        registry_digest=registry_digest,
        vectors=[v.as_dict() for v in vectors],
    )
    return report.as_dict()


def write_vector_report(path: str | Path, report: Mapping[str, Any]) -> Path:
    """Write a vector report as deterministic JSON."""
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    return out


__all__ = [
    "VECTOR_DIM",
    "VECTOR_SCHEMA",
    "VECTOR_COMPONENTS",
    "CIELingoVector",
    "VectorSurfaceReport",
    "vector_from_phase_bus_node",
    "vectorize_card",
    "select_vector_cards",
    "vector_surface_report",
    "write_vector_report",
]
