#!/usr/bin/env python3
"""Znajdź plik/katalog PhaseMemory."""
import time
from pathlib import Path

# Typowe lokalizacje PhaseMemory
candidates = [
    Path("/media/adrian/New Volume/CIEL_memories/state/"),
    Path("/media/adrian/New Volume/CIEL_memories/"),
    Path("/home/adrian/noema/data/"),
    Path("/home/adrian/noema/src/ciel_sot_agent/"),
    Path("/dev/shm/ciel_noema/"),
]

pm_names = ["phase_memory", "cielingo_phase_memory", "phase_memory.pkl",
            "phase_memory.json", "phase_memory.jsonl", "pm_store", "pm.pkl"]

print("=== Szukam PhaseMemory ===")
for base in candidates:
    if not base.exists():
        continue
    for f in base.iterdir():
        name = f.name.lower()
        if any(n in name for n in pm_names) or "phase" in name and "mem" in name:
            mt = f.stat().st_mtime
            size = f.stat().st_size if f.is_file() else sum(ff.stat().st_size for ff in f.rglob("*") if ff.is_file())
            print(f"  ZNALEZIONO: {f} ({size//1024}KB, mtime={time.ctime(mt)})")

# Szukaj też w src
src_path = Path("/home/adrian/noema/src")
if src_path.exists():
    for f in src_path.rglob("*phase*mem*"):
        print(f"  src: {f}")
