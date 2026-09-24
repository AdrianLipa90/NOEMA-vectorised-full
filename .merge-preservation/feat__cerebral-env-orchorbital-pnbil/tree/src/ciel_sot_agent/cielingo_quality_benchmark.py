"""CIELingo quality benchmark runner for prompt samples."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable

from .cielingo_client import analyze_text, load_lingo_samples

QUALITY_BENCHMARK_SCHEMA_V01 = "ciel-sot-agent/cielingo-quality-benchmark/v0.1"
CLIENT_SCHEMA_V01 = "ciel-sot-agent/cielingo-client-analysis/v0.1"
DEFAULT_SAMPLES = [
    "Here now we resolve memory, identity, and truth.",
    "Spotkajmy się gdzieś kiedyś.",
    "The speaker is here now, but the answer is still unresolved.",
]


def _row_snapshot(result: dict[str, Any]) -> dict[str, Any]:
    breakdown = result.get("quality_breakdown", {})
    if not isinstance(breakdown, dict):
        breakdown = {}
    return {
        "prompt": result.get("text", ""),
        "summary": result.get("summary", ""),
        "phase_summary": result.get("phase_summary", ""),
        "quality_score": result.get("quality_score", 0.0),
        "projection_confidence": result.get("projection_confidence", 0.0),
        "concept_count": breakdown.get("concept_count", 0),
        "operator_count": breakdown.get("operator_count", 0),
        "unresolved_count": breakdown.get("unresolved_count", 0),
        "composition_valid": result.get("composition_valid", False),
    }


def run_quality_benchmark(
    samples: Iterable[str],
    *,
    language: str | None = None,
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for sample in samples:
        result = analyze_text(sample, language=language)
        rows.append(_row_snapshot(result))

    if rows:
        mean_quality_score = sum(float(row["quality_score"]) for row in rows) / len(rows)
        mean_projection_confidence = sum(float(row["projection_confidence"]) for row in rows) / len(rows)
        best_sample = max(rows, key=lambda row: float(row["quality_score"]))
        worst_sample = min(rows, key=lambda row: float(row["quality_score"]))
    else:
        mean_quality_score = 0.0
        mean_projection_confidence = 0.0
        best_sample = None
        worst_sample = None

    return {
        "schema": QUALITY_BENCHMARK_SCHEMA_V01,
        "client_schema": CLIENT_SCHEMA_V01,
        "sample_count": len(rows),
        "mean_quality_score": round(mean_quality_score, 4),
        "mean_projection_confidence": round(mean_projection_confidence, 4),
        "best_sample": best_sample,
        "worst_sample": worst_sample,
        "rows": rows,
    }


def _load_samples(path: Path | None) -> list[str]:
    if path is None:
        return list(DEFAULT_SAMPLES)
    samples = load_lingo_samples(path)
    return samples or list(DEFAULT_SAMPLES)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a CIELingo quality benchmark.")
    parser.add_argument("--samples", type=Path, default=None, help="Optional JSON file with prompt samples.")
    parser.add_argument("--language", default=None, help="Optional language code passed to CIELingo.")
    parser.add_argument("--output", type=Path, default=None, help="Optional JSON report path.")
    args = parser.parse_args(argv)

    report = run_quality_benchmark(_load_samples(args.samples), language=args.language)
    rendered = json.dumps(report, indent=2, ensure_ascii=False)

    if args.output is not None:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
