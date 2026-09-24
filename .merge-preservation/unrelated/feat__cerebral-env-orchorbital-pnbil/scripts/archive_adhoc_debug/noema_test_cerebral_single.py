#!/usr/bin/env python3
"""Test — jedno pytanie przez headless socket, timeout 25s."""
import socket, json, time
from pathlib import Path

SOCK = Path("/media/adrian/New Volume/CIEL_memories/run/ciel_headless.sock")
QUESTION = "Czym jest przestrzeń fazowa?"

print(f"Asking: {QUESTION!r}")
t0 = time.time()

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.settimeout(25.0)
s.connect(str(SOCK))
s.sendall((json.dumps({"text": QUESTION}) + "\n").encode())
resp = b""
deadline = time.time() + 25
while time.time() < deadline:
    try:
        chunk = s.recv(4096)
        if not chunk: break
        resp += chunk
    except socket.timeout:
        continue
s.close()
elapsed = time.time() - t0

if not resp:
    print(f"TIMEOUT after {elapsed:.1f}s")
else:
    d = json.loads(resp)
    print(f"Time: {elapsed:.1f}s")
    print(f"Response: {d.get('response', d.get('error', '???'))[:500]}")
    # Sprawdź czy cerebral model był użyty
    print(f"Error field: {d.get('error', 'none')}")
    print(f"Full keys: {list(d.keys())}")
