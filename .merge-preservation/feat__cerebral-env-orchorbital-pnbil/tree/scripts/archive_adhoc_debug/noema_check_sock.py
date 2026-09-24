#!/usr/bin/env python3
"""Sprawdz czy socket istnieje i status daemona."""
import os, pathlib, subprocess

sock = pathlib.Path("/media/adrian/New Volume/CIEL_memories/run/ciel_headless.sock")
print(f"Socket exists: {sock.exists()}")
print(f"Socket dir exists: {sock.parent.exists()}")

# Lista plikow w run/
run_dir = sock.parent
if run_dir.exists():
    files = list(run_dir.iterdir())
    print(f"Files in {run_dir}: {[f.name for f in files]}")

# Sprawdz czy jest jakis inny socket
import sys
sys.path.insert(0, "/home/adrian/noema/src")
from ciel_geometry.paths import P as _P
print(f"HEADLESS_SOCK path: {_P.RUN.HEADLESS_SOCK}")
headless_sock = pathlib.Path(_P.RUN.HEADLESS_SOCK)
print(f"Headless sock exists: {headless_sock.exists()}")
