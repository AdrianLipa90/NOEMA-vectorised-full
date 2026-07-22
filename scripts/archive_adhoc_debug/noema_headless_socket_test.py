#!/usr/bin/env python3
"""Krotki test socket headless + ostatnie 20 linii po 14:47:39."""
import subprocess, socket, json, time
from pathlib import Path

# Tylko linie po restarcie
r = subprocess.run(
    ["journalctl", "--user", "-u", "noema-headless.service",
     "--since", "14:47:35", "-n", "30", "--no-pager"],
    capture_output=True, text=True
)
print("=== JOURNAL od 14:47:35 ===")
print(r.stdout)

# Test socket
sock_path = "/media/adrian/New Volume/CIEL_memories/run/ciel_headless.sock"
sp = Path(sock_path)
print(f"\n=== SOCKET TEST ===")
if not sp.exists():
    print("BLAD: socket nie istnieje!")
else:
    t0 = time.time()
    try:
        c = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        c.settimeout(15.0)
        c.connect(sock_path)
        msg = json.dumps({"text": "test"}) + "\n"
        c.sendall(msg.encode())
        buf = b""
        dl = time.time() + 15.0
        while time.time() < dl:
            try:
                chunk = c.recv(4096)
                if not chunk:
                    break
                buf += chunk
                if len(buf) > 100:
                    break
            except socket.timeout:
                continue
        c.close()
        elapsed = time.time() - t0
        print(f"czas: {elapsed:.1f}s")
        if buf:
            d = json.loads(buf)
            print(f"response[:100]: {str(d.get('response', ''))[:100]}")
            surf = d.get("surface") or {}
            print(f"coherence: {surf.get('coherence')}")
            print(f"tick: {surf.get('tick')}")
        else:
            print("BLAD: brak odpowiedzi!")
    except Exception as e:
        print(f"BLAD: {e} (elapsed {time.time()-t0:.1f}s)")
