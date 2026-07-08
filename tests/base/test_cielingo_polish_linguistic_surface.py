from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from cielingo.polish.grammar_algorithms import analyze_polish_sentence, tokenize_polish
from cielingo.polish.holonomies import compute_holonomy_report
from cielingo.polish.j_functionals import KAPPA_INFO, compute_language_j_functional
from cielingo.polish.linguistic_database import load_polish_database
from cielingo.polish.lingophysics_bridge import load_lingophysics_summary


def test_polish_database_loads_seed_layers() -> None:
    db = load_polish_database(Path.cwd())
    summary = db.database_summary()
    assert "noun" in summary["parts_of_speech"]
    assert "predicate" in summary["sentence_parts"]
    assert summary["case_count"] == 7
    assert summary["lexeme_count"] >= 10
    assert "identity_relevance" in summary["semantic_mass_axes"]


def test_polish_sentence_analysis_roles_and_valency() -> None:
    analysis = analyze_polish_sentence("Jan widzi Marię.", repo_root=Path.cwd().as_posix())
    assert analysis["grammar_status"] == "PASS"
    assert analysis["valency"]["roles"]["Agent"] == "Jan"
    assert analysis["valency"]["roles"]["Theme"] == "Marię"
    assert analysis["tokens"][-1]["operator"] == "cycle_closure"


def test_holonomy_report_for_case_marked_sentence() -> None:
    analysis = analyze_polish_sentence("Jan widzi Marię.", repo_root=Path.cwd().as_posix())
    hol = compute_holonomy_report(analysis)
    assert hol["holonomy_preservation_score"] > 0.5
    assert any(r["operator"] == "word_order_holonomy" for r in hol["reports"])


def test_language_j_functional_is_bounded_and_uses_kappa_info() -> None:
    report = compute_language_j_functional("Jan widzi Marię.", repo_root=Path.cwd().as_posix())
    assert 0.0 <= report["J_language"] <= 1.1
    assert abs(report["kappa_info"] - KAPPA_INFO) < 1e-15
    assert report["status"] in {"PASS", "REVIEW"}
    assert report["components"]["valency_penalty"] == 0.0


def test_lingophysics_bridge_detects_existing_lns_when_present() -> None:
    summary = load_lingophysics_summary(Path.cwd())
    # In standalone patch tests this may be unavailable; in full repo it must be true.
    if summary["available"]:
        assert "alg:case_gauge" in summary["algorithm_ids"]
        assert "operator_coverage" in summary["metric_ids"]
        assert summary["frame_count"] > 0
    else:
        assert summary["reason"] == "lingophysics LNS root not found"


def test_polish_surface_cli_writes_report() -> None:
    proc = subprocess.run(
        [sys.executable, "scripts/cielingo_polish_surface.py", "--write", "--text", "Jan widzi Marię."],
        cwd=Path.cwd(), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout[-1000:]
    report = json.loads(proc.stdout)
    assert report["analysis"]["grammar_status"] == "PASS"
    assert report["j_functional"]["components"]["valency_penalty"] == 0.0
