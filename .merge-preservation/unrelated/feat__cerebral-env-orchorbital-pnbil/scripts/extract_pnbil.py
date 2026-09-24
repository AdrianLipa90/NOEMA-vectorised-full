#!/usr/bin/env python3
"""Extraktuj pn_bil z zip do NOEMA/src/pn_bil/."""
import zipfile, sys
from pathlib import Path

ZIP = Path("/media/adrian/REPOZYTORIA_GIT1/phasenav-binary-immune-surface-v0.4-gitrepo.zip")
DEST = Path(__file__).resolve().parents[1] / "src" / "pn_bil"
DEST.mkdir(parents=True, exist_ok=True)

SRC_PREFIX = "phasenav-binary-immune-surface/src/pn_bil/"

with zipfile.ZipFile(ZIP) as zf:
    extracted = []
    for name in zf.namelist():
        if name.startswith(SRC_PREFIX) and name.endswith(".py"):
            rel = name[len(SRC_PREFIX):]
            if not rel:
                continue
            out = DEST / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(zf.read(name))
            extracted.append(str(rel))
            print(f"  extracted: {rel}")

print(f"\nDone: {len(extracted)} files → {DEST}")

# Sprawdź czy można zaimportować
sys.path.insert(0, str(DEST.parent))
try:
    from pn_bil.phasenav import PHASENAV_24D_COMPONENTS, build_phase_vector, seed_from_sha256
    print(f"\nImport OK — {len(PHASENAV_24D_COMPONENTS)} komponenty fazowe")
except Exception as e:
    print(f"\nImport ERROR: {e}")
