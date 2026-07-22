#!/usr/bin/env python3
"""Sprawdz ktory plik daemon faktycznie uzywa."""
import subprocess, pathlib

result = subprocess.run(
    ["systemctl", "show", "noema-headless.service", "--property=ExecStart"],
    capture_output=True, text=True
)
print("ExecStart:", result.stdout.strip())

result2 = subprocess.run(
    ["systemctl", "cat", "noema-headless.service"],
    capture_output=True, text=True
)
print("\nService file:", result2.stdout[:2000])
