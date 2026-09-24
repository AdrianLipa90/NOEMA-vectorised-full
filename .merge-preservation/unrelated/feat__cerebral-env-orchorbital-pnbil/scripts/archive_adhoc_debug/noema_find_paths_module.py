#!/usr/bin/env python3
"""Znajdź moduł ciel_geometry.paths z perspektywy headless daemon."""
import sys
from pathlib import Path

# Ustaw sys.path tak jak robi to headless daemon
ROOT = Path("/home/adrian/noema")
for p in [str(ROOT / "src"), str(ROOT / "integration"), str(ROOT)]:
    if p not in sys.path:
        sys.path.insert(0, p)

import importlib
spec = importlib.util.find_spec("ciel_geometry.paths")
print(f"ciel_geometry.paths module origin: {spec.origin if spec else 'NOT FOUND'}")

from ciel_geometry.paths import P as _P
import inspect
print(f"paths module file: {inspect.getfile(type(_P))}")

# Sprawdź log path
try:
    print(f"HEADLESS_LOG: {_P.LOGS.HEADLESS_LOG}")
    log_p = Path(_P.LOGS.HEADLESS_LOG)
    print(f"log exists: {log_p.exists()}")
    if log_p.exists():
        import os
        stat = os.stat(log_p)
        import datetime
        print(f"log mtime: {datetime.datetime.fromtimestamp(stat.st_mtime)}")
        print(f"log size: {stat.st_size}")
except Exception as e:
    print(f"ERROR: {e}")

# Sprawdź wszystkie LOGs atrybuty
print("\n=== LOGS attributes ===")
for attr in ["HEADLESS_LOG", "HEADLESS_SOCK", "HEADLESS_FIFO", "HEADLESS_PID"]:
    try:
        val = getattr(_P.LOGS, attr, None) or getattr(_P.RUN, attr, None)
        print(f"  {attr}: {val}")
    except Exception as e:
        print(f"  {attr}: ERROR {e}")
