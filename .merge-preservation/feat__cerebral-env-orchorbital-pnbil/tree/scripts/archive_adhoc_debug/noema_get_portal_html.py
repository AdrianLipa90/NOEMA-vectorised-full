#!/usr/bin/env python3
"""Pobierz HTML portalu i szukaj chat input / send button."""
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
    # Tylko body (po \r\n\r\n)
    body = resp.split(b"\r\n\r\n", 1)
    return body[1].decode(errors="replace") if len(body) > 1 else resp.decode(errors="replace")

html = get("/")
print(f"HTML length: {len(html)} chars")

# Szukaj chat-related kodu
lines = html.split("\n")
chat_lines = [l.strip() for l in lines
              if any(k in l.lower() for k in
                     ["chat", "send", "message", "input", "cielingo", "submit", "fetch", "post", "websocket"])]
print(f"\n=== CHAT-RELATED LINES ({len(chat_lines)}) ===")
for l in chat_lines[:40]:
    print(l[:160])
