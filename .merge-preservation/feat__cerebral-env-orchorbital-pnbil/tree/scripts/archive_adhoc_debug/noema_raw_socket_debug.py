#!/usr/bin/env python3
"""Raw socket debug — co dokładnie zwraca daemon."""
import socket, json, time

SOCKET_PATH = "/media/adrian/New Volume/CIEL_memories/run/ciel_headless.sock"

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.settimeout(20)
s.connect(SOCKET_PATH)
payload = json.dumps({"type": "chat", "text": "Czym jest system NOEMA i jak działa?", "session_id": "raw-debug"}) + "\n"
print(f"Wysylam: {payload[:100]}")
s.sendall(payload.encode())

buf = b""
t0 = time.time()
while time.time() - t0 < 20:
    try:
        chunk = s.recv(4096)
    except socket.timeout:
        print("TIMEOUT")
        break
    if not chunk:
        print(f"Connection closed. Received {len(buf)} bytes.")
        break
    buf += chunk
    print(f"Chunk ({len(chunk)} bytes): {chunk[:200]!r}")
    if b"\n" in buf:
        break

s.close()
print(f"\nTotal: {len(buf)} bytes")
print(f"Raw: {buf[:500]!r}")

if buf.strip():
    line = buf.split(b"\n")[0]
    try:
        resp = json.loads(line)
        print(f"\nJSON keys: {list(resp.keys())}")
        for k, v in resp.items():
            print(f"  {k}: {repr(str(v)[:150])}")
    except Exception as e:
        print(f"JSON parse error: {e}")
