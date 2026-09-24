#!/usr/bin/env python3
"""Czytaj pliki py z binarki phasenav i aux z CIEL_memories."""
import zipfile, sys
from pathlib import Path

ZIP = Path("/media/adrian/REPOZYTORIA_GIT1/phasenav-binary-immune-surface-v0.4-gitrepo.zip")

print("=== pliki .py w phasenav-binary ===")
with zipfile.ZipFile(ZIP) as zf:
    py_files = [n for n in zf.namelist() if n.endswith(".py") and not ".git/" in n]
    for n in sorted(py_files):
        print(f"  {n}")

    # Czytaj kluczowe pliki
    for n in sorted(py_files):
        if any(k in n for k in ["immune", "surface", "phasenav", "binary", "inference", "bloch", "orchorbital"]):
            print(f"\n=== {n} ===")
            try:
                content = zf.read(n).decode("utf-8", errors="replace")
                print(content[:2000])
            except Exception as e:
                print(f"  ERROR: {e}")

# aux
CIEL_MEM = Path("/media/adrian/New Volume/CIEL_memories")
AUX = CIEL_MEM / "aux"
print(f"\n=== CIEL_memories/aux: {'EXISTS' if AUX.exists() else 'MISSING'} ===")
if AUX.exists():
    for f in sorted(AUX.iterdir())[:20]:
        print(f"  {f.name}")
