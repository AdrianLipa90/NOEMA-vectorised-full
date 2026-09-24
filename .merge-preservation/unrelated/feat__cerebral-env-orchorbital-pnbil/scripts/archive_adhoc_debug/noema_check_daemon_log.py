#!/usr/bin/env python3
"""Sprawdz logi headless daemon."""
import sys, pathlib
sys.path.insert(0, "/home/adrian/noema/src")
from ciel_geometry.paths import P as _P

log_path = pathlib.Path(_P.LOGS.HEADLESS_LOG)
print(f"Log path: {log_path}")
print(f"Log exists: {log_path.exists()}")
if log_path.exists():
    lines = log_path.read_text(errors="replace").splitlines()
    # Ostatnie 30 linii
    print(f"\n--- Ostatnie 30 linii: ---")
    for l in lines[-30:]:
        print(l)
