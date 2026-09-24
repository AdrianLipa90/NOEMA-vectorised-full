#!/usr/bin/env python3
"""Znajdź SITE_ROOT i plik cielingo-chat.js."""
import subprocess
from pathlib import Path

r = subprocess.run(
    ["grep", "-n", "SITE_ROOT",
     "/home/adrian/noema/scripts/noema_portal_daemon.py"],
    capture_output=True, text=True, timeout=10
)
print("=== SITE_ROOT ===")
print(r.stdout)

# Też sprawdź journal portalu żeby zobaczyć SITE_ROOT path
r2 = subprocess.run(
    ["journalctl", "--user", "-u", "noema-portal.service",
     "--no-pager", "-n", "50", "--output=short"],
    capture_output=True, text=True
)
lines = [l for l in r2.stdout.split("\n") if "serving" in l.lower() or "SITE" in l or "static" in l.lower() or "Error" in l or "error" in l.lower()]
print("\n=== JOURNAL (static/serving) ===")
for l in lines[:20]:
    print(l)
