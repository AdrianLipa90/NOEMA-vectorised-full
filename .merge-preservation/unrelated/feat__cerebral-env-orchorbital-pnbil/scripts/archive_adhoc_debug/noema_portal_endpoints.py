#!/usr/bin/env python3
"""Pokaż endpointy portalu i sprawdź chat."""
import subprocess, json

# Sprawdź jakie endpointy ma portal
r = subprocess.run(
    ["grep", "-n", "def do_\|path.*==\|path.*startswith\|/api\|/chat\|headless\|SOCK",
     "/home/adrian/noema/scripts/noema_portal_daemon.py"],
    capture_output=True, text=True
)
print("=== PORTAL ENDPOINTS ===")
print(r.stdout[:2000])

# Wyślij testowy chat request do portalu
import socket as _s
import time
try:
    s = _s.socket(_s.AF_INET, _s.SOCK_STREAM)
    s.settimeout(5.0)
    s.connect(("127.0.0.1", 18888))
    req = (
        "POST /api/chat HTTP/1.1\r\n"
        "Host: localhost:18888\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: 24\r\n"
        "Connection: close\r\n"
        "\r\n"
        '{"message":"test ping"}'
    )
    s.sendall(req.encode())
    resp = b""
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            chunk = s.recv(4096)
            if not chunk:
                break
            resp += chunk
        except _s.timeout:
            break
    s.close()
    print("\n=== /api/chat RESPONSE ===")
    print(resp[:1000].decode(errors="replace"))
except Exception as e:
    print(f"\n/api/chat ERROR: {e}")
