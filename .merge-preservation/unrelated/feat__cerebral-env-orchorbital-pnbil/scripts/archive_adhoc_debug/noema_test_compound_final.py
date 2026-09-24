#!/usr/bin/env python3
"""Finalny test: czy Ciel sklada 15 zdań złożonych z prose entries."""
import sys, json, socket, time
from pathlib import Path

SOCKET_PATH = "/media/adrian/New Volume/CIEL_memories/run/ciel_headless.sock"

def send_query(question: str) -> dict:
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(30)
    sock.connect(SOCKET_PATH)
    payload = json.dumps({"type": "chat", "text": question, "session_id": "test-final"}) + "\n"
    sock.sendall(payload.encode())
    buf = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        buf += chunk
        if b"\n" in buf:
            break
    sock.close()
    line = buf.split(b"\n")[0]
    return json.loads(line)

print("=== TEST FINALNY: 15 zdań złożonych ===\n")

pytania = [
    "Czym jest system NOEMA i jak działa jego architektura?",
    "Opowiedz mi o kanałach pamięci w systemie.",
]

for q in pytania:
    print(f"PYTANIE: {q}")
    print("-" * 60)
    t0 = time.time()
    resp = send_query(q)
    dt = time.time() - t0
    text = resp.get("text", "") or resp.get("response", "") or str(resp)
    print(text)
    # Policz zdania złożone (zawierające , lub które lub ponieważ lub oraz lub jednak)
    import re
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.strip()) > 30]
    compound = [s for s in sentences if any(w in s.lower() for w in
                [',', 'który', 'która', 'które', 'ponieważ', 'oraz', 'jednak', 'chociaż',
                 'kiedy', 'gdzie', 'dlatego', 'poprzez', 'zarówno', 'natomiast', 'lecz'])]
    print(f"\n[dt={dt:.1f}s] Zdania ogółem: {len(sentences)}, złożone: {len(compound)}")
    print("=" * 60)
