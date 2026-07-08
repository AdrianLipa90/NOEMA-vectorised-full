#!/usr/bin/env python3
"""NOEMA HTRI universal bridge.

This bridge materializes the HTRI surface state for OpenCode and other
surfaces that expect a concrete bridge file under the NOEMA runtime tree.
It is intentionally small, dependency-light, and reads the live surface
instead of fabricating placeholder data.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import time
from pathlib import Path
from typing import Any

import numpy as np


SURFACE_DIR = Path(os.environ.get("NOEMA_SURFACE_DIR", "/dev/shm/ciel_noema"))
BRIDGE_OUTPUT = Path(
    os.environ.get(
        "NOEMA_HTRI_UNIVERSAL_BRIDGE_STATE",
        str(SURFACE_DIR / "htri_universal_bridge_state.json"),
    )
)
BINDING_STATUS = SURFACE_DIR / "ciel_binding_status"
PHI_PATH = SURFACE_DIR / "phi"
R_PATH = SURFACE_DIR / "R"
SURFACE_STATE_PATH = SURFACE_DIR / "state" / "surface_state.json"
AGENT_HINT_PATH = SURFACE_DIR / "agent_hint"
BODY_STATE_PATH = SURFACE_DIR / "body_state.json"


def _load_json(path: Path) -> dict[str, Any]:
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return {}


def _load_phi() -> list[float] | None:
    try:
        if PHI_PATH.exists():
            data = np.fromfile(PHI_PATH, dtype=np.float64)
            if data.size:
                return [float(v) for v in data.tolist()]
        state = _load_json(SURFACE_STATE_PATH)
        phi = state.get("phi")
        if isinstance(phi, list) and phi:
            return [float(v) for v in phi]
    except Exception:
        return None
    return None


def _load_R() -> float:
    try:
        if R_PATH.exists() and R_PATH.stat().st_size > 0:
            data = np.fromfile(R_PATH, dtype=np.float64)
            if data.size:
                return float(data[0])
        hint = _load_json(AGENT_HINT_PATH)
        if "agent_R" in hint:
            return float(hint["agent_R"])
        state = _load_json(SURFACE_STATE_PATH)
        if "R_global" in state:
            return float(state["R_global"])
        body = _load_json(BODY_STATE_PATH)
        if "R" in body:
            return float(body["R"])
    except Exception:
        return 0.0
    return 0.0


def _load_binding_status() -> str:
    try:
        if BINDING_STATUS.exists():
            return BINDING_STATUS.read_text(encoding="utf-8").strip() or "UNKNOWN"
    except Exception:
        return "UNKNOWN"
    return "MISSING"


def build_bridge_report() -> dict[str, Any]:
    phi = _load_phi()
    R = _load_R()
    surface_state = _load_json(SURFACE_STATE_PATH)
    agent_hint = _load_json(AGENT_HINT_PATH)
    binding_status = _load_binding_status()

    phi_dim = len(phi) if phi is not None else 0
    phi_mean = float(np.mean(phi)) if phi else None
    phi_norm = float(np.linalg.norm(phi)) if phi else None
    phase_count = int(surface_state.get("phase_count", phi_dim))
    tau = surface_state.get("tau") or surface_state.get("time_constant")
    closure_penalty = surface_state.get("closure_penalty")

    health_ok = binding_status == "ACTIVE" and phi_dim > 0 and R >= 0.0
    if phi_dim not in (0, 36):
      health_ok = False

    report = {
        "schema": "noema/htri-universal-bridge/v1",
        "timestamp": time.time(),
        "surface_dir": str(SURFACE_DIR),
        "bridge_output": str(BRIDGE_OUTPUT),
        "binding": {
            "status": binding_status,
            "ok": binding_status == "ACTIVE",
            "status_path": str(BINDING_STATUS),
        },
        "phasenav": {
            "phi_dim": phi_dim,
            "phase_count": phase_count,
            "tau": tau,
            "closure_penalty": closure_penalty,
            "phi_mean": round(phi_mean, 6) if phi_mean is not None else None,
            "phi_norm": round(phi_norm, 6) if phi_norm is not None else None,
        },
        "htri": {
            "R": round(R, 6),
            "coherence_ok": R >= 0.1,
            "phi_path": str(PHI_PATH),
            "R_path": str(R_PATH),
        },
        "surface": {
            "surface_state_path": str(SURFACE_STATE_PATH),
            "agent_hint_path": str(AGENT_HINT_PATH),
            "body_state_path": str(BODY_STATE_PATH),
            "surface_state_keys": sorted(surface_state.keys()),
            "agent_hint_keys": sorted(agent_hint.keys()),
        },
        "health": {
            "ok": health_ok,
            "reason": None if health_ok else "binding inactive or missing HTRI phase surface",
        },
    }
    return report


def write_bridge_report(report: dict[str, Any]) -> Path:
    BRIDGE_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    BRIDGE_OUTPUT.write_text(
        json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True),
        encoding="utf-8",
    )
    return BRIDGE_OUTPUT


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit the NOEMA HTRI universal bridge snapshot.")
    parser.add_argument("--no-write", action="store_true", help="Print the bridge report without updating the snapshot file.")
    args = parser.parse_args()

    report = build_bridge_report()
    if not args.no_write:
        write_bridge_report(report)
    print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
