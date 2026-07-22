#!/usr/bin/env python3
import subprocess, json

# Lista wszystkich user services żeby znaleźć cielingo
r = subprocess.run(
    ["systemctl", "--user", "list-units", "--type=service", "--all", "--no-pager", "--plain"],
    capture_output=True, text=True
)
lines = r.stdout.strip().split("\n")
ciel = [l for l in lines if "ciel" in l.lower() or "cielingo" in l.lower()]
print("=== CIEL services ===")
for l in ciel:
    print(l)

print("\n=== ALL noema services ===")
noema = [l for l in lines if "noema" in l.lower()]
for l in noema:
    print(l)
