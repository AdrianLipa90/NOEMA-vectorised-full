from __future__ import annotations

from src.ciel_sot_agent.cielingo_bridge import build_lingo_frame
from scripts.cielingo_ablation_benchmark import run_ablation_benchmark


def test_ablation_benchmark_reports_structural_diff() -> None:
    report = run_ablation_benchmark(
        [
            "Here now we ask about memory and truth.",
            "Spotkajmy się gdzieś kiedyś.",
        ],
        language="en",
    )

    assert report["sample_count"] == 2
    assert report["mean_length_delta"] > 0
    assert report["mean_projection_confidence"] >= 0.0
    assert 0.0 <= report["mean_quality_score"] <= 1.0
    assert report["rows"][0]["enhanced"]["summary"].startswith("CIELingo|")
    assert 0.0 <= report["rows"][0]["enhanced"]["quality_score"] <= 1.0
    assert report["rows"][0]["delta"]["length"] > 0


def test_ablation_uses_real_lingo_frame_signals() -> None:
    frame = build_lingo_frame("Here now we ask somewhere?", ciel_state={"language": "en"})
    report = run_ablation_benchmark(["Here now we ask somewhere?"], language="en")

    assert report["rows"][0]["enhanced"]["deictic_count"] == frame["deictic_frame"]["anchor_count"]
    assert report["rows"][0]["enhanced"]["unresolved_count"] == len(frame["unresolved"])
    assert 0.0 <= report["rows"][0]["enhanced"]["quality_score"] <= 1.0
