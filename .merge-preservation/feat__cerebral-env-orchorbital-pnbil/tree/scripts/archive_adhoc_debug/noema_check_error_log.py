#!/usr/bin/env python3
"""Szukaj błędów w logu headless."""
from pathlib import Path

log = Path("/media/adrian/New Volume/CIEL_memories/logs/ciel_headless.jsonl")
lines = log.read_text(errors="replace").splitlines()
errors = [l for l in lines if "ERROR" in l or "Traceback" in l or "exception" in l.lower() or "index out of range" in l]
print(f"Linie z bledami ({len(errors)}):")
for l in errors[-20:]:
    print(l)
