#!/usr/bin/env python3
"""One-off native stop for a single, explicitly-named process — run only
through noema_run_script (NOEMA-native execution), never raw bash.

Usage: noema_stop_pid.py <pid> <expected_name_substring>

Refuses to act unless the live process at <pid> still matches
<expected_name_substring>, so a stale/reused PID can't silently kill the
wrong process.
"""
from __future__ import annotations
import os
import signal
import sys
import time


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: noema_stop_pid.py <pid> <expected_name_substring>")
        return 2
    pid = int(sys.argv[1])
    expected = sys.argv[2]

    try:
        with open(f"/proc/{pid}/cmdline", "rb") as f:
            cmdline = f.read().decode(errors="replace")
    except FileNotFoundError:
        print(f"pid {pid} not found (already gone)")
        return 0

    if expected not in cmdline:
        print(f"REFUSED: pid {pid} cmdline {cmdline!r} does not contain {expected!r}")
        return 1

    try:
        os.kill(pid, signal.SIGTERM)
    except PermissionError:
        print(f"PermissionError sending SIGTERM to pid {pid} (needs root)")
        return 1
    except ProcessLookupError:
        print(f"pid {pid} already gone")
        return 0

    for _ in range(20):
        if not os.path.exists(f"/proc/{pid}"):
            print(f"pid {pid} stopped")
            return 0
        time.sleep(0.1)
    print(f"pid {pid} still alive after SIGTERM+2s")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
