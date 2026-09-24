#!/usr/bin/env python3
"""Run NOEMA-surface HTRI Kuramoto 120 and gate pipeline publication."""
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

from noema_holonomic_doctor.manifest import manifest_digest, noema_ls
from noema_nonlocal_db import card_registry_digest, load_cards, validate_cards
from noema_htri import (
    KuramotoHTRIConfig,
    build_pipeline_metrics,
    pipeline_connection_score,
    run_kuramoto_htri_120,
    validate_htri_report,
)
from noema_htri.pipeline_publish import write_json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--steps", type=int, default=512)
    parser.add_argument("--oscillators", type=int, default=120)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--pipeline-runtime-confirmed", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    cards = load_cards(root)
    card_validation = validate_cards(cards)
    manifest = noema_ls(root)
    m_digest = manifest_digest(manifest)
    c_digest = card_registry_digest(cards)

    report = run_kuramoto_htri_120(
        manifest_digest=m_digest,
        card_registry_digest=c_digest,
        config=KuramotoHTRIConfig(n_oscillators=args.oscillators, steps=args.steps),
    )
    report["generated_at"] = datetime.now(UTC).isoformat()
    report["card_validation"] = card_validation

    report_path = root / "integration" / "reports" / "noema_htri" / "htri_kuramoto_120.raw.noema.json"
    legacy_report_path = root / "integration" / "reports" / "noema_htri" / "htri_kuramoto_120.noema.json"
    latest_report_path = root / "integration" / "reports" / "noema_htri" / "htri_kuramoto_120.latest.noema.json"
    validation_path = root / "integration" / "reports" / "noema_htri" / "htri_kuramoto_120.validation.noema.json"
    metrics_path = root / "integration" / "reports" / "noema_pipeline_metrics.json"
    quarantine_path = root / "integration" / "reports" / "noema_htri" / "htri_kuramoto_120.quarantine.noema.json"

    pipeline_reader_exists = (root / "src" / "ciel_sot_agent" / "ciel_pipeline.py").exists()
    score = pipeline_connection_score(
        report_written=args.write,
        metrics_file_written=False,
        pipeline_reader_exists=pipeline_reader_exists,
        pipeline_runtime_confirmed=args.pipeline_runtime_confirmed,
    )
    validation = validate_htri_report(report, pipeline_connected_score=score)
    report["validation_gate"] = validation

    if args.write:
        write_json(report_path, report)
        # Compatibility aliases: old consumers used htri_kuramoto_120.noema.json.
        # Keep them current so stale pre-validation reports cannot shadow v0.2 output.
        write_json(legacy_report_path, report)
        write_json(latest_report_path, report)
        # Recompute connection score with raw report evidence included.  Metrics file
        # only counts if validation passes and is actually written below.
        score = pipeline_connection_score(
            report_written=True,
            metrics_file_written=False,
            pipeline_reader_exists=pipeline_reader_exists,
            pipeline_runtime_confirmed=args.pipeline_runtime_confirmed,
        )
        validation = validate_htri_report(report, pipeline_connected_score=score)
        report["validation_gate"] = validation
        write_json(validation_path, validation)

        if validation["publish_to_pipeline"]:
            pipeline_metrics = build_pipeline_metrics(report, validation)
            write_json(metrics_path, pipeline_metrics)
            report["pipeline_metrics"] = pipeline_metrics
            report["written"] = {
                "raw_report": report_path.as_posix(),
                "validation": validation_path.as_posix(),
                "pipeline_metrics": metrics_path.as_posix(),
            }
        else:
            quarantine = {
                "schema": "noema/htri-quarantine/v0.2",
                "raw_report": report_path.as_posix(),
                "validation": validation,
                "may_publish_to_pipeline": False,
                "reason": validation["reasons"],
            }
            write_json(quarantine_path, quarantine)
            report["written"] = {
                "raw_report": report_path.as_posix(),
                "validation": validation_path.as_posix(),
                "quarantine": quarantine_path.as_posix(),
            }

    print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False))
    if not card_validation["valid"]:
        return 2
    return 0 if validation["publish_to_pipeline"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
