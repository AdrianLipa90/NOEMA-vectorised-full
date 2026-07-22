"""CIELingo triadic output vectorization.

The output triad turns parsed phase sense into a runtime-ready 3-lane vector:

1. comprehension lane: word-to-phase understanding and confidence;
2. inference lane: shared CIELingo vector/HTRI/J/CQCL transport;
3. expression lane: output readiness through tensor-scalar resistance/thinning.

Each lane is 24D to remain compatible with the CIELingo vector surface.  The
full output vector is therefore 72D.  This is a local diagnostic/runtime adapter,
not a claim of external NOEMA SoT execution or physical HTRI measurement.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Iterable, Mapping

from .htri_phase_bus import BASE_FREQUENCY_HZ, DEFAULT_OSCILLATORS, KAPPA_INFO
from .phase_sense_parser import parse_text_to_phase_sense
from .vector_surface import VECTOR_COMPONENTS, VECTOR_DIM, vectorize_card
from .lns_language_cards import load_all_language_cards

TRIADIC_OUTPUT_SCHEMA = "cielingo/triadic-output-vector/v0.1"
TRIAD_LANES: tuple[str, ...] = ("comprehension", "inference", "expression")
TRIAD_VECTOR_DIM = VECTOR_DIM * len(TRIAD_LANES)


def _bounded(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _round(value: float) -> float:
    return round(float(value), 9)


def _mean_vectors(vectors: list[tuple[float, ...]]) -> tuple[float, ...]:
    if not vectors:
        return tuple(0.0 for _ in range(VECTOR_DIM))
    return tuple(_round(sum(v[i] for v in vectors) / len(vectors)) for i in range(VECTOR_DIM))


def _digest_payload(payload: Any) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def _phase_alignment_to_bus(phase_rad: float, *, oscillator_id: int = 0) -> float:
    bus_phase = (2.0 * math.pi * oscillator_id / max(1, DEFAULT_OSCILLATORS)) % (2.0 * math.pi)
    return _bounded(0.5 + 0.5 * math.cos(phase_rad - bus_phase))


@dataclass(frozen=True)
class TriadicOutputVector:
    """72D output vector with adapter payloads."""

    schema: str
    language_hint: str | None
    input_text_sha256: str
    vector_dim: int
    lane_dim: int
    lanes: tuple[str, ...]
    lane_components: tuple[str, ...]
    comprehension_lane: tuple[float, ...]
    inference_lane: tuple[float, ...]
    expression_lane: tuple[float, ...]
    output_vector: tuple[float, ...]
    output_digest: str
    cqcl_output_variables: dict[str, float]
    htri_output_state: dict[str, float | int]
    noema_output_document: dict[str, Any]
    orchorbital_output_payload: dict[str, Any]
    phase_sense_report: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        for key in ("lanes", "lane_components", "comprehension_lane", "inference_lane", "expression_lane", "output_vector"):
            data[key] = list(data[key])
        return data


@dataclass(frozen=True)
class OnVivoOutputTestReport:
    """A local on-vivo style runtime sample report."""

    schema: str
    source_role: str
    epistemic_status: str
    token_count: int
    matched_token_count: int
    unknown_token_count: int
    vector_dim: int
    output_digest: str
    output_readiness: float
    semantic_time_resistance: float
    semantic_time_thinning: float
    phase_lock: float
    needs_supervised_grammar_review: bool
    output: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _cards_for_phase_report(repo_root: str | Path, phase_report: Mapping[str, Any]) -> list[Any]:
    wanted = {
        (str(t.get("card_id")), str(t.get("source_path")))
        for t in phase_report.get("tokens", [])
        if t.get("matched") and t.get("card_id") and t.get("source_path")
    }
    cards = []
    for card in load_all_language_cards(repo_root):
        if (card.card_id, card.source_path) in wanted:
            cards.append(card)
    return cards


def _comprehension_lane(phase_report: Mapping[str, Any]) -> tuple[float, ...]:
    token_count = max(1, int(phase_report.get("token_count", 0)))
    matched_ratio = _bounded(float(phase_report.get("matched_ratio", 0.0)))
    unknown_ratio = _bounded(float(phase_report.get("unknown_token_count", 0)) / token_count)
    confidence = _bounded(float(phase_report.get("mean_knowledge_confidence", 0.0)))
    mass = _bounded(float(phase_report.get("mean_semantic_mass", 0.0)))
    density = _bounded(float(phase_report.get("mean_density", 0.0)))
    viscosity = _bounded(float(phase_report.get("mean_viscosity", 0.0)))
    saturation = _bounded(float(phase_report.get("mean_saturation", 0.0)))
    resistance = _bounded(float(phase_report.get("mean_semantic_time_resistance", 0.0)))
    thinning = _bounded(float(phase_report.get("mean_semantic_time_thinning", 0.0)))
    phase = float(phase_report.get("dominant_phase_rad", 0.0))
    token_norm = _bounded(token_count / 32.0)
    phase_alignment = _phase_alignment_to_bus(phase)
    # M8–M11 derived
    meta_reflexive_depth = _bounded(resistance / max(confidence, 0.001))
    meta_cognitive_curvature = _bounded((confidence + mass + density) / 3.0)
    meta_loop_coherence = _bounded(phase_alignment * (1.0 - resistance))
    temporal_spiral_phase = _bounded(0.5 + 0.5 * math.sin(phase / 2.0))
    temporal_memory_decay = _bounded(1.0 - (1.0 / (1.0 + token_count)))
    temporal_anticipation = _bounded(thinning * (1.0 + confidence) / 2.0)
    imaginal_symbolic_field = _bounded(token_norm * (1.0 + phase_alignment) / 2.0)
    imaginal_resonance = _bounded(mass * phase_alignment)
    imaginal_narrative_coherence = _bounded((matched_ratio + confidence) / 2.0)
    quantum_berry_phase = _bounded((1.0 - unknown_ratio) * (1.0 + phase_alignment) / 2.0)
    quantum_topological_order = _bounded(abs(thinning - 0.5) * 2.0)
    quantum_entanglement_entropy = _bounded((mass + confidence + density) / 3.0)
    values = (
        # --- 24 legacy (indices 0–23) ---
        matched_ratio,
        unknown_ratio,
        confidence,
        mass,
        density,
        viscosity,
        saturation,
        resistance,
        thinning,
        0.5 + 0.5 * math.sin(phase),
        0.5 + 0.5 * math.cos(phase),
        phase_alignment,
        _bounded(1.0 - resistance),
        _bounded(confidence * matched_ratio),
        _bounded((mass + confidence) / 2.0),
        _bounded((density + saturation) / 2.0),
        _bounded(viscosity * resistance),
        _bounded(thinning * matched_ratio),
        token_norm,
        _bounded(1.0 - unknown_ratio),
        _bounded(KAPPA_INFO * (1.0 + mass + density)),
        _bounded(abs(math.sin(phase / 2.0))),
        _bounded(abs(math.cos(phase / 2.0))),
        _bounded((matched_ratio + confidence + thinning) / 3.0),
        # --- M8–M11 (indices 24–35) ---
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
    return tuple(_round(v) for v in values)


def _expression_lane(comprehension: tuple[float, ...], inference: tuple[float, ...], phase_report: Mapping[str, Any]) -> tuple[float, ...]:
    resistance = _bounded(float(phase_report.get("mean_semantic_time_resistance", 0.0)))
    thinning = _bounded(float(phase_report.get("mean_semantic_time_thinning", 0.0)))
    confidence = _bounded(float(phase_report.get("mean_knowledge_confidence", 0.0)))
    readiness = _bounded(0.45 * comprehension[23] + 0.35 * inference[5] + 0.20 * thinning - 0.25 * resistance)
    values = []
    for i in range(VECTOR_DIM):
        mixed = 0.42 * comprehension[i] + 0.42 * inference[i] + 0.16 * readiness
        if i in {5, 13, 14, 15, 16}:
            mixed = 0.50 * mixed + 0.25 * confidence + 0.25 * thinning
        if i in {6, 7, 8}:
            mixed = 0.55 * mixed + 0.45 * (1.0 - resistance)
        values.append(_round(_bounded(mixed)))
    return tuple(values)


def vectorize_triadic_output(
    text: str,
    repo_root: str | Path = ".",
    *,
    language_hint: str | None = "pl",
) -> dict[str, Any]:
    """Vectorize a text sample into the 72D output triad."""
    phase_report = parse_text_to_phase_sense(text, repo_root, language_hint=language_hint)
    cards = _cards_for_phase_report(repo_root, phase_report)
    card_vectors = [vectorize_card(card).vector for card in cards]
    inference = _mean_vectors(card_vectors)
    comprehension = _comprehension_lane(phase_report)
    expression = _expression_lane(comprehension, inference, phase_report)
    output_vector = tuple(_round(x) for lane in (comprehension, inference, expression) for x in lane)
    digest = _digest_payload({"schema": TRIADIC_OUTPUT_SCHEMA, "text_sha": phase_report["input_text_sha256"], "vector": output_vector})

    readiness = _bounded(expression[23])
    phase_lock = _bounded((comprehension[11] + inference[5] + expression[5]) / 3.0)
    resistance = _bounded(float(phase_report.get("mean_semantic_time_resistance", 0.0)))
    thinning = _bounded(float(phase_report.get("mean_semantic_time_thinning", 0.0)))
    cqcl = {
        "comprehension": comprehension[23],
        "inference_alignment": inference[5],
        "expression_readiness": readiness,
        "semantic_time_resistance": resistance,
        "semantic_time_thinning": thinning,
        "phase_lock": phase_lock,
        "output_coherence": _bounded(0.40 * readiness + 0.35 * phase_lock + 0.25 * (1.0 - resistance)),
    }
    htri = {
        "base_frequency_hz": round(BASE_FREQUENCY_HZ, 9),
        "omega0_rad_s": round(2.0 * math.pi * BASE_FREQUENCY_HZ, 9),
        "oscillator_count": DEFAULT_OSCILLATORS,
        "phase_lock": round(phase_lock, 9),
        "phase_drag": round(resistance, 9),
        "phase_thinning": round(thinning, 9),
        "output_amplitude": round(readiness, 9),
    }
    noema_doc = {
        "schema": "noema/cielingo-triadic-output-vector-document/v0.1",
        "input_text_sha256": phase_report["input_text_sha256"],
        "output_digest": digest,
        "vector_dim": TRIAD_VECTOR_DIM,
        "lane_dim": VECTOR_DIM,
        "lanes": list(TRIAD_LANES),
        "phase_sense_digest": phase_report["phase_sense_digest"],
        "epistemic_status": "local on-vivo style runtime sample; not external NOEMA SoT write",
    }
    orchor = {
        "schema": "cielingo/orchorbital-output-triad-payload/v0.1",
        "output_digest": digest,
        "phase_lock": round(phase_lock, 9),
        "semantic_time_resistance": round(resistance, 9),
        "semantic_time_thinning": round(thinning, 9),
        "recommended_output_lane": "speak" if readiness >= 0.55 else "slow_parse_then_speak",
        "supervision_required": any(t.get("supervision_required") for t in phase_report.get("tokens", [])),
    }
    out = TriadicOutputVector(
        schema=TRIADIC_OUTPUT_SCHEMA,
        language_hint=language_hint,
        input_text_sha256=phase_report["input_text_sha256"],
        vector_dim=TRIAD_VECTOR_DIM,
        lane_dim=VECTOR_DIM,
        lanes=TRIAD_LANES,
        lane_components=VECTOR_COMPONENTS,
        comprehension_lane=comprehension,
        inference_lane=inference,
        expression_lane=expression,
        output_vector=output_vector,
        output_digest=digest,
        cqcl_output_variables={k: round(float(v), 9) for k, v in cqcl.items()},
        htri_output_state=htri,
        noema_output_document=noema_doc,
        orchorbital_output_payload=orchor,
        phase_sense_report=phase_report,
    )
    return out.as_dict()


def on_vivo_output_test(
    text: str,
    repo_root: str | Path = ".",
    *,
    language_hint: str | None = "pl",
) -> dict[str, Any]:
    """Run the local on-vivo style output-vector test."""
    output = vectorize_triadic_output(text, repo_root, language_hint=language_hint)
    phase = output["phase_sense_report"]
    report = OnVivoOutputTestReport(
        schema="cielingo/on-vivo-output-test/v0.1",
        source_role="local_runtime_sample_for_cielingo_output_vectorization",
        epistemic_status="on-vivo means live text sample in local runtime; no phone/hardware claim",
        token_count=int(phase["token_count"]),
        matched_token_count=int(phase["matched_token_count"]),
        unknown_token_count=int(phase["unknown_token_count"]),
        vector_dim=int(output["vector_dim"]),
        output_digest=str(output["output_digest"]),
        output_readiness=float(output["cqcl_output_variables"]["expression_readiness"]),
        semantic_time_resistance=float(output["cqcl_output_variables"]["semantic_time_resistance"]),
        semantic_time_thinning=float(output["cqcl_output_variables"]["semantic_time_thinning"]),
        phase_lock=float(output["cqcl_output_variables"]["phase_lock"]),
        needs_supervised_grammar_review=bool(output["orchorbital_output_payload"]["supervision_required"]),
        output=output,
    )
    return report.as_dict()


def write_output_test_report(path: str | Path, report: Mapping[str, Any]) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    return out


__all__ = [
    "TRIADIC_OUTPUT_SCHEMA",
    "TRIAD_LANES",
    "TRIAD_VECTOR_DIM",
    "TriadicOutputVector",
    "OnVivoOutputTestReport",
    "vectorize_triadic_output",
    "on_vivo_output_test",
    "write_output_test_report",
]
