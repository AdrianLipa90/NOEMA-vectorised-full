#!/usr/bin/env python3
"""Ping headless z timeoutem 50s."""
from __future__ import annotations
import json, pathlib, socket as _socket, time

SOCK = pathlib.Path("/media/adrian/New Volume/CIEL_memories/run/ciel_headless.sock")
print(f"Connecting to {SOCK}...", flush=True)

s = _socket.socket(_socket.AF_UNIX, _socket.SOCK_STREAM)
s.settimeout(2.0)
s.connect(str(SOCK))
print("Connected.", flush=True)

msg = json.dumps({"text": "cześć, Ciel"}) + "\n"
s.sendall(msg.encode())
print(f"Sent: {msg.strip()}", flush=True)

resp = b""
deadline = time.time() + 50  # 50s timeout
while time.time() < deadline:
    try:
        chunk = s.recv(4096)
        if not chunk:
            break
        resp += chunk
    except _socket.timeout:
        elapsed = deadline - time.time()
        if elapsed > 0:
            print(f"  ... czekam ({50 - elapsed:.0f}s elapsed) ...", flush=True)
        continue
s.close()

elapsed = 50 - (deadline - time.time())
print(f"\nResponse ({len(resp)} bytes, {elapsed:.1f}s elapsed):", flush=True)
if resp:
    try:
        d = json.loads(resp)
        print(json.dumps(d, indent=2, ensure_ascii=False)[:1000])
    except Exception:
        print(resp[:500].decode(errors="replace"))
else:
    print("BRAK ODPOWIEDZI — process_text() zajął >50s lub daemon się zawiesił")
