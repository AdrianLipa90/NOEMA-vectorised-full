"""Pipeline publication helpers for validated HTRI reports."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def build_pipeline_metrics(report: dict[str, Any], validation: dict[str, Any]) -> dict[str, Any]:
    """Build pipeline-facing metrics only from a validation-passing report."""
    if not validation.get("publish_to_pipeline"):
        raise ValueError("HTRI report did not pass validation gate; refuse pipeline publication")
    metrics = report["metrics"]
    return {
        "schema": "noema/pipeline-htri-metrics/v0.2",
        "source": "noema_htri_kuramoto_120",
        "J_functional_contribution_candidate": metrics["htri_diagnostic_cost"],
        "htri_index": metrics["htri_index"],
        "coherence_index": metrics["order_parameter_final"],
        "closure_penalty": metrics["phase_closure_error_final"],
        "pipeline_connected_score": validation["pipeline_connected_score"],
        "publication_status": "validated",
    }


def write_json(path: str | Path, payload: dict[str, Any]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


__all__ = ["build_pipeline_metrics", "write_json"]
