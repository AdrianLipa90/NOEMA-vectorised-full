#!/usr/bin/env python3
"""Sprawdź czy socket headless istnieje i czy daemon odpowiada."""
from __future__ import annotations
import json, pathlib, socket as _socket, sys, time

sys.path.insert(0, "/home/adrian/noema/src")
sys.path.insert(0, "/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/src")

try:
    from noema_paths import _P
    sock_path = pathlib.Path(_P.RUN.HEADLESS_SOCK)
    fifo_path = pathlib.Path(_P.RUN.HEADLESS_FIFO)
    print(f"HEADLESS_SOCK: {sock_path}")
    print(f"HEADLESS_FIFO: {fifo_path}")
    print(f"sock exists: {sock_path.exists()}")
    print(f"fifo exists: {fifo_path.exists()}")
except Exception as e:
    print(f"ERROR import noema_paths: {e}")
    # Fallback: szukaj .sock
    import subprocess
    r = subprocess.run(["find", "/dev/shm", "/run", "/tmp", "-name", "*.sock", "-maxdepth", "5"],
                       capture_output=True, text=True)
    print("=== .sock files ===")
    print(r.stdout[:500])

# Sprawdź czy socket słucha
try:
    sock_path_try = pathlib.Path("/dev/shm/ciel_noema/ciel_headless.sock")
    if not sock_path_try.exists():
        sock_path_try = pathlib.Path("/tmp/ciel_headless.sock")
    if sock_path_try.exists():
        print(f"\nProba polaczenia z {sock_path_try}...")
        s = _socket.socket(_socket.AF_UNIX, _socket.SOCK_STREAM)
        s.settimeout(3.0)
        s.connect(str(sock_path_try))
        msg = json.dumps({"text": "test ping"}) + "\n"
        s.sendall(msg.encode())
        resp = b""
        try:
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                resp += chunk
        except _socket.timeout:
            pass
        s.close()
        print(f"ODPOWIEDZ ({len(resp)} bytes): {resp[:200]}")
    else:
        print(f"\n{sock_path_try} nie istnieje")
except Exception as e:
    print(f"Connection ERROR: {e}")
