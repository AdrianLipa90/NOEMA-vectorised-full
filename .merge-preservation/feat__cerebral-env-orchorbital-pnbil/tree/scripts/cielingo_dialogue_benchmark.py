#!/usr/bin/env python3
"""Offline dialogue-competence benchmark for CIELingo.

This is not a claim that a system has passed a Turing test.  It is a stable,
inspectable regression gate for prerequisites of credible dialogue: turn type,
reference handling, correction, and calibrated clarification.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from cielingo_core.dialogue_competence import analyze_dialogue


CASES: tuple[dict[str, Any], ...] = (
    {"id": "greeting", "text": "Cześć!", "continuity": {}, "act": "greeting"},
    {"id": "question", "text": "Jak działa pamięć sesyjna?", "continuity": {}, "act": "question"},
    {
        "id": "resolved_reference",
        "text": "Kontynuuj to.",
        "continuity": {"reference_requested": True, "active_topic": ["cielingo"]},
        "reference": 1.0,
    },
    {
        "id": "missing_reference",
        "text": "Kontynuuj to.",
        "continuity": {"reference_requested": True, "active_topic": []},
        "reference": 0.0,
    },
    {
        "id": "correction",
        "text": "Nie chodzi o portal, tylko o CIELingo.",
        "continuity": {},
        "act": "correction",
        "accepted": ["cielingo"],
    },
)


def run() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for case in CASES:
        signal = analyze_dialogue(case["text"], case["continuity"])
        checks = {
            "act": signal.act == case.get("act", signal.act),
            "reference": signal.quality["reference_resolution"] == case.get("reference", signal.quality["reference_resolution"]),
            "revision": list(signal.revision["accepted"]) == case.get("accepted", list(signal.revision["accepted"])),
        }
        rows.append({"id": case["id"], "passed": all(checks.values()), "checks": checks, "signal": signal.to_dict()})
    return {
        "schema": "CIELINGO_DIALOGUE_COMPETENCE_BENCHMARK/v0.1",
        "scope": "offline deterministic dialogue prerequisites; not a Turing-test claim",
        "passed": sum(1 for row in rows if row["passed"]),
        "total": len(rows),
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, help="optional JSON report path")
    args = parser.parse_args()
    report = run()
    encoded = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    print(encoded)
    return 0 if report["passed"] == report["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
