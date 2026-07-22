#!/usr/bin/env python3
"""Znajdź rzeczywistą ścieżkę socket headless i co daemon ma otwarte."""
import subprocess, os, pathlib

# Znajdź noema_paths przez grep w noema/src
r = subprocess.run(
    ["grep", "-r", "HEADLESS_SOCK", "/home/adrian/noema/src/", "--include=*.py", "-l"],
    capture_output=True, text=True, timeout=10
)
print("=== HEADLESS_SOCK files ===")
print(r.stdout[:300])

# Pokaż gdzie jest HEADLESS_SOCK zdefiniowane
r2 = subprocess.run(
    ["grep", "-r", "HEADLESS_SOCK", "/home/adrian/noema/src/", "--include=*.py"],
    capture_output=True, text=True, timeout=10
)
print("\n=== HEADLESS_SOCK definitions ===")
print(r2.stdout[:800])

# Sprawdź otwarte pliki procesu 1658427
try:
    r3 = subprocess.run(
        ["ls", "-la", f"/proc/1658427/fd/"],
        capture_output=True, text=True, timeout=5
    )
    socks = [l for l in r3.stdout.split("\n") if "socket" in l.lower() or ".sock" in l.lower()]
    print("\n=== proc/1658427 sockets ===")
    for s in socks[:20]:
        print(s)
except Exception as e:
    print(f"proc error: {e}")

# Sprawdź przez ss/netstat
r4 = subprocess.run(
    ["ss", "-x", "-p"],
    capture_output=True, text=True, timeout=5
)
headless = [l for l in r4.stdout.split("\n") if "headless" in l.lower() or "1658427" in l]
print("\n=== ss unix sockets with 'headless' or pid 1658427 ===")
for l in headless[:20]:
    print(l)
