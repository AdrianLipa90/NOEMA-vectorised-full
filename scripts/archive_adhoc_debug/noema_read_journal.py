#!/usr/bin/env python3
"""Native systemd journal reader — uses the systemd.journal Python binding
(libsystemd bindings), not the `journalctl` CLI. Run only through
noema_run_script, never raw bash.

Usage: noema_read_journal.py <unit> [n_lines]
"""
from __future__ import annotations
import sys


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: noema_read_journal.py <unit> [n_lines]")
        return 2
    unit = sys.argv[1]
    n_lines = int(sys.argv[2]) if len(sys.argv) > 2 else 40

    try:
        from systemd import journal
    except ImportError as e:
        print(f"systemd.journal not importable: {e}")
        return 1

    j = journal.Reader()
    j.add_match(_SYSTEMD_USER_UNIT=unit)
    j.seek_tail()
    entries = []
    for _ in range(n_lines):
        entry = j.get_previous()
        if not entry:
            break
        entries.append(entry)
    entries.reverse()
    for e in entries:
        ts = e.get("__REALTIME_TIMESTAMP")
        msg = e.get("MESSAGE", "")
        print(f"{ts} {msg}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
