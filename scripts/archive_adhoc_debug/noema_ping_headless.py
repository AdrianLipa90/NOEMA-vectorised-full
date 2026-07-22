#!/usr/bin/env python3
"""Ping headless daemon przez socket."""
from __future__ import annotations
import json, pathlib, socket as _socket, sys, time

SOCK = pathlib.Path("/media/adrian/New Volume/CIEL_memories/run/ciel_headless.sock")

print(f"Socket: {SOCK}")
print(f"Exists: {SOCK.exists()}")

if SOCK.exists():
    try:
        s = _socket.socket(_socket.AF_UNIX, _socket.SOCK_STREAM)
        s.settimeout(5.0)
        s.connect(str(SOCK))
        msg = json.dumps({"text": "cześć"}) + "\n"
        s.sendall(msg.encode())
        resp = b""
        deadline = time.time() + 10
        while time.time() < deadline:
            try:
                chunk = s.recv(4096)
                if not chunk:
                    break
                resp += chunk
            except _socket.timeout:
                break
        s.close()
        print(f"Response ({len(resp)} bytes): {resp[:500].decode(errors='replace')}")
    except Exception as e:
        print(f"Connection ERROR: {type(e).__name__}: {e}")
else:
    print("SOCKET NIE ISTNIEJE — daemon nie powiązał socketa!")
    # Sprawdź czy plik RUN dir istnieje
    run_dir = SOCK.parent
    print(f"run/ dir exists: {run_dir.exists()}")
    if run_dir.exists():
        print(f"run/ contents: {list(run_dir.iterdir())}")
