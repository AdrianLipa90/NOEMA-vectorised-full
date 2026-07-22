#!/usr/bin/env python3
"""Sprawdz ktory plik headless daemon uruchamia i czy lang fix jest w kodzie."""
import subprocess, pathlib

result = subprocess.run(
    ["systemctl", "--user", "show", "noema-headless.service", "--property=ExecStart"],
    capture_output=True, text=True
)
print("ExecStart:", result.stdout.strip())

# Sprawdz ktory plik daemon.py zawiera _user_lang
candidates = [
    pathlib.Path("/home/adrian/noema/scripts/ciel_headless_daemon.py"),
    pathlib.Path("/home/adrian/noema/src/ciel_headless_daemon.py"),
]
for p in candidates:
    if p.exists():
        content = p.read_text()
        has_user_lang = "_user_lang" in content
        has_sim_threshold = "_sim_threshold = -1.0" in content
        print(f"\n{p}:")
        print(f"  _user_lang: {has_user_lang}")
        print(f"  _sim_threshold = -1.0: {has_sim_threshold}")
