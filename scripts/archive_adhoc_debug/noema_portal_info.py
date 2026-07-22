#!/usr/bin/env python3
"""Info o portalu — port, endpointy, status."""
import logging, subprocess, json, sys
from pathlib import Path

_log = logging.getLogger(__name__)

# Sprawdź na jakim porcie słucha portal
r = subprocess.run(
    ["ss", "-tlnp"],
    capture_output=True, text=True
)
lines = [l for l in r.stdout.split("\n") if "python" in l or "portal" in l.lower()]
print("=== portal ports (ss) ===")
for l in lines:
    print(l)

# Sprawdź plik serwisu żeby zobaczyć port
svc = Path("/home/adrian/.config/systemd/user/noema-portal.service")
if svc.exists():
    print("\n=== noema-portal.service ===")
    print(svc.read_text()[:800])

# Spróbuj połączyć z portalem na popularnych portach
import socket
for port in [8080, 8081, 8765, 5000, 9000, 9001, 9485, 8500]:
    try:
        s = socket.socket()
        s.settimeout(0.3)
        s.connect(("127.0.0.1", port))
        s.close()
        print(f"  PORT {port}: OPEN")
    except Exception as exc:
        _log.debug("port %s closed: %s", port, exc)
