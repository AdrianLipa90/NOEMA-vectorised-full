#!/usr/bin/env python3
"""Czytaj topology_api.py, middleware.py i zawartość binarki phasenav."""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OMEGA_ROOT = REPO_ROOT / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM" / "ciel_omega"

# 1. topology_api.py
topo = (OMEGA_ROOT / "inference" / "topology_api.py").read_text()
print("=== topology_api.py ===")
print(topo[:3000])

# 2. middleware.py
mw = (OMEGA_ROOT / "inference" / "middleware.py").read_text()
print("\n=== middleware.py ===")
print(mw[:2000])

# 3. Zawartość binarki zip
import zipfile
ZIP = Path("/media/adrian/REPOZYTORIA_GIT1/phasenav-binary-immune-surface-v0.4-gitrepo.zip")
print("\n=== phasenav-binary zip contents ===")
with zipfile.ZipFile(ZIP) as zf:
    for name in sorted(zf.namelist())[:60]:
        print(f"  {name}")
