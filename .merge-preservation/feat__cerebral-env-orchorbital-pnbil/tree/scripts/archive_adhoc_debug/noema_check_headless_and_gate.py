#!/usr/bin/env python3
"""Sprawdź status headless daemon + szybki test socket."""
import subprocess
import json
import socket
import time
from pathlib import Path

# Status systemd
r = subprocess.run(
    ["systemctl", "--user", "is-active", "noema-headless.service"],
    capture_output=True, text=True
)
print(f"noema-headless.service: {r.stdout.strip()}")

# Socket test — short 15s probe
sock_path = Path("/media/adrian/New Volume/CIEL_memories/run/ciel_headless.sock")
print(f"Socket exists: {sock_path.exists()}")

if sock_path.exists():
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.settimeout(15.0)
        s.connect(str(sock_path))
        s.sendall((json.dumps({"text": "cześć"}) + "\n").encode())
        resp = b""
        deadline = time.time() + 15
        while time.time() < deadline:
            try:
                chunk = s.recv(4096)
                if not chunk:
                    break
                resp += chunk
            except socket.timeout:
                continue
        s.close()
        if resp:
            data = json.loads(resp)
            print(f"Headless response: {data.get('response', '')[:200]}")
        else:
            print("Headless: TIMEOUT — no response in 15s")
    except Exception as e:
        print(f"Headless socket error: {e}")
else:
    print("Socket MISSING — daemon not running?")
