#!/usr/bin/env python3
"""Czytaj rdzeń pn_bil: phasenav.py, noema_sot.py, immune.py."""
import zipfile
from pathlib import Path

ZIP = Path("/media/adrian/REPOZYTORIA_GIT1/phasenav-binary-immune-surface-v0.4-gitrepo.zip")

KEY_FILES = [
    "phasenav-binary-immune-surface/pn_bil/phasenav.py",
    "phasenav-binary-immune-surface/pn_bil/noema_sot.py",
    "phasenav-binary-immune-surface/pn_bil/immune.py",
    "phasenav-binary-immune-surface/pn_bil/__init__.py",
]

with zipfile.ZipFile(ZIP) as zf:
    all_names = zf.namelist()
    py_names = [n for n in all_names if n.endswith(".py") and "/.git/" not in n and "__pycache__" not in n]
    print("=== wszystkie .py pliki ===")
    for n in sorted(py_names):
        print(f"  {n}")

    for kf in KEY_FILES:
        if kf in all_names:
            print(f"\n=== {kf} ===")
            print(zf.read(kf).decode("utf-8", errors="replace")[:3000])
        else:
            print(f"\n  BRAK: {kf}")

# aux w NOEMA
NOEMA_ROOT = Path(__file__).resolve().parents[1]
for d in ["aux", "src/aux", "integration/aux"]:
    p = NOEMA_ROOT / d
    if p.exists():
        print(f"\n=== {p} ===")
        for f in sorted(p.iterdir())[:20]:
            print(f"  {f.name}")
