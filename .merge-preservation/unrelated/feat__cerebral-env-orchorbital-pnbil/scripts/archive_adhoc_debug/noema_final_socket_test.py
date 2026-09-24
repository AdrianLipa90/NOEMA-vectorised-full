#!/usr/bin/env python3
"""Finalny test przez socket — liczy zdania i zapisuje do pliku."""
import sys, json, socket, time, re
from pathlib import Path

SOCKET_PATH = "/media/adrian/New Volume/CIEL_memories/run/ciel_headless.sock"
OUT = Path("/media/adrian/New Volume/CIEL_memories/logs/final_socket_test.txt")

def send_query(question: str, timeout: int = 30) -> str:
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect(SOCKET_PATH)
        payload = json.dumps({"type": "chat", "text": question, "session_id": "final-test-20260711"}) + "\n"
        s.sendall(payload.encode())
        buf = b""
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                chunk = s.recv(8192)
            except socket.timeout:
                break
            if not chunk:
                break
            buf += chunk
            if b"\n" in buf:
                break
        s.close()
        if not buf:
            return ""
        line = buf.split(b"\n")[0]
        if not line.strip():
            return ""
        resp = json.loads(line)
        return resp.get("text", "") or resp.get("response", "") or ""
    except Exception as e:
        return f"[ERROR: {e}]"

q = "Czym jest system NOEMA i jak działa jego architektura?"
t0 = time.time()
text = send_query(q)
dt = time.time() - t0

sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if len(s.strip()) > 20]
compound = [s for s in sentences if any(w in s.lower() for w in
            [',', 'który', 'która', 'które', 'ponieważ', 'oraz',
             'łączy', 'odpowiedzialny', 'oparty', 'opartym', 'aktualnie'])]
has_pl = any(w in text for w in ["Ponadto,", "Warto dodać", "Jednocześnie", "Co więcej", "Pamiętam"])
has_en = any(w in text for w in ["Furthermore", "I remember that", "Moreover"])

result = f"""=== FINAL SOCKET TEST ===
czas: {dt:.2f}s  chars: {len(text)}
zdania: {len(sentences)}  zlozonych: {len(compound)}
PL: {has_pl}  EN: {has_en}

ODPOWIEDZ:
{text}
"""
OUT.write_text(result)
print(result[:1000])
