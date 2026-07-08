from __future__ import annotations

from src.ciel_sot_agent.cielingo_client import analyze_text, run_cielingo_client
from src.ciel_sot_agent.cielingo_quality_benchmark import run_quality_benchmark


def test_cielingo_client_returns_quality_report() -> None:
    result = analyze_text("Here now we resolve memory, identity, and truth.", language="en")

    assert result["schema"].startswith("ciel-sot-agent/cielingo-client-analysis/")
    assert result["summary"].startswith("CIELingo|")
    assert result["phase_summary"].startswith("PhaseNav|")
    assert result["frame"]["summary"] == result["summary"]
    assert 0.0 <= result["quality_score"] <= 1.0
    assert result["quality_breakdown"]["concept_count"] >= 1


def test_cielingo_client_rewards_richer_prompt() -> None:
    sparse = analyze_text("Hi.", language="en")
    rich = analyze_text(
        "Here now we resolve memory, identity, uncertainty, and phase coupling.",
        language="en",
    )

    assert rich["quality_score"] > sparse["quality_score"]
    assert rich["quality_breakdown"]["richness"] > sparse["quality_breakdown"]["richness"]


def test_cielingo_client_batches_samples() -> None:
    report = run_cielingo_client(
        [
            "Hi.",
            "Here now we resolve memory, identity, and truth.",
        ],
        language="en",
    )

    assert report["schema"].startswith("ciel-sot-agent/cielingo-client-run/")
    assert report["client_schema"].startswith("ciel-sot-agent/cielingo-client-analysis/")
    assert report["sample_count"] == 2
    assert 0.0 <= report["mean_quality_score"] <= 1.0
    assert report["best_sample"]["quality_score"] >= report["worst_sample"]["quality_score"]


def test_cielingo_quality_benchmark_prefers_richer_sample() -> None:
    report = run_quality_benchmark(
        [
            "Hi.",
            "Here now we resolve memory, identity, and truth.",
        ],
        language="en",
    )

    assert report["schema"].startswith("ciel-sot-agent/cielingo-quality-benchmark/")
    assert report["client_schema"].startswith("ciel-sot-agent/cielingo-client-analysis/")
    assert report["sample_count"] == 2
    assert 0.0 <= report["mean_quality_score"] <= 1.0
    assert report["best_sample"]["quality_score"] >= report["worst_sample"]["quality_score"]
