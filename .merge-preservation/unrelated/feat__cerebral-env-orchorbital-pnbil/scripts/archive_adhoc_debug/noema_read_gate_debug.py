#!/usr/bin/env python3
from pathlib import Path
import json

debug_p = Path("/media/adrian/New Volume/CIEL_memories/state/headless_gate_debug.json")
print(f"Exists: {debug_p.exists()}")
if debug_p.exists():
    print(debug_p.read_text())

# Sprawdź też headless log tail (pełny)
log_p = Path("/media/adrian/New Volume/CIEL_memories/logs/ciel_headless.jsonl")
if log_p.exists():
    lines = log_p.read_text(errors="replace").splitlines()
    print(f"\n=== LOG tail (last 30) — {len(lines)} total ===")
    for l in lines[-30:]:
        print(l)
