#!/usr/bin/env python3
"""Persistent supervisor for the CIEL subconscious backend.

The current canonical topology is the inline CIELingo/PhaseNav backend exposed
by ``scripts/ciel_subconscious.py``.  Earlier revisions imported a removed
``start_server`` function and described an external llama-server fallback;
that made the supervisor unimportable even though its active inline path was
healthy.  The supervisor now monitors only the implemented backend and reports
an explicit offline state when it is unavailable.
"""

from __future__ import annotations

import argparse
import logging
import signal
import subprocess
import sys
import time
from pathlib import Path

log = logging.getLogger(__name__)
PROJECT = Path(__file__).resolve().parent.parent
SRC = str(PROJECT / "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from ciel_sot_agent.subconsciousness import is_running

_INLINE_SCRIPT = PROJECT / "scripts" / "ciel_subconscious.py"


def _inline_backend_ok() -> bool:
    """Return True when the inline subconscious backend responds to ``--status``."""
    if not _INLINE_SCRIPT.exists():
        return False
    try:
        result = subprocess.run(
            [sys.executable, str(_INLINE_SCRIPT), "--status"],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        return result.returncode == 0 and "inline: OK" in (result.stdout or "")
    except (OSError, subprocess.SubprocessError) as exc:
        log.warning("Inline subconscious status check failed: %s", exc)
        return False


def get_status() -> dict[str, object]:
    """Report the effective subconscious backend state without inventing a server."""
    inline_ok = _inline_backend_ok()
    memory_backend_ok = is_running()
    if inline_ok:
        mode = "inline"
        running = True
    elif memory_backend_ok:
        mode = "memory"
        running = True
    else:
        mode = "offline"
        running = False
    return {
        "running": running,
        "mode": mode,
        "inline_ok": inline_ok,
        "server_running": memory_backend_ok,
        "server_url": None,
    }


def run_supervisor(interval: float = 15.0) -> int:
    """Monitor the implemented inline/memory backend until stopped."""
    stopping = False

    def _stop(_signum, _frame) -> None:
        nonlocal stopping
        stopping = True

    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)

    while not stopping:
        status = get_status()
        if not status["running"]:
            print(
                "[sub-supervisor] inline subconscious backend unavailable; retrying",
                file=sys.stderr,
            )
        time.sleep(interval)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--daemon", action="store_true", help="Run supervisor loop")
    parser.add_argument("--status", action="store_true", help="Print running status and exit")
    parser.add_argument(
        "--json-status",
        action="store_true",
        help="Print detailed JSON backend status and exit",
    )
    parser.add_argument("--interval", type=float, default=15.0, help="Poll interval in seconds")
    args = parser.parse_args()

    if args.json_status:
        import json

        print(json.dumps(get_status(), ensure_ascii=False))
        return 0
    if args.status:
        print("running" if get_status()["running"] else "stopped")
        return 0
    return run_supervisor(interval=args.interval)


if __name__ == "__main__":
    raise SystemExit(main())
