#!/usr/bin/env python3
"""Symuluje dokładnie to co gate robi: ładuje gate module i wywołuje headless_cielingo_voice."""
import sys, importlib.util, json
from pathlib import Path

GATE = Path("/home/adrian/.config/opencode/noema_hooks/noema_sync_dispatch_gate.py")
print(f"Gate exists: {GATE.exists()}")
print(f"Gate mtime:  {GATE.stat().st_mtime:.0f}")

# Sprawdź czy pyc istnieje
pyc = Path("/home/adrian/.config/opencode/noema_hooks/__pycache__/noema_sync_dispatch_gate.cpython-312.pyc")
print(f"pyc exists:  {pyc.exists()}")

# Wczytaj funkcję bezpośrednio z pliku
spec = importlib.util.spec_from_file_location("gate_module", GATE)
mod = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(mod)
    print("Gate module loaded OK")
except Exception as e:
    print(f"Gate module LOAD ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Wywołaj headless_cielingo_voice
print("\nCalling headless_cielingo_voice('test message', None)...")
try:
    result = mod.headless_cielingo_voice("test message z symulacji gate", None)
    print(f"Result: {result}")
except Exception as e:
    print(f"EXCEPTION in headless_cielingo_voice: {e}")
    import traceback
    traceback.print_exc()

# Sprawdź czy pliki debug istnieją po wywołaniu
ntfs = Path("/media/adrian/New Volume/CIEL_memories/state/headless_gate_debug.json")
local = Path("/home/adrian/noema/headless_gate_debug_local.json")
print(f"\nAfter call:")
print(f"  NTFS debug:  exists={ntfs.exists()}")
if ntfs.exists():
    print(f"    content: {ntfs.read_text()[:300]}")
print(f"  LOCAL debug: exists={local.exists()}")
if local.exists():
    print(f"    content: {local.read_text()[:300]}")
