#!/usr/bin/env python3
"""Znajdź gdzie portal trzyma pliki statyczne."""
import subprocess
from pathlib import Path

# Szukaj jak portal serwuje pliki JS (static file serving)
r = subprocess.run(
    ["grep", "-n", "static\|STATIC\|web_root\|WWW\|public\|html_root\|send_response.*200\|path.suffix\|path.endswith",
     "/home/adrian/noema/scripts/noema_portal_daemon.py"],
    capture_output=True, text=True, timeout=10
)
print("=== STATIC SERVING ===")
print(r.stdout[:2000])

# Sprawdź czy istnieje static/ lub web/ w noema root
for d in ["static", "web", "www", "public", "frontend", "html", "ui"]:
    p = Path("/home/adrian/noema") / d
    if p.exists():
        print(f"\nFound dir: {p}")
        print(list(p.iterdir())[:10])

# Znajdź wszystkie .js pliki w noema
r2 = subprocess.run(
    ["find", "/home/adrian/noema", "-name", "*.js", "-not", "-path", "*/node_modules/*",
     "-not", "-path", "*/.venv/*", "-maxdepth", "5"],
    capture_output=True, text=True, timeout=10
)
print("\n=== JS FILES ===")
print(r2.stdout[:1000])
