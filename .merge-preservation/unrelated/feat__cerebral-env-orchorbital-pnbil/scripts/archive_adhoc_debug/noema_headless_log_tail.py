#!/usr/bin/env python3
"""Ostatnie 20 linii logu headless."""
from pathlib import Path

log = Path("/media/adrian/New Volume/CIEL_memories/state/ciel_headless.log")
if not log.exists():
    # try alternate
    import subprocess
    r = subprocess.run(
        ["journalctl", "--user", "-u", "noema-headless.service", "-n", "20", "--no-pager"],
        capture_output=True, text=True
    )
    print(r.stdout[-3000:])
else:
    lines = log.read_text(errors="replace").splitlines()
    print("\n".join(lines[-20:]))
