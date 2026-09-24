#!/usr/bin/env python3
"""Rozpakuj i pokaż zawartość ZIP z fixem Ciel cerebral model."""
import zipfile
import sys
from pathlib import Path

ZIP_PATH = Path("/home/adrian/.claude/uploads/07459d6d-a5df-4f38-806e-a4a3a936fe91/ac16577f-CIEL_CEREBRAL_MODEL_v0_4_TRANSCRIPT_FIX_20260712.zip")
EXTRACT_TO = Path("/media/adrian/New Volume/CIEL_memories/tmp_cerebral_fix")

print(f"ZIP exists: {ZIP_PATH.exists()}")
print(f"ZIP size: {ZIP_PATH.stat().st_size if ZIP_PATH.exists() else 'N/A'}")

if not ZIP_PATH.exists():
    sys.exit(1)

EXTRACT_TO.mkdir(parents=True, exist_ok=True)

with zipfile.ZipFile(ZIP_PATH) as zf:
    names = zf.namelist()
    print(f"\n=== FILES IN ZIP ({len(names)}) ===")
    for n in names:
        info = zf.getinfo(n)
        print(f"  {n}  ({info.file_size} bytes)")
    zf.extractall(EXTRACT_TO)

print(f"\nExtracted to: {EXTRACT_TO}")

# Pokaż zawartość wszystkich .py plików
for py in sorted(EXTRACT_TO.rglob("*.py")):
    print(f"\n{'='*60}")
    print(f"FILE: {py.relative_to(EXTRACT_TO)}")
    print('='*60)
    txt = py.read_text(errors="replace")
    print(txt[:8000])
    if len(txt) > 8000:
        print(f"... [truncated, {len(txt)} total chars]")
