#!/usr/bin/env python3
"""Policz linie i pokaz ostatnie 20 linii logu headless."""
from pathlib import Path
log = Path("/media/adrian/New Volume/CIEL_memories/logs/ciel_headless.jsonl")
lines = log.read_text(errors="replace").splitlines()
print(f"Linia count: {len(lines)}")
print("Ostatnie 20 linii:")
for l in lines[-20:]:
    print(l)
