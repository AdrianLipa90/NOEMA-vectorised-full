#!/usr/bin/env python3
"""Sprawdź status wszystkich noema-*.service demonów."""
import subprocess, json

result = subprocess.run(
    ["systemctl", "--user", "list-units", "--type=service", "--all",
     "--output=json", "--no-pager"],
    capture_output=True, text=True
)

units = []
try:
    units = json.loads(result.stdout)
except Exception:
    # fallback: plain text
    for line in result.stdout.splitlines():
        if "noema-" in line or "ciel" in line.lower():
            print(line)
    raise SystemExit(0)

noema_units = [u for u in units if "noema-" in u.get("unit", "") or "ciel" in u.get("unit", "").lower()]
inactive = [u for u in noema_units if u.get("active") != "active"]
active = [u for u in noema_units if u.get("active") == "active"]

print(f"=== ACTIVE ({len(active)}) ===")
for u in sorted(active, key=lambda x: x["unit"]):
    print(f"  {u['unit']}: {u.get('sub','?')}")

print(f"\n=== INACTIVE/FAILED ({len(inactive)}) ===")
for u in sorted(inactive, key=lambda x: x["unit"]):
    print(f"  {u['unit']}: active={u.get('active','?')} sub={u.get('sub','?')}")
