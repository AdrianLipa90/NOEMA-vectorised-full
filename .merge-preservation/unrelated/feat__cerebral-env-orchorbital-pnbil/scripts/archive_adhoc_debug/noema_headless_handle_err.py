#!/usr/bin/env python3
"""Pobierz linie logu od 14:53:00 żeby zobaczyć pełny traceback _handle."""
import subprocess
r = subprocess.run(
    ["journalctl", "--user", "-u", "noema-headless.service",
     "--since", "14:53:00", "--no-pager"],
    capture_output=True, text=True
)
print(r.stdout[:6000])
