#!/usr/bin/env python3
"""Generate bootstrap cards for the NOEMA nonlocal database layer."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from noema_nonlocal_db import card_registry_digest, load_cards, validate_cards

CARD_SPECS = [
    ("000_ROOT", "NOEMA root card", "Root of the NOEMA nonlocal DB bootstrap layer", []),
    ("001_DOCTOR", "NOEMA Doctor", "Diagnostic wrapper and pain-surface emitter", ["000_ROOT"]),
    ("002_PIPELINE_SURFACE", "Pipeline surface", "Pipeline connectivity and metric emission surface", ["000_ROOT", "001_DOCTOR"]),
    ("003_HTRI_KURAMOTO_120", "HTRI Kuramoto 120", "120 oscillator HTRI diagnostic simulator", ["000_ROOT", "002_PIPELINE_SURFACE"]),
    ("004_J_FUNCTIONAL", "J-functional", "Holonomic diagnostic cost and bounded R_H semantics", ["000_ROOT", "002_PIPELINE_SURFACE"]),
    ("005_PAIN_SURFACE", "Pain surface", "Structured fault/pain emission layer", ["001_DOCTOR"]),
    ("006_SEMANTIC_BRIDGE", "Semantic bridge", "Bridge between card meanings, reports and operator packets", ["000_ROOT", "005_PAIN_SURFACE"]),
    ("007_NONLOCAL_PROXY", "Nonlocal proxy", "NOEMA-surface proxy semantics for file-packet coupling", ["000_ROOT", "006_SEMANTIC_BRIDGE"]),
    ("008_EULER_BERRY_CLOSURE", "Euler-Berry closure", "Cyclic phase closure invariant for diagnostics", ["003_HTRI_KURAMOTO_120", "004_J_FUNCTIONAL"]),
    ("009_NOEMA_PRIORITY_FIELD", "NOEMA priority field", "Priority/meaning field for Doctor and pipeline interpretation", ["001_DOCTOR", "006_SEMANTIC_BRIDGE", "008_EULER_BERRY_CLOSURE"]),
]


def build_card(idx: str, title: str, meaning: str, deps: list[str]) -> dict:
    card_id = f"noema:nonlocal_db:{idx}"
    dep_ids = [f"noema:nonlocal_db:{d}" for d in deps]
    return {
        "schema": "noema/nonlocal-db-card/v0.1",
        "card_id": card_id,
        "title": title,
        "layer": "noema_nonlocal_db_bootstrap",
        "meaning": meaning,
        "depends_on": dep_ids,
        "runtime_semantics": {
            "nonlocality": "NOEMA-surface/proxy/file-packet coupling unless externally verified",
            "source_of_truth": "append-only NOEMA card/report layer",
            "pipeline_role": "diagnostic meaning/prioritization input",
        },
        "epistemic_boundary": {
            "direct_external_sensor_verified": False,
            "user007_sot_write_claimed": False,
            "sandbox_candidate": True,
        },
        "status": "bootstrap_candidate",
        "priority": "high" if idx in {"000_ROOT", "001_DOCTOR", "002_PIPELINE_SURFACE"} else "normal",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    cards_dir = root / "cards" / "noema_nonlocal_db"
    cards_dir.mkdir(parents=True, exist_ok=True)
    for idx, title, meaning, deps in CARD_SPECS:
        path = cards_dir / f"{idx}.noema.card.json"
        path.write_text(json.dumps(build_card(idx, title, meaning, deps), indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    cards = load_cards(root)
    validation = validate_cards(cards)
    report = {
        "schema": "noema/nonlocal-db-bootstrap-report/v0.1",
        "generated_at": datetime.now(UTC).isoformat(),
        "cards_dir": "cards/noema_nonlocal_db",
        "card_count": len(cards),
        "registry_digest": card_registry_digest(cards),
        "validation": validation,
    }
    out = root / "cards" / "noema_nonlocal_db" / "BOOTSTRAP_REPORT.noema.json"
    out.write_text(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False))
    return 0 if validation["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
