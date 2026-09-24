#!/usr/bin/env python3
"""Znajdz logi exception bridge — pełne tracebacki."""
from pathlib import Path
import re

# Szukaj plikow z exception logami
candidates = [
    Path("/media/adrian/New Volume/CIEL_memories/logs"),
    Path("/home/adrian/noema/logs"),
    Path("/dev/shm/ciel_noema"),
]

for d in candidates:
    if d.exists():
        files = list(d.rglob("*.jsonl")) + list(d.rglob("*.log"))
        print(f"\n{d}: {len(files)} plikow")
        for f in files[:10]:
            print(f"  {f.name} ({f.stat().st_size} bytes)")

# Szukaj w headless jsonl linii z IndexError
log = Path("/media/adrian/New Volume/CIEL_memories/logs/ciel_headless.jsonl")
lines = log.read_text(errors="replace").splitlines()
idx_errors = [l for l in lines if "IndexError" in l or "index out of range" in l]
print(f"\nIndexError lines in headless log: {len(idx_errors)}")
for l in idx_errors[-10:]:
    print(l)
