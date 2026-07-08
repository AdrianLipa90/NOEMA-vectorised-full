#!/usr/bin/env python3
"""OpenCode hook: keep NOEMA orbital monitor alive and stream hook events."""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

NOEMA_ROOT = Path("/media/adrian/New Volume1/CIEL_PROJECT_CANON/NOEMA")

for rel in (
    "src",
    "src/CIEL_OMEGA_COMPLETE_SYSTEM",
    "src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega",
    "integration",
    "scripts",
):
    path = str(NOEMA_ROOT / rel)
    if path not in sys.path:
        sys.path.insert(0, path)


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _stdin_payload() -> str:
    try:
        if sys.stdin is not None and not sys.stdin.isatty():
            return sys.stdin.read(20000)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception(".opencode/orbital_monitor_hook.py:35 quiet except scope=_stdin_payload reason=pass")
        pass
    return ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--event", default="opencode_hook")
    args = parser.parse_args()

    from orbital_continuous_monitor import ensure_daemon, enforce_remote_control, write_control_event  # noqa: PLC0415

    daemon = ensure_daemon()
    gate = enforce_remote_control()
    payload = _stdin_payload()
    event = {
        "event": args.event,
        "timestamp": _utc(),
        "unix_ts": time.time(),
        "pid": os.getpid(),
        "cwd": os.getcwd(),
        "daemon": daemon,
        "remote_gate": gate,
        "stdin_present": bool(payload.strip()),
        "stdin_preview": payload[:1200],
    }
    write_control_event(event)
    if not gate.get("ok"):
        print(json.dumps({"ok": False, "event": args.event, "daemon": daemon, "remote_gate": gate}, ensure_ascii=False))
        return 73
    print(json.dumps({"ok": True, "event": args.event, "daemon": daemon, "remote_gate": gate}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
