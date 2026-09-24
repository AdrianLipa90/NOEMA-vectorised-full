#!/usr/bin/env python3
"""Czekaj na PhaseMemory, potem testuj polskie łączniki."""
import socket, json, time
from pathlib import Path

SOCK = Path("/media/adrian/New Volume/CIEL_memories/run/ciel_headless.sock")
LOG = Path("/media/adrian/New Volume/CIEL_memories/logs/ciel_headless.jsonl")
TEXT = "Czym jest system NOEMA i jak działa architektura CIELingo z PhaseMemory?"

# Czekaj na PhaseMemory loaded
print("Czekam na PhaseMemory loaded...")
for i in range(60):
    time.sleep(1)
    lines = LOG.read_text(errors="replace").splitlines()
    recent = [l for l in lines[-10:] if "PhaseMemory loaded" in l]
    if recent:
        print(f"OK: {recent[-1]}")
        break
else:
    print("TIMEOUT: PhaseMemory nie zaladowala w 60s")

time.sleep(2)  # dodatkowy margines

# Test socket
def query(text):
    payload = json.dumps({"text": text, "context": {}}).encode()
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(30)
    s.connect(str(SOCK))
    s.sendall(payload + b"\n")
    buf = b""
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        buf += chunk
        try:
            data = json.loads(buf.decode())
            break
        except json.JSONDecodeError:
            pass
    s.close()
    return data

print(f"\nQuery: {TEXT}")
result = query(TEXT)

if "error" in result:
    print(f"BLAD: {result['error']}")
else:
    response = result.get("response") or result.get("text") or ""
    print(f"Odpowiedz ({len(response)} znakow):")
    print(response[:500])

    # Sprawdz laczniki
    pl_connectors = ["Ponadto", "Warto dodać", "Jednocześnie", "Pamiętam", "W kontekście"]
    en_connectors = ["Furthermore", "It is worth adding", "I remember that", "At the same time"]
    pl_found = [c for c in pl_connectors if c in response]
    en_found = [c for c in en_connectors if c in response]
    print(f"\nPL laczniki: {pl_found}")
    print(f"EN laczniki: {en_found}")
    print(f"Jezyk: {'POLSKI' if pl_found and not en_found else 'ANGIELSKI' if en_found and not pl_found else 'MIESZANY' if pl_found and en_found else 'BRAK LACZNIKOW'}")

    # Policz zdania
    import re
    sentences = re.split(r'(?<=[.!?])\s+', response.strip())
    sentences = [s for s in sentences if len(s) > 10]
    complex_markers = ["który", "która", "które", "którą", "którym", "których", "że", "ponieważ",
                       "gdyż", "jednak", "natomiast", "chociaż", "aby", "żeby", "kiedy", "gdy",
                       "jeśli", "jeżeli", "bo", "więc", "lecz", "ale", "gdyby"]
    compound = [s for s in sentences if any(m in s.lower() for m in complex_markers)]
    print(f"\nZdan lacznie: {len(sentences)}")
    print(f"Zdan zlozonych: {len(compound)}")
    print(f"CEL: {'OSIAGNIETY >=15 zdan, >=13 zlozonych' if len(sentences) >= 15 and len(compound) >= 13 else 'NIE OSIAGNIETY'}")
