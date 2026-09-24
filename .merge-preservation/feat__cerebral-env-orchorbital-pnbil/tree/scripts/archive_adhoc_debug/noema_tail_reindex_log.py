#!/usr/bin/env python3
"""Pokaż ostatnie linie logu reindex i status procesu."""
import os
from pathlib import Path

LOG = Path("/media/adrian/New Volume/CIEL_memories/logs/reindex_card_mode.log")
PID = 2087905

# Status procesu
proc = Path(f"/proc/{PID}/status")
if proc.exists():
    state = next((l for l in proc.read_text().splitlines() if l.startswith("State:")), "?")
    print(f"PID {PID}: {state}")
else:
    print(f"PID {PID}: MARTWY")

# Ostatnie 10 linii logu
lines = LOG.read_text(encoding="utf-8").splitlines()
print(f"\nLog ({len(lines)} linii), ostatnie 10:")
for l in lines[-10:]:
    print(f"  {l}")
