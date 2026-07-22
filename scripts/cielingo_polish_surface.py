#!/usr/bin/env python3
"""Run CIELingo Polish linguistic surface diagnostics."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cielingo.polish.grammar_algorithms import analyze_polish_sentence
from cielingo.polish.j_functionals import compute_language_j_functional
from cielingo.polish.linguistic_database import load_polish_database
from cielingo.polish.lingophysics_bridge import load_lingophysics_summary


def _check_noema_runtime() -> bool:
    """Sprawdź czy NOEMA surface runtime jest dostępny przez pliki stanu."""
    candidates = [
        Path(__file__).resolve().parent.parent / "runtime" / "mcp_ticks.jsonl",
        Path(__file__).resolve().parent.parent / "runtime" / "phasenav" / "latest",
    ]
    return any(p.exists() for p in candidates)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--text", default="Jan widzi Marię.")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    db = load_polish_database(root)
    noema_available = _check_noema_runtime()
    report = {
        "schema": "cielingo/polish-linguistic-surface-report/v0.1",
        "generated_at": datetime.now(UTC).isoformat(),
        "database_summary": db.database_summary(),
        "lingophysics_summary": load_lingophysics_summary(root),
        "analysis": analyze_polish_sentence(args.text, repo_root=root.as_posix()),
        "j_functional": compute_language_j_functional(args.text, repo_root=root.as_posix()),
        "execution_layer": "cuda" if noema_available else "fallback_cpu_ram",
        "nonlocal_claim_allowed": False,
        "primary_noema_runtime_available": noema_available,
    }
    if args.write:
        out = root / "integration" / "reports" / "cielingo_polish" / "polish_linguistic_surface.report.noema.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False), encoding="utf-8")
        report["written"] = {"report": out.as_posix()}
    print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False))
    return 0 if report["analysis"]["grammar_status"] in {"PASS", "UNRESOLVED"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
