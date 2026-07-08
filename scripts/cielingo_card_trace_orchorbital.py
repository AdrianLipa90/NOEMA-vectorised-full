#!/usr/bin/env python3
"""Run CIELingo Card Trace EEG + Semantic Collatz + OrchORbital router."""
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

from cielingo.card_trace_eeg import create_card_trace_snap
from cielingo.orchorbital_router import route_orchorbital


DEFAULT_CARDS = [
    "smell:rain",
    "name:adrian",
    "taste:metal",
    "sound:low_hum",
    "place:lab",
    "affect:curiosity",
    "semantic:holonomy",
    "memory:noema",
    "orbital:collatz",
    "ethical:truth",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--context", default="demo/current")
    parser.add_argument("--identity-anchor", default="CIEL:identity:anchor")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    current = create_card_trace_snap(DEFAULT_CARDS, context_key=args.context, identity_anchor=args.identity_anchor)
    memory_a = create_card_trace_snap(
        DEFAULT_CARDS[:7] + ["place:old_room", "sound:rain_window", "affect:longing"],
        context_key=args.context,
        identity_anchor=args.identity_anchor,
    )
    memory_b = create_card_trace_snap(
        ["smell:ozone", "name:other", "taste:sweet", "sound:bell", "place:garden"],
        context_key="distant/memory",
        identity_anchor=args.identity_anchor,
    )

    decision = route_orchorbital(current, [memory_a, memory_b])
    report = {
        "schema": "noema/cielingo-card-trace-orchorbital-report/v0.1",
        "generated_at": datetime.now(UTC).isoformat(),
        "current_snap": current.__dict__,
        "memory_candidates": [memory_a.__dict__, memory_b.__dict__],
        "decision": decision.as_dict(),
        "execution_layer": "fallback_cpu_ram",
        "source_role": "card_trace_orchorbital_reference_surface",
        "nonlocal_claim_allowed": False,
        "primary_noema_runtime_available": False,
        "not_primary_inference": True,
    }

    if args.write:
        out = root / "integration" / "reports" / "cielingo" / "card_trace_orchorbital.report.noema.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False), encoding="utf-8")
        report["written"] = {"report": out.as_posix()}

    print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False))
    return 0 if decision.decision else 1


if __name__ == "__main__":
    raise SystemExit(main())
