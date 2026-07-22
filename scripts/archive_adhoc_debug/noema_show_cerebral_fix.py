#!/usr/bin/env python3
"""Pokaż pełną zawartość kluczowych plików z ZIP."""
from pathlib import Path

BASE = Path("/media/adrian/New Volume/CIEL_memories/tmp_cerebral_fix")

files = [
    "scripts/ciel_cerebral_model.py",
    "scripts/ciel_cerebral_continuity.py",
    "scripts/ciel_language_runtime.py",
    "docs/architecture/CIEL_CEREBRAL_MODEL_v0_1.md",
]

for fname in files:
    p = BASE / fname
    if p.exists():
        txt = p.read_text(errors="replace")
        print(f"\n{'#'*70}")
        print(f"# FILE: {fname}  ({len(txt)} chars)")
        print('#'*70)
        print(txt)
    else:
        print(f"MISSING: {fname}")
