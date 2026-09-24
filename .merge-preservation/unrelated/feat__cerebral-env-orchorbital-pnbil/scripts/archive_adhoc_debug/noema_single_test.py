#!/usr/bin/env python3
"""Test jednego pytania do headless."""
import json, pathlib, socket as _socket, time

SOCK = pathlib.Path("/media/adrian/New Volume/CIEL_memories/run/ciel_headless.sock")
QUERY = "ile masz lat?"

s = _socket.socket(_socket.AF_UNIX, _socket.SOCK_STREAM)
s.settimeout(2.0)
s.connect(str(SOCK))
s.sendall((json.dumps({"text": QUERY}) + "\n").encode())
resp = b""
deadline = time.time() + 25
while time.time() < deadline:
    try:
        chunk = s.recv(4096)
        if not chunk:
            break
        resp += chunk
    except _socket.timeout:
        continue
s.close()

if not resp:
    print("BRAK ODPOWIEDZI")
else:
    d = json.loads(resp)
    print(f"Q: {QUERY}")
    print(f"A: {d.get('response', 'BRAK')}")
    print(f"mode: {d.get('episodic_mode', d.get('mode', '?'))}")
