#!/usr/bin/env python3
"""Test /api/cielingo/chat endpoint portalu."""
import socket as _s, time, json

def portal_request(method: str, path: str, body: str = "") -> str:
    s = _s.socket(_s.AF_INET, _s.SOCK_STREAM)
    s.settimeout(15.0)
    s.connect(("127.0.0.1", 18888))
    body_bytes = body.encode()
    req = (
        f"{method} {path} HTTP/1.1\r\n"
        f"Host: localhost:18888\r\n"
        f"Content-Type: application/json\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    ).encode() + body_bytes
    s.sendall(req)
    resp = b""
    deadline = time.time() + 30
    while time.time() < deadline:
        try:
            chunk = s.recv(4096)
            if not chunk:
                break
            resp += chunk
        except _s.timeout:
            break
    s.close()
    return resp.decode(errors="replace")

# 1. Test /api/cielingo/chat
print("=== POST /api/cielingo/chat ===")
r = portal_request("POST", "/api/cielingo/chat",
                   json.dumps({"message": "ile masz lat?"}))
print(r[:2000])
