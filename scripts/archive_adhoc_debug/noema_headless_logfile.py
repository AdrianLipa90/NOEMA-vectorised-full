#!/usr/bin/env python3
"""Znajdź i pokaż log headless."""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path("/home/adrian/noema")
sys.path.insert(0, str(ROOT / "src"))

try:
    from ciel_geometry.paths import P as _P
    log_path = Path(_P.LOGS.HEADLESS_LOG)
    print(f"LOG_PATH: {log_path}")
    print(f"exists: {log_path.exists()}")
    if log_path.exists():
        text = log_path.read_text(errors="replace")
        lines = text.split("\n")
        print(f"Total lines: {len(lines)}")
        # Ostatnie 60 linii
        print("\n=== OSTATNIE 60 LINII ===")
        for l in lines[-60:]:
            print(l)
except Exception as e:
    print(f"ERROR: {e}")
    # Fallback: szukaj pliku logów
    candidates = list(Path("/media/adrian/New Volume/CIEL_memories/logs").glob("*headless*"))
    print(f"Headless log candidates: {candidates}")
    for c in candidates[:2]:
        print(f"\n--- {c} ---")
        t = c.read_text(errors="replace")
        print(t[-2000:])
