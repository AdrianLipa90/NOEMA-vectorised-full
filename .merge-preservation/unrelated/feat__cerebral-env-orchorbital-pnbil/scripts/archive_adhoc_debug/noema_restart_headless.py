#!/usr/bin/env python3
"""Restart noema-headless daemon via systemctl --user."""
import subprocess, time, os

result = subprocess.run(
    ["systemctl", "--user", "restart", "noema-headless"],
    capture_output=True, text=True, timeout=15
)
print(f"returncode: {result.returncode}")
print(f"stdout: {result.stdout!r}")
print(f"stderr: {result.stderr!r}")

if result.returncode != 0:
    raise RuntimeError(f"systemctl restart failed: {result.stderr}")

# Czekaj na start
time.sleep(5)
status = subprocess.run(
    ["systemctl", "--user", "is-active", "noema-headless"],
    capture_output=True, text=True, timeout=5
)
print(f"status: {status.stdout.strip()}")
