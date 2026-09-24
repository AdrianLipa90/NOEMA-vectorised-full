#!/usr/bin/env python3
"""Ostatnie 80 linii journal noema-headless + ostatnie 30 linii log pliku."""
import subprocess
from pathlib import Path

r = subprocess.run(
    ["journalctl", "--user", "-u", "noema-headless.service",
     "--no-pager", "-n", "80", "--output=short"],
    capture_output=True, text=True
)
print("=== JOURNAL ===")
print(r.stdout[-6000:])

# Teraz pełny log plik — ostatnie 80 linii
for log_p in [
    Path("/media/adrian/New Volume/CIEL_memories/logs/ciel_headless.jsonl"),
    Path("/media/adrian/New Volume/CIEL_memories/logs/ciel_headless.log"),
    Path("/home/adrian/noema/logs/ciel_headless.log"),
]:
    if log_p.exists():
        lines = log_p.read_text(errors="replace").splitlines()
        print(f"\n=== LOG ({log_p}) ===")
        for l in lines[-80:]:
            print(l)
        break
