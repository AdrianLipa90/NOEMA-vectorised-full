#!/usr/bin/env python3
"""Restart daemonów po raise injection — przez MCP bridge."""
import json, socket, sys
from pathlib import Path

NOEMA_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(NOEMA_ROOT / "src"))

# Daemony które zmodyfikowaliśmy
DAEMONS = [
    "noema-linux-cards",
    "noema-phase-archiver",
    "noema-orchestrator",
    "noema-subconscious",
    "noema-trigger",
    "noema-proc-watch",
    "noema-journal",
    "noema-actuator",
    "noema-sentinel",
    "noema-cielingo",
    "noema-surface-refresh",
    "noema-portal",
    "noema-hub",
]

# Używamy MCP bridge przez stdio
import subprocess, os

env = os.environ.copy()
env["NOEMA_ROOT"] = str(NOEMA_ROOT)

for daemon in DAEMONS:
    req = json.dumps({
        "jsonrpc": "2.0",
        "method": "noema_daemon_restart",
        "params": {"daemon": daemon},
        "id": 1
    })
    try:
        result = subprocess.run(
            ["python3", "-c", f"""
import sys, json
sys.path.insert(0, '{NOEMA_ROOT}/src')
# Spróbuj MCP bridge
try:
    import subprocess as sp
    r = sp.run(['systemctl', '--user', 'restart', '{daemon}.service'],
               capture_output=True, text=True, timeout=10)
    print(json.dumps({{"daemon": "{daemon}", "ok": r.returncode==0, "msg": r.stderr.strip()}}))
except Exception as e:
    print(json.dumps({{"daemon": "{daemon}", "ok": False, "msg": str(e)}}))
"""],
            capture_output=True, text=True, timeout=15, env=env
        )
        out = result.stdout.strip()
        if out:
            data = json.loads(out)
            print(f"{'OK' if data['ok'] else 'ERR'} {data['daemon']}: {data.get('msg', '')[:60]}")
        else:
            print(f"NO_OUTPUT {daemon}: {result.stderr.strip()[:60]}")
    except Exception as e:
        print(f"EXCEPT {daemon}: {e}")
