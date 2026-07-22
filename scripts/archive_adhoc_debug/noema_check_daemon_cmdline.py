#!/usr/bin/env python3
"""Sprawdz cmdline i kod daemona PID 1408924."""
from pathlib import Path
import json

pid = 1408924

# cmdline
try:
    cmdline = Path(f"/proc/{pid}/cmdline").read_bytes().replace(b'\x00', b' ').decode(errors='replace').strip()
    print(f"PID {pid} cmdline: {cmdline}")
except Exception as e:
    print(f"cmdline error: {e}")

# exe
try:
    import os
    exe = os.readlink(f"/proc/{pid}/exe")
    print(f"PID {pid} exe: {exe}")
except Exception as e:
    print(f"exe error: {e}")

# environ — sprawdz PYTHONPATH
try:
    env = Path(f"/proc/{pid}/environ").read_bytes().split(b'\x00')
    for e in env:
        if b'PYTHON' in e or b'noema' in e.lower() or b'NOEMA' in e:
            print(f"  ENV: {e.decode(errors='replace')}")
except Exception as e:
    print(f"environ error: {e}")

# Sprawdz czy plik skryptu ma _user_lang
for script_path in [
    "/home/adrian/noema/scripts/ciel_headless_daemon.py",
    "/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/scripts/ciel_headless_daemon.py",
]:
    p = Path(script_path)
    if p.exists():
        text = p.read_text(errors='replace')
        print(f"\n{script_path}:")
        print(f"  _user_lang: {'_user_lang' in text}")
        print(f"  _sim_threshold = -1.0: {'_sim_threshold = -1.0' in text}")
        print(f"  min_sim=-1.0: {text.count('min_sim=-1.0')}")
        # Znajdz linię z _user_lang
        for i, line in enumerate(text.splitlines(), 1):
            if '_user_lang' in line:
                print(f"  L{i}: {line.strip()}")
