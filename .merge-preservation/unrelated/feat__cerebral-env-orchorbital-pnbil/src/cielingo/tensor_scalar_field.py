"""CIELingo tensor-scalar field for real exchange and imaginary context.

CIELingo already has a stable 24D vector compatibility surface.  This module
adds the missing field interpretation without changing that vector contract:

* real information exchange is represented as a rank-2 tensor-like 3x3 matrix;
* contextual/affective load is represented as a scalar medium;
* sarcasm, excitement, tension, relief and fear are treated as dense/viscous
  scalar-context proxies, not as token labels;
* density, viscosity, colour and saturation determine semantic time resistance.

The layer is deterministic and local.  It does not claim external NOEMA SoT
writeback, live Mongo, physical HTRI, or psychological affect measurement.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Iterable, Mapping

from .htri_phase_bus import KAPPA_INFO
from .lexical_holonomy import (
    LexicalHolonomyEdge,
    WordKnowledgeNote,
    build_lexical_holonomy_edges,
    build_word_knowledge_notes,
    extract_lexical_units,
)
from .lns_language_cards import LNSLanguageCard
from .vector_surface import CIELingoVector, select_vector_cards, vectorize_card

TENSOR_SCALAR_SCHEMA = "cielingo/tensor-scalar-field/v0.1"
TENSOR_SHAPE: tuple[int, int] = (3, 3)
TENSOR_AXES: tuple[str, ...] = (
    "semantic_mass_phase",
    "collatz_jfunctional_transport",
    "lexical_holonomy_exchange",
)
SCALAR_CHANNELS: tuple[str, ...] = ("density", "viscosity", "colour", "saturation")
AFFECT_CHANNELS: tuple[str, ...] = ("sarcasm", "excitement", "tension", "relief", "fear")

# Multilingual local keywords.  These are seed priors only; external lexical
# evidence must be attached before treating them as verified affect labels.
AFFECT_KEYWORDS: Mapping[str, tuple[str, ...]] = {
    "sarcasm": ("sarcasm", "sarkazm", "irony", "ironia", "żart", "joke", "mask", "hidden"),
    "excitement": ("excitement", "ekscyt", "joy", "rado", "light", "światło", "energy", "energia", "dance"),
    "tension": ("tension", "napię", "pressure", "presja", "pain", "ból", "conflict", "konflikt"),
    "relief": ("relief", "ulga", "release", "uwol", "rest", "spoczy", "home", "dom"),
    "fear": ("fear", "strach", "ciem", "dark", "threat", "zagro", "loss", "utrata"),
}


@dataclass(frozen=True)
class ContextScalarField:
    """Imaginary/contextual scalar medium attached to one CIELingo vector."""

    schema: str
    field_kind: str
    channels: tuple[str, ...]
    density: float
    viscosity: float
    colour_hue_deg: float
    colour_name: str
    saturation: float
    affect_scalars: dict[str, float]
    semantic_time_resistance: float
    semantic_time_thinning: float
    scalar_context_potential: float
    epistemic_note: str

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["channels"] = list(self.channels)
        return data


@dataclass(frozen=True)
class TensorScalarWordState:
    """One mixed tensor-scalar state for a card/word cluster."""

    schema: str
    card_id: str
    canonical_label: str
    source_path: str
    tensor_role: str
    scalar_role: str
    tensor_shape: tuple[int, int]
    tensor_axes: tuple[str, ...]
    real_exchange_tensor: tuple[tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]]
    tensor_trace: float
    tensor_determinant_proxy: float
    scalar_context: ContextScalarField
    lexical_relation_count: int
    lexical_similarity_flux: float
    lexical_opposition_flux: float
    knowledge_confidence: float
    vector_digest: str
    noema_document: dict[str, Any]
    cqcl_payload: dict[str, float]
    htri_payload: dict[str, float | int | str]
    orchorbital_payload: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["tensor_shape"] = list(self.tensor_shape)
        data["tensor_axes"] = list(self.tensor_axes)
        data["real_exchange_tensor"] = [list(row) for row in self.real_exchange_tensor]
        data["scalar_context"] = self.scalar_context.as_dict()
        return data


@dataclass(frozen=True)
class TensorScalarReport:
    """Aggregate CIELingo tensor-scalar field report."""

    schema: str
    source_role: str
    epistemic_status: str
    card_count: int
    tensor_shape: tuple[int, int]
    scalar_channels: tuple[str, ...]
    affect_channels: tuple[str, ...]
    mean_density: float
    mean_viscosity: float
    mean_saturation: float
    mean_semantic_time_resistance: float
    mean_semantic_time_thinning: float
    mean_knowledge_confidence: float
    high_resistance_count: int
    high_viscosity_count: int
    registry_digest: str
    states: list[dict[str, Any]]

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["tensor_shape"] = list(self.tensor_shape)
        data["scalar_channels"] = list(self.scalar_channels)
        data["affect_channels"] = list(self.affect_channels)
        return data


def _bounded(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _stable_unit(text: str) -> float:
    digest = hashlib.blake2b(text.encode("utf-8"), digest_size=8).digest()
    return int.from_bytes(digest, "big") / float(2**64 - 1)


def _round(value: float) -> float:
    return round(float(value), 9)


def _digest_payload(payload: Any) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def _relation_family_flux(edges: Iterable[LexicalHolonomyEdge]) -> tuple[float, float, int]:
    similarity = 0.0
    opposition = 0.0
    count = 0
    for edge in edges:
        count += 1
        if edge.relation_family == "equivalence_or_similarity":
            similarity += abs(float(edge.weight))
        elif edge.relation_family == "opposition_or_divergence":
            opposition += abs(float(edge.weight))
        elif edge.relation_family == "semantic_convergence":
            similarity += 0.5 * abs(float(edge.weight))
    scale = max(1.0, float(count))
    return _bounded(similarity / scale), _bounded(opposition / scale), count


def _dominant_colour(affect: Mapping[str, float], *, phase_seed: str) -> tuple[float, str]:
    # Colour is a scalar-context hue label, not a UI colour and not a material
    # property.  It is determined from affect dominance plus stable phase.
    base_hue = 360.0 * _stable_unit("colour|" + phase_seed)
    dominant = max(AFFECT_CHANNELS, key=lambda key: float(affect.get(key, 0.0)))
    offsets = {
        "sarcasm": 285.0,
        "excitement": 48.0,
        "tension": 12.0,
        "relief": 158.0,
        "fear": 232.0,
    }
    names = {
        "sarcasm": "violet_ironic_context",
        "excitement": "gold_excited_context",
        "tension": "red_tension_context",
        "relief": "green_relief_context",
        "fear": "blue_dark_fear_context",
    }
    hue = (0.25 * base_hue + 0.75 * offsets[dominant]) % 360.0
    return _round(hue), names[dominant]


def _affect_scalars(text: str, *, phase_seed: str) -> dict[str, float]:
    lower = text.lower()
    values: dict[str, float] = {}
    for channel, keywords in AFFECT_KEYWORDS.items():
        keyword_hits = sum(1 for word in keywords if word in lower)
        keyword_boost = min(0.55, 0.18 * keyword_hits)
        # Small deterministic prior prevents a zeroed scalar field when cards do
        # not carry affect words yet, while keeping the result marked as proxy.
        prior = 0.12 + 0.28 * _stable_unit(f"affect|{channel}|{phase_seed}")
        values[channel] = _round(_bounded(prior + keyword_boost))
    return values


def _notes_by_card(repo_root: str | Path = ".") -> dict[str, list[WordKnowledgeNote]]:
    out: dict[str, list[WordKnowledgeNote]] = {}
    for note in build_word_knowledge_notes(repo_root):
        out.setdefault(note.card_id, []).append(note)
    return out


def _edges_by_card(repo_root: str | Path = ".") -> dict[str, list[LexicalHolonomyEdge]]:
    units = extract_lexical_units(repo_root)
    lexical_to_card = {unit.lexical_id: unit.card_id for unit in units}
    out: dict[str, list[LexicalHolonomyEdge]] = {}
    for edge in build_lexical_holonomy_edges(repo_root):
        card_id = lexical_to_card.get(edge.source_lexical_id)
        if card_id:
            out.setdefault(card_id, []).append(edge)
    return out


def _mean_confidence(notes: Iterable[WordKnowledgeNote]) -> float:
    vals = [float(note.knowledge_confidence) for note in notes]
    if not vals:
        return 0.0
    return _bounded(sum(vals) / len(vals))


def _card_text(card: LNSLanguageCard, vector: CIELingoVector) -> str:
    fields: list[str] = [card.card_id, card.canonical_label, card.card_kind, card.source_path]
    fields.extend(card.semantic_axes)
    for labels in card.languages.values():
        fields.extend(labels)
    fields.extend(vector.noema_document.get("tags", []))
    return " ".join(str(x) for x in fields if x)


def tensor_scalar_state_from_card(
    card: LNSLanguageCard,
    *,
    edges_by_card: Mapping[str, list[LexicalHolonomyEdge]] | None = None,
    notes_by_card: Mapping[str, list[WordKnowledgeNote]] | None = None,
) -> TensorScalarWordState:
    """Build the mixed field state for one CIELingo language card."""
    vector = vectorize_card(card)
    vec = vector.vector
    local_edges = list((edges_by_card or {}).get(card.card_id, []))
    sim_flux, opp_flux, rel_count = _relation_family_flux(local_edges)
    confidence = _mean_confidence((notes_by_card or {}).get(card.card_id, []))

    relation_load = _bounded(math.log1p(rel_count) / math.log(64.0))
    label_entropy = _bounded(vec[19])
    phase_tension = _bounded(vec[6])
    j_total = _bounded(vec[13])

    text = _card_text(card, vector)
    affect = _affect_scalars(text, phase_seed=card.card_id)
    affect_tension = _bounded((affect["tension"] + affect["fear"] + affect["sarcasm"]) / 3.0)
    affect_lightness = _bounded((affect["relief"] + affect["excitement"]) / 2.0)

    density = _bounded(0.42 * vec[0] + 0.28 * relation_load + 0.18 * label_entropy + 0.12 * affect_tension)
    viscosity = _bounded(0.34 * phase_tension + 0.22 * opp_flux + 0.22 * (1.0 - confidence) + 0.22 * affect_tension)
    saturation = _bounded(0.30 * label_entropy + 0.24 * relation_load + 0.20 * affect_tension + 0.16 * affect_lightness + 0.10 * sim_flux)
    hue, colour_name = _dominant_colour(affect, phase_seed=card.card_id)
    semantic_time_resistance = _bounded((density * (0.55 + viscosity) * (0.65 + saturation)) + 0.16 * affect_tension - 0.08 * affect["relief"])
    semantic_time_thinning = _bounded((0.45 * affect_lightness + 0.25 * sim_flux + 0.18 * confidence) * (1.0 - 0.55 * semantic_time_resistance))
    scalar_context_potential = _round(KAPPA_INFO * (density + viscosity + saturation + semantic_time_resistance))

    tensor = (
        (_round(vec[0]), _round(vec[5]), _round(relation_load)),
        (_round(vec[7]), _round(vec[8]), _round(j_total)),
        (_round(sim_flux), _round(opp_flux), _round(phase_tension)),
    )
    tensor_trace = _round(tensor[0][0] + tensor[1][1] + tensor[2][2])
    # Cheap determinant proxy for stability/orientation without adding numpy.
    determinant_proxy = _round(
        tensor[0][0] * tensor[1][1] * tensor[2][2]
        + tensor[0][1] * tensor[1][2] * tensor[2][0]
        + tensor[0][2] * tensor[1][0] * tensor[2][1]
        - tensor[0][2] * tensor[1][1] * tensor[2][0]
        - tensor[0][1] * tensor[1][0] * tensor[2][2]
        - tensor[0][0] * tensor[1][2] * tensor[2][1]
    )

    scalar = ContextScalarField(
        schema="cielingo/context-scalar-field/v0.1",
        field_kind="imaginary_context_scalar_medium",
        channels=SCALAR_CHANNELS,
        density=_round(density),
        viscosity=_round(viscosity),
        colour_hue_deg=hue,
        colour_name=colour_name,
        saturation=_round(saturation),
        affect_scalars=affect,
        semantic_time_resistance=_round(semantic_time_resistance),
        semantic_time_thinning=_round(semantic_time_thinning),
        scalar_context_potential=scalar_context_potential,
        epistemic_note=(
            "Local scalar-context proxy. Sarcasm/excitement/tension/relief/fear are inferred from "
            "card text, lexical load and phase features; external lexical/affective calibration is still required."
        ),
    )
    digest = _digest_payload({"schema": TENSOR_SCALAR_SCHEMA, "card_id": card.card_id, "tensor": tensor, "scalar": scalar.as_dict()})

    noema_document = {
        "schema": "noema/cielingo-tensor-scalar-document/v0.1",
        "card_id": card.card_id,
        "vector_digest": vector.vector_digest,
        "field_digest": digest,
        "source_path": card.source_path,
        "field_roles": {
            "real": "rank_2_information_exchange_tensor",
            "imaginary": "context_affect_scalar_medium",
        },
        "scalar_channels": list(SCALAR_CHANNELS),
        "affect_channels": list(AFFECT_CHANNELS),
        "epistemic_status": "local tensor-scalar proxy; not external NOEMA SoT write",
    }
    cqcl_payload = {
        "real_exchange_trace": tensor_trace,
        "real_exchange_det_proxy": determinant_proxy,
        "context_density": scalar.density,
        "context_viscosity": scalar.viscosity,
        "context_saturation": scalar.saturation,
        "semantic_time_resistance": scalar.semantic_time_resistance,
        "semantic_time_thinning": scalar.semantic_time_thinning,
        "scalar_context_potential": scalar.scalar_context_potential,
    }
    htri_payload: dict[str, float | int | str] = {
        **vector.htri_state,
        "context_viscosity": scalar.viscosity,
        "context_density": scalar.density,
        "phase_drag": scalar.semantic_time_resistance,
        "colour_hue_deg": scalar.colour_hue_deg,
        "colour_name": scalar.colour_name,
    }
    orchorbital_payload = {
        **vector.orchorbital_payload,
        "tensor_scalar_field_digest": digest,
        "semantic_time_resistance": scalar.semantic_time_resistance,
        "scalar_context": scalar.as_dict(),
    }
    return TensorScalarWordState(
        schema=TENSOR_SCALAR_SCHEMA,
        card_id=card.card_id,
        canonical_label=card.canonical_label,
        source_path=card.source_path,
        tensor_role="real_information_exchange_tensor",
        scalar_role="imaginary_context_affect_scalar",
        tensor_shape=TENSOR_SHAPE,
        tensor_axes=TENSOR_AXES,
        real_exchange_tensor=tensor,
        tensor_trace=tensor_trace,
        tensor_determinant_proxy=determinant_proxy,
        scalar_context=scalar,
        lexical_relation_count=rel_count,
        lexical_similarity_flux=_round(sim_flux),
        lexical_opposition_flux=_round(opp_flux),
        knowledge_confidence=_round(confidence),
        vector_digest=vector.vector_digest,
        noema_document=noema_document,
        cqcl_payload=cqcl_payload,
        htri_payload=htri_payload,
        orchorbital_payload=orchorbital_payload,
    )


def tensor_scalar_report(
    repo_root: str | Path = ".",
    *,
    query: str = "",
    limit: int | None = None,
) -> dict[str, Any]:
    """Build a CIELingo tensor-scalar report through the local NOEMA/LNS surface."""
    cards = select_vector_cards(repo_root, query=query, limit=limit)
    edge_index = _edges_by_card(repo_root)
    note_index = _notes_by_card(repo_root)
    states = [tensor_scalar_state_from_card(card, edges_by_card=edge_index, notes_by_card=note_index) for card in cards]
    count = len(states)
    if count:
        mean_density = sum(s.scalar_context.density for s in states) / count
        mean_viscosity = sum(s.scalar_context.viscosity for s in states) / count
        mean_saturation = sum(s.scalar_context.saturation for s in states) / count
        mean_resistance = sum(s.scalar_context.semantic_time_resistance for s in states) / count
        mean_thinning = sum(s.scalar_context.semantic_time_thinning for s in states) / count
        mean_confidence = sum(s.knowledge_confidence for s in states) / count
    else:
        mean_density = mean_viscosity = mean_saturation = mean_resistance = mean_thinning = mean_confidence = 0.0
    registry_digest = _digest_payload([{"card_id": s.card_id, "field_digest": s.noema_document["field_digest"]} for s in states])
    report = TensorScalarReport(
        schema="cielingo/tensor-scalar-field-report/v0.1",
        source_role="local_noema_lns_tensor_scalar_context_surface",
        epistemic_status=(
            "diagnostic local field: real information exchange tensor + imaginary context scalar; "
            "not external NOEMA SoT write and not psychological affect measurement"
        ),
        card_count=count,
        tensor_shape=TENSOR_SHAPE,
        scalar_channels=SCALAR_CHANNELS,
        affect_channels=AFFECT_CHANNELS,
        mean_density=_round(mean_density),
        mean_viscosity=_round(mean_viscosity),
        mean_saturation=_round(mean_saturation),
        mean_semantic_time_resistance=_round(mean_resistance),
        mean_semantic_time_thinning=_round(mean_thinning),
        mean_knowledge_confidence=_round(mean_confidence),
        high_resistance_count=sum(1 for s in states if s.scalar_context.semantic_time_resistance >= 0.55),
        high_viscosity_count=sum(1 for s in states if s.scalar_context.viscosity >= 0.55),
        registry_digest=registry_digest,
        states=[s.as_dict() for s in states],
    )
    return report.as_dict()


def write_tensor_scalar_report(path: str | Path, report: Mapping[str, Any]) -> Path:
    """Write a tensor-scalar report as deterministic JSON."""
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    return out


__all__ = [
    "AFFECT_CHANNELS",
    "SCALAR_CHANNELS",
    "TENSOR_AXES",
    "TENSOR_SCALAR_SCHEMA",
    "TENSOR_SHAPE",
    "ContextScalarField",
    "TensorScalarReport",
    "TensorScalarWordState",
    "tensor_scalar_state_from_card",
    "tensor_scalar_report",
    "write_tensor_scalar_report",
]
