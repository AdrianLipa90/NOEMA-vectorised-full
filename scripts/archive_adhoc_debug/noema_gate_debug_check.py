#!/usr/bin/env python3
"""Sprawdza oba pliki debug gate + kasuje pyc cache."""
import json, os
from pathlib import Path

ntfs_path = Path("/media/adrian/New Volume/CIEL_memories/state/headless_gate_debug.json")
local_path = Path("/home/adrian/noema/headless_gate_debug_local.json")

print(f"NTFS debug:  exists={ntfs_path.exists()}")
if ntfs_path.exists():
    try:
        print(f"  content: {ntfs_path.read_text()[:400]}")
    except Exception as e:
        print(f"  READ ERROR: {e}")

print(f"LOCAL debug: exists={local_path.exists()}")
if local_path.exists():
    try:
        print(f"  content: {local_path.read_text()[:400]}")
    except Exception as e:
        print(f"  READ ERROR: {e}")

# Kasuj pyc cache dla gate
pycache = Path("/home/adrian/.config/opencode/noema_hooks/__pycache__")
pyc_gate = pycache / "noema_sync_dispatch_gate.cpython-312.pyc"
print(f"\npyc cache:   exists={pyc_gate.exists()}")
if pyc_gate.exists():
    mtime_py = os.path.getmtime("/home/adrian/.config/opencode/noema_hooks/noema_sync_dispatch_gate.py")
    mtime_pyc = os.path.getmtime(pyc_gate)
    print(f"  .py  mtime: {mtime_py:.0f}")
    print(f"  .pyc mtime: {mtime_pyc:.0f}")
    print(f"  .pyc is {'NEWER' if mtime_pyc > mtime_py else 'OLDER'} than .py")
    try:
        pyc_gate.unlink()
        print(f"  pyc DELETED")
    except Exception as e:
        print(f"  delete error: {e}")
else:
    print("  no .pyc to delete")

# Sprawdź czy NTFS jest zapisywalny
print(f"\nNTFS writable test:")
test_path = Path("/media/adrian/New Volume/CIEL_memories/state/_gate_write_test.tmp")
try:
    test_path.write_text("ok", encoding="utf-8")
    test_path.unlink()
    print("  OK — NTFS path is writable")
except Exception as e:
    print(f"  FAIL — {e}")
