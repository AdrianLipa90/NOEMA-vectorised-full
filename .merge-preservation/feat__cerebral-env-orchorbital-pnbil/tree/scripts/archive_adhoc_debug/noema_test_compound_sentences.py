#!/usr/bin/env python3
"""Test: czy Ciel generuje wielozdaniowe odpowiedzi z PhaseMemory."""
import json, socket, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from ciel_geometry.paths import P

QUESTIONS = [
    "Czym jest system NOEMA i jak działa jego architektura?",
    "Opowiedz mi o PhaseNav i fazach w systemie.",
]

sock_path = P.RUN.HEADLESS_SOCK
print(f"Socket: {sock_path}")
print(f"Exists: {Path(sock_path).exists()}\n")

for q in QUESTIONS:
    print(f"PYTANIE: {q}")
    t0 = time.time()
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(60)
    s.connect(sock_path)
    s.sendall(q.encode("utf-8"))
    s.shutdown(socket.SHUT_WR)
    buf = b""
    while True:
        d = s.recv(65536)
        if not d:
            break
        buf += d
    s.close()
    elapsed = time.time() - t0
    result = json.loads(buf.decode("utf-8"))
    response = result.get("response", "???")
    mode = result.get("episodic_mode", result.get("mode", "?"))
    n_mem = len((result.get("knowledge", {}).get("sources") or []))
    print(f"CZAS: {elapsed:.2f}s  |  MODE: {mode}")
    print(f"ODPOWIEDŹ ({len(response)} znaków):")
    print(response)
    # policz zdania
    import re
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', response) if s.strip()]
    print(f"\nLICZBA ZDAŃ: {len(sentences)}")
    print("-" * 60)
