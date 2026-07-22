#!/usr/bin/env python3
"""Test: czy daemon zwraca zdania z polskimi łącznikami."""
import socket, json, time

SOCK = "/media/adrian/New Volume/CIEL_memories/run/ciel_headless.sock"
TEXT = "Czym jest system NOEMA i jak działa architektura CIELingo z PhaseMemory?"

def query(text):
    payload = json.dumps({"text": text, "context": {}}).encode()
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(30)
    s.connect(SOCK)
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

print(f"Pytanie: {TEXT}")
print()
result = query(TEXT)
response = result.get("response") or result.get("text") or str(result)
print(f"Odpowiedź ({len(response)} znaków):")
print(response)
print()

# Sprawdz łączniki
pl_connectors = ["Ponadto", "Warto dodać", "Jednocześnie", "Pamiętam", "W kontekście", "Przede wszystkim", "Co więcej"]
en_connectors = ["Furthermore", "It is worth", "Additionally", "I remember that", "In context"]

pl_found = [c for c in pl_connectors if c in response]
en_found = [c for c in en_connectors if c in response]

print(f"Polskie łączniki znalezione: {pl_found}")
print(f"Angielskie łączniki znalezione: {en_found}")
print()

# Policz zdania
import re
sentences = re.split(r'(?<=[.!?])\s+', response.strip())
sentences = [s for s in sentences if len(s) > 10]
complex_markers = ["który", "która", "które", "którą", "którym", "których", "że", "ponieważ", "gdyż",
                   "jednak", "natomiast", "chociaż", "mimo że", "aby", "żeby", "kiedy", "gdy",
                   "jeśli", "jeżeli", "bo", "więc", "lecz", "ale"]
compound = [s for s in sentences if any(m in s.lower() for m in complex_markers)]
print(f"Zdania łącznie: {len(sentences)}")
print(f"Zdania złożone: {len(compound)}")
print()
for i, s in enumerate(sentences[:15], 1):
    is_c = any(m in s.lower() for m in complex_markers)
    print(f"  [{i}]{'[Z]' if is_c else '[P]'} {s[:120]}")
