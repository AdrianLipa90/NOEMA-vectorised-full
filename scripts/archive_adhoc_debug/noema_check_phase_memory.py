#!/usr/bin/env python3
"""Sprawdź stan PhaseMemory i CIELingo learning."""
import sys, json, socket, time
from pathlib import Path

SOCK = "/media/adrian/New Volume/CIEL_memories/run/ciel_headless.sock"

def query_ciel(method, params=None, timeout=8):
    req = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}}
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect(SOCK)
        s.sendall((json.dumps(req) + "\n").encode())
        buf = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            buf += chunk
            if b"\n" in buf:
                break
        return json.loads(buf.decode().strip())
    finally:
        s.close()

# Sprawdź phase memory stats
print("=== PhaseMemory stats ===")
try:
    r = query_ciel("phase_memory_stats")
    print(f"Stats: {json.dumps(r.get('result', r), ensure_ascii=False, indent=2)[:500]}")
except Exception as e:
    print(f"phase_memory_stats: {e}")

# Sprawdź openness i learning
print("\n=== CIELingo learning state ===")
try:
    r2 = query_ciel("cielingo_status")
    result = r2.get("result", r2)
    for k in ["openness", "phase_memory_size", "learning_enabled", "kb_connected", "last_learn_ts"]:
        if k in result:
            print(f"  {k}: {result[k]}")
    # Pokaż pełne pole jeśli małe
    if len(str(result)) < 800:
        print(f"  (pełne): {result}")
except Exception as e:
    print(f"cielingo_status: {e}")

# Sprawdź ostatnie wpisy PhaseMemory
PM_DIR = Path("/media/adrian/New Volume/CIEL_memories/state/cielingo_phase_memory")
if PM_DIR.exists():
    files = sorted(PM_DIR.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)[:3]
    print(f"\n=== Ostatnie wpisy PhaseMemory (razem {len(list(PM_DIR.iterdir()))} plików) ===")
    for f in files:
        mtime = time.ctime(f.stat().st_mtime)
        print(f"  {f.name} [{mtime}]")
