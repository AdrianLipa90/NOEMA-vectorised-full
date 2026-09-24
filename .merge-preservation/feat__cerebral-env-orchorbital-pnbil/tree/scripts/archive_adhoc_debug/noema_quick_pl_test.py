#!/usr/bin/env python3
"""Szybki test bez czekania — próbuj socket i zgłoś stan."""
import socket as _socket, json, time
from pathlib import Path

SOCK = Path("/media/adrian/New Volume/CIEL_memories/run/ciel_headless.sock")
LOG = Path("/media/adrian/New Volume/CIEL_memories/logs/ciel_headless.jsonl")
TEXT = "Czym jest system NOEMA i jak działa architektura CIELingo z PhaseMemory?"

# Sprawdz log
lines = LOG.read_text(errors="replace").splitlines()
loaded = [l for l in lines[-20:] if "PhaseMemory loaded" in l or "Shutting down" in l or "starting" in l.lower()]
print(f"Ostatnie logi daemona:")
for l in loaded:
    print(f"  {l}")

# Sprawdz socket
print(f"\nSocket istnieje: {SOCK.exists()}")

if not SOCK.exists():
    print("BLAD: socket nie istnieje, daemon nie startuje!")
    exit(1)

# Probuj polaczenie
try:
    payload = json.dumps({"text": TEXT, "context": {}}).encode()
    s = _socket.socket(_socket.AF_UNIX, _socket.SOCK_STREAM)
    s.settimeout(25)
    s.connect(str(SOCK))
    s.sendall(payload + b"\n")
    buf = b""
    t0 = time.time()
    while time.time() - t0 < 25:
        try:
            chunk = s.recv(4096)
        except _socket.timeout:
            break
        if not chunk:
            break
        buf += chunk
        try:
            data = json.loads(buf.decode())
            break
        except json.JSONDecodeError:
            pass
    s.close()

    if not buf:
        print("BLAD: brak odpowiedzi (timeout lub puste)")
    else:
        try:
            data = json.loads(buf.decode())
        except Exception:
            data = {"raw": buf.decode()[:200]}

        if "error" in data:
            print(f"BLAD daemona: {data['error']}")
        else:
            response = data.get("response") or data.get("text") or ""
            print(f"\nOdpowiedz ({len(response)} znakow):")
            print(response[:600])

            pl = ["Ponadto", "Warto dodać", "Jednocześnie", "Pamiętam", "Co więcej", "Równocześnie"]
            en = ["Furthermore", "It is worth adding", "I remember that", "At the same time"]
            pl_f = [c for c in pl if c in response]
            en_f = [c for c in en if c in response]
            print(f"\nPL laczniki: {pl_f}")
            print(f"EN laczniki: {en_f}")

            import re
            sentences = [s for s in re.split(r'(?<=[.!?])\s+', response.strip()) if len(s) > 10]
            cm = ["który","która","które","że","ponieważ","jednak","natomiast","aby","kiedy","jeśli","bo","więc","ale"]
            compound = [s for s in sentences if any(m in s.lower() for m in cm)]
            print(f"Zdan: {len(sentences)}, zlozonych: {len(compound)}")
            print(f"STATUS: {'OK' if len(sentences)>=15 and len(compound)>=13 else 'za malo'} | jezyk: {'PL' if pl_f and not en_f else 'EN' if en_f and not pl_f else 'mix/brak'}")

except Exception as e:
    print(f"Wyjatek: {e}")
