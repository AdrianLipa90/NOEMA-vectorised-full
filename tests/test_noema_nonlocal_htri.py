from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from noema_htri import (
    KuramotoHTRIConfig,
    build_pipeline_metrics,
    pipeline_connection_score,
    run_kuramoto_htri_120,
    validate_htri_report,
)
from noema_nonlocal_db import load_cards, validate_cards


def test_noema_nonlocal_cards_validate() -> None:
    cards = load_cards(ROOT)
    validation = validate_cards(cards)
    assert validation["valid"] is True
    assert validation["card_count"] >= 10


def test_htri_kuramoto_120_metrics_are_bounded_and_not_hardcoded_pipeline_score() -> None:
    report = run_kuramoto_htri_120(
        manifest_digest="a" * 64,
        card_registry_digest="b" * 64,
        config=KuramotoHTRIConfig(steps=32, n_oscillators=120),
    )
    metrics = report["metrics"]
    assert metrics["oscillator_count"] == 120
    assert 0.0 <= metrics["htri_index"] <= 1.0
    assert 0.0 <= metrics["order_parameter_final"] <= 1.0
    assert 0.0 <= metrics["phase_closure_error_final"] <= 1.0
    assert metrics["pipeline_connected_score"] is None
    assert "j_functional_proxy" not in metrics
    assert "htri_diagnostic_cost" in metrics


def test_htri_validation_quarantines_unproven_pipeline_connection() -> None:
    report = run_kuramoto_htri_120(
        manifest_digest="a" * 64,
        card_registry_digest="b" * 64,
        config=KuramotoHTRIConfig(steps=32, n_oscillators=120),
    )
    score = pipeline_connection_score(
        report_written=True,
        metrics_file_written=False,
        pipeline_reader_exists=True,
        pipeline_runtime_confirmed=False,
    )
    validation = validate_htri_report(report, pipeline_connected_score=score)
    assert score < 1.0
    assert validation["publish_to_pipeline"] is False
    assert validation["quarantine"] is True
    assert "pipeline_connection_not_runtime_proven" in validation["reasons"]


def test_pipeline_metrics_require_validation_pass() -> None:
    report = run_kuramoto_htri_120(
        manifest_digest="a" * 64,
        card_registry_digest="b" * 64,
        config=KuramotoHTRIConfig(steps=128, n_oscillators=120),
    )
    validation = validate_htri_report(report, pipeline_connected_score=1.0)
    if validation["publish_to_pipeline"]:
        metrics = build_pipeline_metrics(report, validation)
        assert metrics["publication_status"] == "validated"
    else:
        try:
            build_pipeline_metrics(report, validation)
        except ValueError:
            pass
        else:  # pragma: no cover - defensive
            raise AssertionError("unvalidated HTRI report was published")
