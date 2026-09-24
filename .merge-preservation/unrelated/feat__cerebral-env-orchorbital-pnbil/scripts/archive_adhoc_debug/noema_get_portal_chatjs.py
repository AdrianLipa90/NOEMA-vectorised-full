#!/usr/bin/env python3
"""Pobierz cielingo-chat.js z portalu."""
import socket as _s, time

def get(path: str) -> str:
    s = _s.socket(_s.AF_INET, _s.SOCK_STREAM)
    s.settimeout(5.0)
    s.connect(("127.0.0.1", 18888))
    req = f"GET {path} HTTP/1.1\r\nHost: localhost:18888\r\nConnection: close\r\n\r\n"
    s.sendall(req.encode())
    resp = b""
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            chunk = s.recv(8192)
            if not chunk:
                break
            resp += chunk
        except _s.timeout:
            break
    s.close()
    body = resp.split(b"\r\n\r\n", 1)
    return body[1].decode(errors="replace") if len(body) > 1 else resp.decode(errors="replace")

js = get("/js/pages/cielingo-chat.js")
print(f"JS length: {len(js)}")
print(js[:5000])
