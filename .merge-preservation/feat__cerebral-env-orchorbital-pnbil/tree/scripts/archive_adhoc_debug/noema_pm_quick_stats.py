#!/usr/bin/env python3
"""Szybkie statystyki PhaseMemory przez filesystem."""
import time
from pathlib import Path

PM = Path("/media/adrian/New Volume/CIEL_memories/state/cielingo_phase_memory")

if not PM.exists():
    print("PhaseMemory dir: BRAK")
else:
    # Policz pliki bez sortowania (szybkie)
    count = 0
    newest_mtime = 0
    newest_name = ""
    oldest_mtime = float('inf')
    for f in PM.iterdir():
        if f.is_file():
            count += 1
            mt = f.stat().st_mtime
            if mt > newest_mtime:
                newest_mtime = mt
                newest_name = f.name
            if mt < oldest_mtime:
                oldest_mtime = mt

    print(f"PhaseMemory: {count} wpisów")
    print(f"  Najnowszy: {newest_name} [{time.ctime(newest_mtime)}]")
    print(f"  Najstarszy: [{time.ctime(oldest_mtime)}]")

# Sprawdź log daemona
LOG = Path("/media/adrian/New Volume/CIEL_memories/logs/ciel_headless.jsonl")
if LOG.exists():
    lines = LOG.read_text(errors="replace").splitlines()
    recent = [l for l in lines[-30:] if any(k in l for k in
        ["PhaseMemory loaded", "learn", "knowledge", "error", "ERROR", "WARN"])]
    print(f"\nOstatnie logi (filtered):")
    for l in recent[-5:]:
        print(f"  {l[:120]}")
