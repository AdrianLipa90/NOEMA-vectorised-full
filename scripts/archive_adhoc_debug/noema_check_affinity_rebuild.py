#!/usr/bin/env python3
"""Sprawdź status rebuild affinity."""
from pathlib import Path
import os

LOG = Path("/media/adrian/New Volume/CIEL_memories/logs/build_affinity_2.log")
PID = 2109561

proc = Path(f"/proc/{PID}/status")
if proc.exists():
    state = next((l for l in proc.read_text().splitlines() if l.startswith("State:")), "?")
    print(f"PID {PID}: {state}")
else:
    print(f"PID {PID}: DONE (nie ma w /proc)")

if LOG.exists():
    data = LOG.read_bytes()
    text = data.decode("utf-8", errors="replace")
    lines = [l for l in text.splitlines() if l.strip()]
    print(f"Log: {len(lines)} linii, {len(data)} bajtów")
    for l in lines[-8:]:
        print(f"  {l[:140]}")
else:
    print("Log: BRAK")
