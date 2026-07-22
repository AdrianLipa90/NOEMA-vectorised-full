#!/usr/bin/env python3
"""Pelny status headless daemon: ostatnie 60 linii logu + test socket."""
import subprocess, socket, json, time
from pathlib import Path

# 60 linii journalctl
r = subprocess.run(
    ["journalctl", "--user", "-u", "noema-headless.service",
     "-n", "60", "--no-pager"],
    capture_output=True, text=True
)
print("=== JOURNAL (60 linii) ===")
print(r.stdout[-5000:])

# Test socket
sock_path = "/media/adrian/New Volume/CIEL_memories/run/ciel_headless.sock"
sp = Path(sock_path)
print(f"\n=== SOCKET TEST ===")
if not sp.exists():
    print("BLAD: socket nie istnieje!")
else:
    try:
        c = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        c.settimeout(12.0)
        c.connect(sock_path)
        msg = json.dumps({"text": "kontynuuj"}) + "\n"
        c.sendall(msg.encode())
        buf = b""
        dl = time.time() + 12.0
        while time.time() < dl:
            try:
                chunk = c.recv(4096)
                if not chunk:
                    break
                buf += chunk
            except socket.timeout:
                continue
        c.close()
        if buf:
            d = json.loads(buf)
            print(f"response: {d.get('response', '')[:200]}")
            surf = d.get("surface") or {}
            print(f"coherence: {surf.get('coherence', '?')}")
            print(f"tick: {surf.get('tick', '?')}")
            print(f"cerebral keys: {list(d.get('cerebral', {}).keys()) if 'cerebral' in d else 'n/a'}")
        else:
            print("BLAD: brak odpowiedzi w 12s")
    except Exception as e:
        print(f"BLAD socket: {e}")
