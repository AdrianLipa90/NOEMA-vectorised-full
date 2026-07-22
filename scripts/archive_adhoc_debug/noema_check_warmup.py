#!/usr/bin/env python3
"""Journal od 15:05:12 — szukaj odpowiedzi na 'test' z hooka."""
import subprocess
r = subprocess.run(
    ["journalctl", "--user", "-u", "noema-headless.service",
     "--since", "15:05:12", "--no-pager"],
    capture_output=True, text=True
)
print(r.stdout[-5000:])
