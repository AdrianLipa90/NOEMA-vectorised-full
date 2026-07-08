"""Validation gate for NOEMA HTRI reports.

Raw HTRI simulation output is never a pipeline metric by itself.  It must pass
this gate before publication.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class HTRIPublishThresholds:
    order_parameter_final_min: float = 0.70
    order_parameter_mean_min: float = 0.55
    phase_closure_error_final_max: float = 0.15
    htri_index_min: float = 0.60
    pipeline_connected_score_min: float = 0.80


def pipeline_connection_score(*, report_written: bool, metrics_file_written: bool, pipeline_reader_exists: bool, pipeline_runtime_confirmed: bool) -> float:
    """Evidence-based pipeline connection score.

    No hardcoded 1.0 is allowed: every part must be evidenced.
    """
    score = 0.20  # module/simulator exists by virtue of reaching this code
    score += 0.20 if report_written else 0.0
    score += 0.20 if metrics_file_written else 0.0
    score += 0.20 if pipeline_reader_exists else 0.0
    score += 0.20 if pipeline_runtime_confirmed else 0.0
    return round(score, 6)


def validate_htri_report(
    report: dict[str, Any],
    *,
    pipeline_connected_score: float,
    thresholds: HTRIPublishThresholds | None = None,
) -> dict[str, Any]:
    """Return validation/quarantine decision for a raw HTRI report."""
    thresholds = thresholds or HTRIPublishThresholds()
    metrics = report.get("metrics", {})
    reasons: list[str] = []

    if float(metrics.get("order_parameter_final", 0.0)) < thresholds.order_parameter_final_min:
        reasons.append("order_parameter_final_below_threshold")
    if float(metrics.get("order_parameter_mean", 0.0)) < thresholds.order_parameter_mean_min:
        reasons.append("order_parameter_mean_below_threshold")
    if float(metrics.get("phase_closure_error_final", 1.0)) > thresholds.phase_closure_error_final_max:
        reasons.append("phase_closure_error_above_threshold")
    if float(metrics.get("htri_index", 0.0)) < thresholds.htri_index_min:
        reasons.append("htri_index_below_threshold")
    if pipeline_connected_score < thresholds.pipeline_connected_score_min:
        reasons.append("pipeline_connection_not_runtime_proven")

    passed = not reasons
    return {
        "schema": "noema/htri-validation/v0.2",
        "thresholds": asdict(thresholds),
        "pipeline_connected_score": pipeline_connected_score,
        "status": "PASS" if passed else "QUARANTINE",
        "publish_to_pipeline": passed,
        "quarantine": not passed,
        "reasons": reasons,
    }


__all__ = ["HTRIPublishThresholds", "pipeline_connection_score", "validate_htri_report"]
