#!/usr/bin/env python3
"""Szuka w journalu headless wpisów związanych z chat/response/generate."""
import subprocess

r = subprocess.run(
    ["journalctl", "--user", "-u", "noema-headless.service",
     "-n", "300", "--no-pager", "--output=short"],
    capture_output=True, text=True
)
lines = r.stdout.split("\n")

# Filtruj do linii z kluczowymi słowami
keywords = ["chat", "response", "generat", "answer", "reply", "speak",
            "ERROR", "error", "exception", "Traceback", "raise",
            "queue", "handle", "dispatch", "prompt", "request"]

important = [l for l in lines if any(k.lower() in l.lower() for k in keywords)]
print(f"=== {len(important)} matching lines (of {len(lines)}) ===\n")
for l in important[-60:]:
    print(l)
