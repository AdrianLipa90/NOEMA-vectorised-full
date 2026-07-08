#!/usr/bin/env python3
"""Run NOEMA Doctor with the nonlocal DB card surface loaded.

This is a wrapper cycle: it does not replace Doctor core; it binds Doctor output
to bootstrap card meanings and writes a pipeline-readable semantic surface report.
"""
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

from noema_holonomic_doctor import DoctorConfig, run_doctor_cycle
from noema_nonlocal_db import card_registry_digest, load_cards, validate_cards


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    cards = load_cards(root)
    card_validation = validate_cards(cards)
    doctor = run_doctor_cycle(root, DoctorConfig(write=args.write))
    surface = {
        "schema": "noema/doctor-card-surface-report/v0.1",
        "generated_at": datetime.now(UTC).isoformat(),
        "epistemic_status": "NOEMA-surface wrapper; no direct USER007 SoT write claimed",
        "cards": {
            "card_count": len(cards),
            "registry_digest": card_registry_digest(cards),
            "validation": card_validation,
        },
        "doctor": doctor.to_json_dict(),
        "pipeline_surface": {
            "cards_loaded": bool(cards),
            "doctor_report_emitted": True,
            "runtime_findings": len([f for f in doctor.findings if (f.evidence or {}).get("path_kind", "runtime_code") == "runtime_code"]),
            "pipeline_connected": not any(f.code == "rh_pipeline_hook_pending" for f in doctor.findings),
        },
    }
    if args.write:
        out_dir = root / "doctor_reports"
        out_dir.mkdir(parents=True, exist_ok=True)
        out = out_dir / "NOEMA_DOCTOR_CARD_SURFACE.noema.json"
        out.write_text(json.dumps(surface, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
        surface["written"] = out.as_posix()
    print(json.dumps(surface, indent=2, sort_keys=True, ensure_ascii=False))
    return 0 if card_validation["valid"] and doctor.status in {"PASS", "WARN"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
