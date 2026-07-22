#!/usr/bin/env python3
"""Run one real+imaginal NOEMA step from Adrian's input."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
SCRIPTS = ROOT / "scripts"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ciel_geometry import dual_surface_step  # type: ignore[attr-defined]
from ciel_coupling import append_ciel_memory_update, process_user_input
from ciel_sot_agent.htri_scheduler import get_state_status as get_htri_state


def main() -> int:
    parser = argparse.ArgumentParser(description="Run real+imaginal NOEMA step")
    parser.add_argument("text")
    args = parser.parse_args()

    state = process_user_input(args.text)
    payload = dual_surface_step(state, args.text)
    htri_state = get_htri_state()
    payload["htri_state"] = htri_state
    payload["htri_status"] = htri_state.get("status")
    payload["htri_publication"] = htri_state.get("publication")
    payload["ciel_state"] = {
        "dominant_emotion": state.get("dominant_emotion"),
        "operating_mode": state.get("operating_mode"),
        "noema_tick": state.get("noema_tick"),
        "phase_memory_slot": state.get("phase_memory_slot"),
    }
    payload["dual_memory_update_path"] = append_ciel_memory_update(
        state,
        args.text,
        schema="CIEL_DUAL_SURFACE_UPDATE_V0_1",
        extra_payload={
            "dual_surface": payload,
            "htri_state": payload["htri_state"],
        },
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
