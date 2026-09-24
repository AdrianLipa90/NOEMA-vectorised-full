#!/usr/bin/env python3
"""Test: policz 15 zdań złożonych z full output do pliku."""
import sys, json, socket, time, re
from pathlib import Path

SOCKET_PATH = "/media/adrian/New Volume/CIEL_memories/run/ciel_headless.sock"
OUT_FILE = Path("/media/adrian/New Volume/CIEL_memories/logs/test_15_sentences.txt")

def send_query(question: str) -> str:
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(30)
    sock.connect(SOCKET_PATH)
    payload = json.dumps({"type": "chat", "text": question, "session_id": "test-15-final"}) + "\n"
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
    resp = json.loads(line)
    return resp.get("text", "") or resp.get("response", "")

q = "Czym jest system NOEMA i jak działa jego architektura?"
t0 = time.time()
text = send_query(q)
dt = time.time() - t0

# Policz zdania — split po [.!?]
sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if len(s.strip()) > 20]
compound = [s for s in sentences if any(w in s.lower() for w in
            [',', 'który', 'która', 'które', 'ponieważ', 'oraz', 'jednak', 'chociaż',
             'kiedy', 'gdzie', 'dlatego', 'poprzez', 'zarówno', 'natomiast', 'lecz',
             'odpowiedzialny', 'oparty', 'opartym', 'łączy', 'łączący'])]

has_pl = any(w in text for w in ["Ponadto,", "Warto dodać", "Jednocześnie", "Co więcej", "Pamiętam"])
has_en = any(w in text for w in ["Furthermore", "I remember that", "Moreover"])

output = f"""=== TEST 15 ZDAŃ ZŁOŻONYCH ===
czas: {dt:.1f}s
dlugosc odpowiedzi: {len(text)} znakow
zdania ogolem: {len(sentences)}
zdania zlozonych: {len(compound)}
PL connektory: {has_pl}
EN connektory: {has_en}

=== PELNA ODPOWIEDZ ===
{text}

=== ZDANIA ZLOZONYCH ({len(compound)}) ===
""" + "\n".join(f"[{i+1}] {s}" for i, s in enumerate(compound))

OUT_FILE.write_text(output)
print(f"Wynik zapisany do: {OUT_FILE}")
print(f"Zdania ogółem: {len(sentences)}, złożone: {len(compound)}")
print(f"PL: {has_pl}, EN: {has_en}")
print(f"Pierwsze 3 zdania:")
for s in sentences[:3]:
    print(f"  {s[:120]}")
