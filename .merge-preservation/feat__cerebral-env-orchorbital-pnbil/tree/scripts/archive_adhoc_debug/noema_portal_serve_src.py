#!/usr/bin/env python3
"""Znajdź w source portalu skąd serwuje JS."""
import subprocess

# Szukaj w portalu jak serwuje pliki statyczne
r = subprocess.run(
    ["grep", "-n", "js/pages\|static\|serve_file\|send_file\|\.js\|chat.js\|WebSocket\|eventSource\|SSE",
     "/home/adrian/noema/scripts/noema_portal_daemon.py"],
    capture_output=True, text=True, timeout=10
)
print(r.stdout[:3000])
