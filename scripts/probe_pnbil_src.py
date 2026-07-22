#!/usr/bin/env python3
"""Czytaj pn_bil/src: phasenav.py + noema_sot.py."""
import zipfile
from pathlib import Path

ZIP = Path("/media/adrian/REPOZYTORIA_GIT1/phasenav-binary-immune-surface-v0.4-gitrepo.zip")

KEY = [
    "phasenav-binary-immune-surface/src/pn_bil/phasenav.py",
    "phasenav-binary-immune-surface/src/pn_bil/noema_sot.py",
    "phasenav-binary-immune-surface/src/pn_bil/immune.py",
    "phasenav-binary-immune-surface/src/pn_bil/__init__.py",
    "phasenav-binary-immune-surface/src/pn_bil/schema.py",
]

with zipfile.ZipFile(ZIP) as zf:
    for kf in KEY:
        print(f"\n=== {kf.split('/')[-1]} ===")
        try:
            print(zf.read(kf).decode("utf-8", errors="replace")[:3500])
        except Exception as e:
            print(f"  ERROR: {e}")
