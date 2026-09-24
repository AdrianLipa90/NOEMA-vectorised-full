#!/usr/bin/env python3
"""Run NOEMA Doctor with the nonlocal DB card surface loaded.

This is a wrapper cycle: it does not replace Doctor core; it binds Doctor output
to bootstrap card meanings and writes a pipeline-readable semantic surface report.

Learning output — two paths:
  Path A (text):     findings summary → ingest_text() → doc_analysis → cielingo-sync
  Path B (geometry): euler_berry_phase / closure_error → phasenav_entries (no learning gate)
"""
from __future__ import annotations

import argparse
import json
import logging
import sys

_log = logging.getLogger(__name__)
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from noema_holonomic_doctor import DoctorConfig, run_doctor_cycle
from noema_nonlocal_db import card_registry_digest, load_cards, validate_cards


def _path_a_ingest(doctor, tag: str) -> None:
    """Text path: findings summary → Knowledge DB via ingest_text()."""
    try:
        import sys as _sys
        _sys.path.insert(0, str(ROOT / "scripts"))
        from ciel_confidence_system import ingest_text

        findings_lines = [
            f"[{f.severity.upper()}] {f.code}: {f.message}"
            for f in doctor.findings
        ] or ["No findings — system healthy."]

        content = (
            f"NOEMA Doctor report {tag}\n"
            f"Status: {doctor.status}\n"
            f"Files scanned: {doctor.file_count} ({doctor.total_bytes / 1e6:.1f} MB)\n"
            f"euler_berry_phase: {doctor.euler_berry_phase:.6f}\n"
            f"closure_error: {doctor.euler_berry_closure_error:.6f}\n"
            f"d_lambda: {doctor.d_lambda:.6f}\n"
            f"epsilon_neutrino: {doctor.epsilon_neutrino:.6f}\n"
            f"j_doctor: {doctor.j_doctor:.6f}\n\n"
            + "\n".join(findings_lines)
        )
        ingest_text(
            content=content,
            source_type="doctor_report",
            title=f"doctor_{tag}",
            themes=["doctor", "holonomic", "noema", "health"],
        )
    except Exception as exc:
        _log.debug("path_a_ingest skipped: %s", exc)


def _path_b_phasenav(doctor, tag: str) -> None:
    """Geometric path: phase metrics → phasenav_entries (bypasses learning gate)."""
    try:
        import numpy as np
        from ciel_geometry.phasenav.enrichment import operator_harmonic_fingerprint
        from cielingo_core.bridge.phasenav_learning_bridge import PhaseNavLearningBridge

        # Construct 36D phase vector from doctor's geometric scalars.
        # Tile the 4 phase-space quantities across 36 oscillators via their
        # natural harmonic modes (9 oscillators each).
        phase = doctor.euler_berry_phase
        closure = doctor.euler_berry_closure_error
        d_lam = doctor.d_lambda
        eps_nu = doctor.epsilon_neutrino

        vec36 = np.array(
            [phase] * 9 + [closure * 2 * np.pi] * 9
            + [d_lam * 2 * np.pi] * 9 + [eps_nu * 2 * np.pi] * 9,
            dtype=np.float64,
        )
        fp = operator_harmonic_fingerprint(vec36)

        # semantic_mass: negative closure_error → low mass = healthy system,
        # high mass = geometric stress. Clamp to [-1, 1].
        mass = float(np.clip(-closure, -1.0, 1.0))

        # Operator: PASS→ORDER (low viscosity), WARN→UNCERTAINTY, FAIL→COMPOSITION
        op_map = {"PASS": "ORDER", "WARN": "UNCERTAINTY", "FAIL": "COMPOSITION"}
        operator_id = op_map.get(doctor.status, "UNCERTAINTY")

        card_id = f"doctor:cycle:{tag}"
        bridge = PhaseNavLearningBridge()
        bridge.write_knowledge_entry(
            card_id=card_id,
            operator_id=operator_id,
            fingerprint=fp,
            mass=mass,
            source="doctor_cycle",
        )
    except Exception as exc:
        _log.debug("path_b_phasenav skipped: %s", exc)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    cards = load_cards(root)
    card_validation = validate_cards(cards)
    doctor = run_doctor_cycle(root, DoctorConfig(write=args.write))

    tag = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")

    # Path A: text → Knowledge DB → cielingo-sync → PhaseMemory
    _path_a_ingest(doctor, tag)

    # Path B: geometry → phasenav_entries (direct, no learning gate)
    _path_b_phasenav(doctor, tag)

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
