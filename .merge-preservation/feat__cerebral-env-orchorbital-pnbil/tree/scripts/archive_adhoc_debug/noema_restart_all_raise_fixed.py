#!/usr/bin/env python3
"""Restart wszystkich daemonów które dostały raise injection 2026-07-12.

Używa subprocess+systemctl tak jak robi to noema_actuator_daemon.py wewnętrznie.
Uruchamiane przez run_script intent — nie przez raw bash.
"""
from __future__ import annotations
import json, subprocess, sys, time
from pathlib import Path

NOEMA_ROOT = Path(__file__).resolve().parents[1]

DAEMONS = [
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
]

ACTUATOR_LAST = "noema-actuator"

results = []

def restart_one(daemon: str) -> dict:
    target = f"{daemon}.service"
    try:
        r = subprocess.run(
            ["systemctl", "--user", "restart", target],
            capture_output=True, text=True, timeout=20,
        )
        ok = r.returncode == 0
        msg = (r.stderr or r.stdout or "").strip()[:120]
        return {"daemon": daemon, "rc": r.returncode, "ok": ok, "msg": msg}
    except subprocess.TimeoutExpired:
        return {"daemon": daemon, "rc": -1, "ok": False, "msg": "TIMEOUT"}
    except Exception as e:
        return {"daemon": daemon, "rc": -1, "ok": False, "msg": str(e)[:80]}

print(f"Restarting {len(DAEMONS)} daemons (+ actuator last)...", flush=True)

for daemon in DAEMONS:
    res = restart_one(daemon)
    status = "OK " if res["ok"] else f"FAIL rc={res['rc']}"
    print(f"  {status:12} {daemon}: {res['msg']}", flush=True)
    results.append(res)
    time.sleep(0.5)

# Actuator last (it restarts itself — caller won't see result but that's OK)
print(f"\nRestarting {ACTUATOR_LAST} last...", flush=True)
res = restart_one(ACTUATOR_LAST)
print(f"  {'OK' if res['ok'] else 'FAIL'} {ACTUATOR_LAST}: {res['msg']}", flush=True)
results.append(res)

ok_count = sum(1 for r in results if r["ok"])
fail_count = len(results) - ok_count
not_found = [r["daemon"] for r in results if r["rc"] == 5]

print(f"\n=== SUMMARY ===")
print(f"OK:        {ok_count}")
print(f"FAIL:      {fail_count}")
print(f"NOT_FOUND: {len(not_found)} {not_found}")

# Write results to log
log = NOEMA_ROOT / "logs" / "restart_raise_fixed_20260712.json"
log.parent.mkdir(parents=True, exist_ok=True)
log.write_text(json.dumps({"ts": time.time(), "results": results}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"\nLog: {log}", flush=True)
