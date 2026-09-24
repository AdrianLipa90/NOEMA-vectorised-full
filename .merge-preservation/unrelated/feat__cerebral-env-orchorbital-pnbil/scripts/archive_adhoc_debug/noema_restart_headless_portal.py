#!/usr/bin/env python3
"""PhaseNav-native restart: noema-headless + noema-portal.
Operator: ACTION_REQUEST → TRANSFORM (daemon lifecycle gate).
"""
from __future__ import annotations
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.phasenav_exception_bridge import phase_signal_exception

SERVICES = ["noema-headless.service", "noema-portal.service"]

results = {}
for svc in SERVICES:
    try:
        r = subprocess.run(
            ["systemctl", "--user", "restart", svc],
            capture_output=True, text=True, timeout=15,
        )
        results[svc] = {"rc": r.returncode, "out": (r.stdout + r.stderr).strip()}
    except Exception as e:
        phase_signal_exception(f"noema_restart_headless_portal:{svc}", e, operator_id="REFUSAL")
        results[svc] = {"rc": -1, "error": str(e)}

# Daj czas na start
time.sleep(3)

# Weryfikacja socketu
sock = Path("/media/adrian/New Volume/CIEL_memories/run/ciel_headless.sock")
results["socket_exists"] = sock.exists()

for svc, r in results.items():
    print(f"  {svc}: {r}")
