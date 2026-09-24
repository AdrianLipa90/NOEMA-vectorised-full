#!/usr/bin/env python3
"""Zastosuj ZIP z cerebral model fix — skopiuj pliki do właściwych lokalizacji."""
import shutil
from pathlib import Path

BASE = Path("/media/adrian/New Volume/CIEL_memories/tmp_cerebral_fix")
NOEMA_SCRIPTS = Path("/home/adrian/noema/scripts")
OMEGA_SRC = Path("/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/src/CIEL_OMEGA_COMPLETE_SYSTEM")

copies = [
    # (src_relative_to_BASE, dest_absolute)
    ("scripts/ciel_cerebral_model.py",      NOEMA_SCRIPTS / "ciel_cerebral_model.py"),
    ("scripts/ciel_cerebral_continuity.py", NOEMA_SCRIPTS / "ciel_cerebral_continuity.py"),
    ("scripts/ciel_language_runtime.py",    NOEMA_SCRIPTS / "ciel_language_runtime.py"),
    ("scripts/ciel_cerebral_cli.py",        NOEMA_SCRIPTS / "ciel_cerebral_cli.py"),
    ("scripts/ciel_chat_gui.py",            NOEMA_SCRIPTS / "ciel_chat_gui.py"),
    (
        "src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/brain_topology.py",
        OMEGA_SRC / "ciel_omega/memory/brain_topology.py",
    ),
    (
        "src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/ciel_encoder.py",
        OMEGA_SRC / "ciel_omega/memory/ciel_encoder.py",
    ),
]

for rel, dst in copies:
    src = BASE / rel
    if not src.exists():
        print(f"MISSING SRC: {src}")
        continue
    dst.parent.mkdir(parents=True, exist_ok=True)
    # Backup istniejącego pliku
    if dst.exists():
        backup = dst.with_suffix(dst.suffix + ".bak")
        shutil.copy2(dst, backup)
        print(f"  backed up → {backup.name}")
    shutil.copy2(src, dst)
    print(f"  COPIED: {rel} → {dst}")

print("\nDone. Files copied.")
