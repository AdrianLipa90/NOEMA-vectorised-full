#!/usr/bin/env python3
"""Sprawdź status llama-server port 18520 + inne porty LLM."""
import urllib.request, json, socket

PORTS = {
    18520: "llama-server (main)",
    11434: "ollama",
    8080: "llama.cpp default",
}

for port, name in PORTS.items():
    # Najpierw sprawdź czy port w ogóle nasłuchuje
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect(("127.0.0.1", port))
        port_open = True
    except Exception:
        port_open = False
    finally:
        s.close()

    if not port_open:
        print(f"PORT {port} ({name}): ZAMKNIĘTY")
        continue

    # Port otwarty — spróbuj /health
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=3) as r:
            body = json.loads(r.read())
            print(f"PORT {port} ({name}): OK {body}")
    except Exception as e:
        print(f"PORT {port} ({name}): OTWARTY ale /health błąd: {e}")

# Sprawdź też socket CIEL
import sys
from pathlib import Path
sock_path = "/media/adrian/New Volume/CIEL_memories/run/ciel_headless.sock"
if Path(sock_path).exists():
    print(f"\nCIEL socket: ISTNIEJE ({sock_path})")
else:
    print(f"\nCIEL socket: BRAK")
