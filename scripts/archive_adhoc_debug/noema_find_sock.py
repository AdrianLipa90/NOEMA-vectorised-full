#!/usr/bin/env python3
"""Znajdz poprawna sciezke do headless socket."""
import sys
from pathlib import Path

ROOT = Path("/home/adrian/noema")
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.paths import P as _P
print("HEADLESS_SOCK:", getattr(_P.RUN, "HEADLESS_SOCK", "BRAK"))
print("RUN attrs:", [a for a in dir(_P.RUN) if not a.startswith("_")])
