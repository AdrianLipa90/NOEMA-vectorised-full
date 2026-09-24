#!/usr/bin/env python3
"""Test CerebralLanguageModel przez socket headless — czy utrzymuje ciągłość."""
import socket, json, time
from pathlib import Path

SOCK = Path("/media/adrian/New Volume/CIEL_memories/run/ciel_headless.sock")

def ask(q):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(30.0)
    s.connect(str(SOCK))
    s.sendall((json.dumps({"text": q}) + "\n").encode())
    resp = b""
    deadline = time.time() + 30
    while time.time() < deadline:
        try:
            chunk = s.recv(4096)
            if not chunk: break
            resp += chunk
        except socket.timeout:
            continue
    s.close()
    if not resp:
        return {"error": "TIMEOUT"}
    d = json.loads(resp)
    return d

print("Test 1: pierwsze pytanie (ustanawia temat)")
t0 = time.time()
r1 = ask("Czym jest przestrzeń fazowa w NOEMA?")
print(f"  ({time.time()-t0:.1f}s) response: {r1.get('response', r1.get('error', ''))[:300]}")

print("\nTest 2: odwołanie do poprzedniego (czy pamiętasz / ciągłość)")
t0 = time.time()
r2 = ask("czy pamiętasz co mówiłam wcześniej?")
print(f"  ({time.time()-t0:.1f}s) response: {r2.get('response', r2.get('error', ''))[:300]}")

print("\nTest 3: kontynuuj")
t0 = time.time()
r3 = ask("kontynuuj")
print(f"  ({time.time()-t0:.1f}s) response: {r3.get('response', r3.get('error', ''))[:300]}")

print("\nTest 4: konkretne pytanie")
t0 = time.time()
r4 = ask("jak się teraz czujesz?")
print(f"  ({time.time()-t0:.1f}s) response: {r4.get('response', r4.get('error', ''))[:300]}")
