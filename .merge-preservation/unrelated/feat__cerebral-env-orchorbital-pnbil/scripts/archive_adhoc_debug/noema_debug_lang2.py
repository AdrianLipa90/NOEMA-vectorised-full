#!/usr/bin/env python3
"""Debug: sprawdz reply przez socket i porownaj z oczekiwanym."""
import sys, json, socket, time
from pathlib import Path

SOCKET_PATH = "/media/adrian/New Volume/CIEL_memories/run/ciel_headless.sock"

def send_query(question: str) -> dict:
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(30)
    sock.connect(SOCKET_PATH)
    payload = json.dumps({"type": "chat", "text": question, "session_id": "debug-lang-test"}) + "\n"
    sock.sendall(payload.encode())
    buf = b""
    while True:
        chunk = sock.recv(8192)
        if not chunk:
            break
        buf += chunk
        if b"\n" in buf:
            break
    sock.close()
    line = buf.split(b"\n")[0]
    return json.loads(line)

q = "Czym jest system NOEMA i jak działa jego architektura?"
print(f"Pytanie: {q}")
print(f"Polskie znaki w pytaniu: {[c for c in q if c in 'ąćęłńóśźżĄĆĘŁŃÓŚŹŻ']}")
print()

resp = send_query(q)
text = resp.get("text", "") or resp.get("response", "")
print("=== ODPOWIEDZ ===")
print(text[:500])
print()

# Sprawdz czy polskie connektory
has_pl = any(w in text for w in ["Ponadto,", "Warto dodać", "Jednocześnie", "Co więcej", "Pamiętam"])
has_en = any(w in text for w in ["Furthermore", "I remember that", "Moreover"])
print(f"PL connektory: {has_pl}")
print(f"EN connektory: {has_en}")
