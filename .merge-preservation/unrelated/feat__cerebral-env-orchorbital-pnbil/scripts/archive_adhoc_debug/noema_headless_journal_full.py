#!/usr/bin/env python3
import subprocess

# Ostatnie 100 linii journal dla headless
r = subprocess.run(
    ["journalctl", "--user", "-u", "noema-headless.service", "-n", "100", "--no-pager"],
    capture_output=True, text=True
)
print(r.stdout[-4000:] if len(r.stdout) > 4000 else r.stdout)
