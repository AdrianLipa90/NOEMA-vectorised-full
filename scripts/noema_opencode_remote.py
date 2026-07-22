#!/usr/bin/env python3
"""NOEMA hardcoded remote-control writer for OpenCode via PhaseNav stream."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

NOEMA_ROOT = Path(os.environ.get("NOEMA_ROOT", Path(__file__).resolve().parent.parent))
SURFACE_ROOT = Path("/dev/shm/ciel_noema")
ROOT_COMMANDS = NOEMA_ROOT / "OPENCODE_REMOTE_COMMANDS.jsonl"
SURFACE_COMMANDS = SURFACE_ROOT / "opencode_remote_commands.jsonl"


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_command(action: str, reason: str, **extra) -> dict:
    base = {
        "schema": "noema/opencode-remote-command/v1",
        "control_transport": "phasenav",
        "action": action,
        "reason": reason,
        "timestamp": _utc(),
        "unix_ts": time.time(),
        **extra,
    }
    payload = json.dumps(base, ensure_ascii=False, sort_keys=True)
    base["command_id"] = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]
    return base


def append_command(command: dict) -> None:
    SURFACE_ROOT.mkdir(parents=True, exist_ok=True)
    line = json.dumps(command, ensure_ascii=False)
    for path in (ROOT_COMMANDS, SURFACE_COMMANDS):
        with path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["allow", "resume", "unlock", "block", "pause", "lock", "require_monitor_ok", "require_orbital_ok", "set"])
    parser.add_argument("--reason", default="")
    parser.add_argument("--enabled", choices=["true", "false"], default=None)
    parser.add_argument("--root-access", choices=["requested", "off"], default=None)
    parser.add_argument("--internet-access", choices=["requested", "off"], default=None)
    args = parser.parse_args()

    extra = {}
    if args.enabled is not None:
        extra["enabled"] = args.enabled == "true"
    requested = {}
    if args.root_access:
        requested["root_access"] = args.root_access == "requested"
    if args.internet_access:
        requested["internet_access"] = args.internet_access == "requested"
    if requested:
        extra["requested_capabilities"] = requested

    command = build_command(args.action, args.reason or args.action, **extra)
    append_command(command)
    print(json.dumps(command, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
