"""CIELingo client analysis and quality scoring helpers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable

from ciel_geometry.weighting import canonical_weighting

from .cielingo_bridge import build_lingo_frame, render_lingo_summary, render_phasenav_summary

CLIENT_ANALYSIS_SCHEMA_V01 = "ciel-sot-agent/cielingo-client-analysis/v0.1"
CLIENT_RUN_SCHEMA_V01 = "ciel-sot-agent/cielingo-client-run/v0.1"
DEFAULT_SAMPLES = [
    "Here now we ask about memory and truth.",
    "Spotkajmy się gdzieś kiedyś.",
    "The glass contains water and the speaker is here now.",
]


def _clamp01(value: Any, default: float = 0.0) -> float:
    try:
        return max(0.0, min(1.0, float(value)))
    except Exception:
        return float(default)


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def load_lingo_samples(path: Path | None) -> list[str]:
    if path is None:
        return list(DEFAULT_SAMPLES)

    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return [str(item).strip() for item in data if str(item).strip()]
    if isinstance(data, dict) and isinstance(data.get("samples"), list):
        return [str(item).strip() for item in data["samples"] if str(item).strip()]
    raise ValueError("Unsupported sample file format; expected JSON list or {samples: [...]} object.")


def evaluate_lingo_quality(frame: dict[str, Any]) -> dict[str, Any]:
    tokens = [str(item) for item in _as_list(frame.get("tokens")) if str(item).strip()]
    concept_tokens = [str(item) for item in _as_list(frame.get("concept_tokens")) if str(item).strip()]
    operator_tokens = [str(item) for item in _as_list(frame.get("operator_tokens")) if str(item).strip()]
    deictic_frame = _as_dict(frame.get("deictic_frame"))
    noema_route = _as_dict(frame.get("noema_route"))
    phase_projection = _as_dict(frame.get("phase_projection"))
    cqcl_hint = _as_dict(frame.get("cqcl_hint"))
    tau_bridge = _as_dict(frame.get("tau_bridge"))

    token_count = max(1, len(tokens))
    concept_count = len(concept_tokens)
    operator_count = len(operator_tokens)
    deictic_count = int(deictic_frame.get("anchor_count", 0) or 0)
    unresolved_count = len(_as_list(frame.get("unresolved")))
    summary = str(frame.get("summary", ""))

    signal_mass = concept_count + (0.75 * operator_count) + (0.5 * deictic_count)
    richness = _clamp01(signal_mass / max(2.0, token_count + 1.0))
    semantic_mass = _clamp01(richness)

    projection_confidence = _clamp01(frame.get("projection_confidence", 0.0))
    phase_confidence = _clamp01(phase_projection.get("phase_confidence", projection_confidence))
    route_confidence = _clamp01(noema_route.get("confidence", projection_confidence))
    closure_score = _clamp01(1.0 - min(1.0, unresolved_count / max(1.0, concept_count + operator_count + 1.0)))
    htri_coherence = _clamp01((phase_confidence + route_confidence) / 2.0)
    cqcl_signal = _clamp01(cqcl_hint.get("confidence", projection_confidence))
    phase_nav_similarity = _clamp01(
        0.35
        + (0.12 if concept_count else 0.0)
        + (0.12 if operator_count else 0.0)
        + (0.08 if deictic_count else 0.0)
    )
    affective_similarity = _clamp01(0.5 + (0.03 if "!" in summary else 0.0) - (0.04 if unresolved_count else 0.0))
    euler_alignment = _clamp01(float(tau_bridge.get("phase_potential_strength", 0.5) or 0.0))
    novelty = _clamp01(min(1.0, 0.18 * concept_count + 0.12 * operator_count + 0.08 * deictic_count))
    contradiction_risk = _clamp01(
        min(1.0, unresolved_count / max(1.0, token_count / 2.0))
        + (0.2 if not bool(frame.get("composition_valid", False)) else 0.0)
        + (0.1 if not summary else 0.0)
    )

    weights = canonical_weighting(
        semantic_mass=semantic_mass,
        phase_alignment=phase_confidence,
        coherence_index=route_confidence,
        closure_score=closure_score,
        projection_confidence=projection_confidence,
        htri_coherence=htri_coherence,
        cqcl_signal=cqcl_signal,
        phase_nav_similarity=phase_nav_similarity,
        affective_similarity=affective_similarity,
        euler_alignment=euler_alignment,
        novelty=novelty,
        contradiction_risk=contradiction_risk,
        signal_count=float(len(tokens)),
    )
    quality_score = _clamp01(0.65 * weights["composite"] + 0.35 * richness)

    return {
        "quality_score": round(quality_score, 4),
        "quality_breakdown": {
            **weights,
            "richness": round(richness, 4),
            "token_count": token_count,
            "concept_count": concept_count,
            "operator_count": operator_count,
            "deictic_count": deictic_count,
            "unresolved_count": unresolved_count,
            "summary_length": len(summary),
            "phase_confidence": round(phase_confidence, 4),
            "route_confidence": round(route_confidence, 4),
        },
    }


def analyze_text(
    text: str,
    *,
    language: str | None = None,
    ciel_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    ciel_state = dict(ciel_state or {})
    if language is not None:
        ciel_state["language"] = language

    frame = build_lingo_frame(text, ciel_state=ciel_state or None, language=language)
    summary = render_lingo_summary(frame)
    phase_summary = render_phasenav_summary(frame)
    quality = evaluate_lingo_quality(frame)

    return {
        "schema": CLIENT_ANALYSIS_SCHEMA_V01,
        "text": text,
        "language": language or ciel_state.get("language"),
        "summary": summary,
        "phase_summary": phase_summary,
        "quality_score": quality["quality_score"],
        "quality_breakdown": quality["quality_breakdown"],
        "projection_confidence": round(float(frame.get("projection_confidence", 0.0) or 0.0), 4),
        "composition_valid": bool(frame.get("composition_valid", False)),
        "frame": frame,
    }


def _analysis_snapshot(result: dict[str, Any]) -> dict[str, Any]:
    breakdown = _as_dict(result.get("quality_breakdown"))
    return {
        "text": result.get("text", ""),
        "summary": result.get("summary", ""),
        "phase_summary": result.get("phase_summary", ""),
        "quality_score": result.get("quality_score", 0.0),
        "projection_confidence": result.get("projection_confidence", 0.0),
        "composition_valid": result.get("composition_valid", False),
        "concept_count": breakdown.get("concept_count", 0),
        "operator_count": breakdown.get("operator_count", 0),
        "deictic_count": breakdown.get("deictic_count", 0),
        "unresolved_count": breakdown.get("unresolved_count", 0),
    }


def run_cielingo_client(
    samples: Iterable[str],
    *,
    language: str | None = None,
    ciel_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for sample in samples:
        result = analyze_text(sample, language=language, ciel_state=ciel_state)
        rows.append(_analysis_snapshot(result))

    if rows:
        mean_quality_score = sum(float(row["quality_score"]) for row in rows) / len(rows)
        best_sample = max(rows, key=lambda row: float(row["quality_score"]))
        worst_sample = min(rows, key=lambda row: float(row["quality_score"]))
    else:
        mean_quality_score = 0.0
        best_sample = None
        worst_sample = None

    return {
        "schema": CLIENT_RUN_SCHEMA_V01,
        "client_schema": CLIENT_ANALYSIS_SCHEMA_V01,
        "sample_count": len(rows),
        "mean_quality_score": round(mean_quality_score, 4),
        "best_sample": best_sample,
        "worst_sample": worst_sample,
        "rows": rows,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Analyze CIELingo prompts and score quality.")
    parser.add_argument("texts", nargs="*", metavar="TEXT", help="Prompt texts to analyze.")
    parser.add_argument("--samples", type=Path, default=None, help="Optional JSON file with prompts.")
    parser.add_argument("--language", default=None, help="Optional language code passed to CIELingo.")
    parser.add_argument("--output", type=Path, default=None, help="Optional JSON output path.")
    args = parser.parse_args(argv)

    if args.texts:
        samples = [text for text in args.texts if str(text).strip()]
    elif args.samples is not None:
        samples = load_lingo_samples(args.samples)
    else:
        samples = list(DEFAULT_SAMPLES)

    if len(samples) == 1:
        payload: dict[str, Any] = analyze_text(samples[0], language=args.language)
    else:
        payload = run_cielingo_client(samples, language=args.language)

    rendered = json.dumps(payload, indent=2, ensure_ascii=False)
    if args.output is not None:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
