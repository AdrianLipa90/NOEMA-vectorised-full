#!/usr/bin/env python3
"""Restart NOEMA daemons one by one via actuator intent.json protocol.

Run via: run_script intent (this script submits intents AND waits for each result
by polling result.json — safe because it runs synchronously inside the actuator process
and writes a new intent ONLY after the previous result is confirmed).

WARNING: This script writes directly to actuator/intent.json and polls result.json.
It should NOT be run as a run_script intent (deadlock — actuator busy running this).
Run standalone: python3 noema_restart_batch_via_actuator.py
"""
from __future__ import annotations
import json, logging, time
from pathlib import Path

_log = logging.getLogger(__name__)

INTENT = Path("/dev/shm/ciel_noema/actuator/intent.json")
RESULT = Path("/dev/shm/ciel_noema/actuator/result.json")

DAEMONS = [
    "noema-subconscious",
    "noema-trigger",
    "noema-proc-watch",
    "noema-journal",
    "noema-sentinel",
    "noema-cielingo",
    "noema-surface-refresh",
    "noema-watchdog",
    "noema-holonomic-audit",
    "ciel-auto-log",
    "ciel-memory-bind",
    "noema-hibernation",
    "ciel-agent",
    "noema-hub",
    "ciel-memory-consolidator",
    "noema-self-model",
    "noema-checkpoint",
    "ciel-orbital-monitor",
    "ciel-hw-monitor",
    "ciel-coupling",
    "ciel-local",
    "ciel-memory-dump",
    "noema-self-reflect",
    "ciel-noema-phasenav",
    "noema-wavefield-bridge",
    "noema-imaginal-server",
    "ciel-binding-monitor",
    "noema-plan-bridge",
    "noema-agent-lock",
    "noema-dual-sync",
    "noema-voice",
    "noema-sonic",
    "dream-whisper",
    "ciel-monitor",
    "noema-dashboard",
    "ciel-code-learner",
    "ciel-noema-cielingo-sync",
    "noema-portal",
    "cielingo-mcp-server",
    "ciel-agent-backend",
    "ciel-browser-surface",
    "noema-actuator",  # last — restarts the actuator itself
]

results = []
for daemon in DAEMONS:
    intent_id = f"restart-{daemon}-20260712"
    intent = {
        "id": intent_id,
        "intent": "restart_daemon",
        "target": f"{daemon}.service",
        "reason": "raise injection — quiet except fix 2026-07-12",
        "confidence": 1.0,
        "ts": time.time(),
    }
    INTENT.write_text(json.dumps(intent, indent=2), encoding="utf-8")
    print(f">> {daemon}.service ...", flush=True)

    # Poll for result (max 30s)
    deadline = time.time() + 30
    outcome = None
    while time.time() < deadline:
        time.sleep(1.0)
        try:
            r = json.loads(RESULT.read_bytes())
            if r.get("id") == intent_id:
                outcome = r
                break
        except Exception as exc:
            _log.debug("result.json parse failed: %s", exc)

    if outcome is None:
        print(f"   TIMEOUT {daemon}", flush=True)
        results.append({"daemon": daemon, "status": "timeout"})
    else:
        rc = outcome.get("returncode", -1)
        status = "ok" if rc == 0 else "FAIL"
        err = (outcome.get("output") or "").strip()[:80]
        print(f"   {status} rc={rc} {err}", flush=True)
        results.append({"daemon": daemon, "status": status, "rc": rc, "msg": err})

    # Respect rate limit: wait 16s between restarts (2 per 30s)
    time.sleep(16)

print("\n=== SUMMARY ===")
for r in results:
    print(f"{r['status']:6} {r['daemon']}")
