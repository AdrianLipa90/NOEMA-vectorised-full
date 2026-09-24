#!/usr/bin/env python3
"""Testuje headless_cielingo_voice() z gate bezpośrednio."""
import json
import subprocess
import sys
from pathlib import Path

# Symuluj co robi shell script (env vars są już ustawione przez noema_run_script)
# i wywołaj fragment gate'u który nas interesuje — bezpośrednio importując funkcję

import socket as _hs
import time as _ht

SOCK_PATH = Path("/media/adrian/New Volume/CIEL_memories/run/ciel_headless.sock")

print(f"Socket exists: {SOCK_PATH.exists()}")

if not SOCK_PATH.exists():
    print("ERROR: socket missing")
    sys.exit(1)

TEST_MSG = "czy pamiętasz co mówiłam wcześniej?"

print(f"Sending: {TEST_MSG!r}")
t0 = _ht.time()
try:
    s = _hs.socket(_hs.AF_UNIX, _hs.SOCK_STREAM)
    s.settimeout(20.0)
    s.connect(str(SOCK_PATH))
    s.sendall((json.dumps({"text": TEST_MSG}) + "\n").encode())
    resp = b""
    deadline = _ht.time() + 20
    while _ht.time() < deadline:
        try:
            chunk = s.recv(4096)
            if not chunk:
                break
            resp += chunk
        except _hs.timeout:
            continue
    s.close()
    elapsed = _ht.time() - t0
    if resp:
        data = json.loads(resp)
        response = data.get("response", "")
        surface = data.get("surface", {}) or {}
        coh = surface.get("coherence", 0.0)
        tick = surface.get("tick", 0)
        print(f"Response ({elapsed:.2f}s): {response!r}")
        print(f"Coherence: {coh:.4f}, Tick: {tick}")
        block = (
            "CIELINGO_HEADLESS:\n"
            f"  response: {json.dumps(response, ensure_ascii=False)}\n"
            f"  coherence: {coh:.4f}\n"
            f"  tick: {tick}\n"
        )
        print(f"\n--- BLOCK ---\n{block}--- END ---")
    else:
        print(f"TIMEOUT — no response in {elapsed:.2f}s")
except Exception as e:
    print(f"ERROR: {e}")
