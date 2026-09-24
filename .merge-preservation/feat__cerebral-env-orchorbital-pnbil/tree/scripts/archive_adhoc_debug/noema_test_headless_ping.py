#!/usr/bin/env python3
import json, socket, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from ciel_geometry.paths import P

sock_path = P.RUN.HEADLESS_SOCK
print(f"Socket: {sock_path}")
print(f"Exists: {Path(sock_path).exists()}")

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.settimeout(50)
s.connect(sock_path)
s.sendall("Cześć, Ciel. Jesteś tutaj?".encode("utf-8"))
s.shutdown(socket.SHUT_WR)
buf = b""
while True:
    d = s.recv(65536)
    if not d: break
    buf += d
s.close()
result = json.loads(buf.decode("utf-8"))
print(f"Response: {result.get('response', '???')[:300]}")
print(f"Operator: {result.get('frame', {}).get('operator', '?')}")
print(f"OK: True")
