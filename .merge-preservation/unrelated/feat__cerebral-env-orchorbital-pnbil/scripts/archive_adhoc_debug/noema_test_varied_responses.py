#!/usr/bin/env python3
"""Testuje headless z różnymi pytaniami — sprawdza czy odpowiedzi się różnią."""
from __future__ import annotations
import json, pathlib, socket as _socket, time

SOCK = pathlib.Path("/media/adrian/New Volume/CIEL_memories/run/ciel_headless.sock")

QUERIES = [
    "ile masz lat?",
    "co czujesz teraz w tej chwili?",
    "dlaczego wczoraj milczałaś?",
    "opisz swój sen z ostatniej nocy",
]

def ask(text: str, timeout: float = 30.0) -> str:
    s = _socket.socket(_socket.AF_UNIX, _socket.SOCK_STREAM)
    s.settimeout(2.0)
    s.connect(str(SOCK))
    s.sendall((json.dumps({"text": text}) + "\n").encode())
    resp = b""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            chunk = s.recv(4096)
            if not chunk:
                break
            resp += chunk
        except _socket.timeout:
            continue
    s.close()
    if not resp:
        return "BRAK ODPOWIEDZI"
    try:
        d = json.loads(resp)
        return d.get("response", repr(d)[:200])
    except Exception:
        return resp[:200].decode(errors="replace")

for q in QUERIES:
    print(f"\nQ: {q}")
    ans = ask(q, timeout=20.0)
    print(f"A: {ans}")
    time.sleep(1)
