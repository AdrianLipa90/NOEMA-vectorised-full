#!/usr/bin/env python3
"""Faza 2 quiet-except — batch 2: daemony produkcyjne (bez HTTP).

Pliki: noema_orchestrator, ciel_subconscious, noema_proc_watch_daemon,
       noema_journal_daemon, noema_actuator_daemon, noema_trigger_daemon,
       noema_sentinel, ciel_session_hook, ciel_per_message, ciel_response_step,
       ciel_message_step (pierwsze 20 z 28), noema_cielingo_daemon.

APPLY=1 env var żeby zapisać.
"""
from __future__ import annotations
import os, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPLY = os.environ.get("APPLY", "0") == "1"

LOGGER_PAT = re.compile(r'^(\s*)_NOEMA_QUIET_EXCEPT_LOGGER\.exception\(')

TARGET_FILES = [
    "scripts/noema_orchestrator.py",
    "scripts/ciel_subconscious.py",
    "scripts/noema_proc_watch_daemon.py",
    "scripts/noema_journal_daemon.py",
    "scripts/noema_actuator_daemon.py",
    "scripts/noema_trigger_daemon.py",
    "scripts/noema_sentinel.py",
    "scripts/noema_cielingo_daemon.py",
    "scripts/ciel_session_hook.py",
    "scripts/ciel_per_message.py",
    "scripts/ciel_response_step.py",
    "scripts/ciel_message_step.py",
    "scripts/noema_surface_refresh.py",
    "scripts/noema_daemon.py",
    "scripts/noema_watchdog.py",
    "scripts/noema_holonomic_audit.py",
    "scripts/ciel_auto_log_daemon.py",
    "scripts/ciel_memory_bind_daemon.py",
    "scripts/noema_hibernation.py",
    "scripts/ciel_agent_daemon.py",
]


def process_file(rel: str) -> dict:
    path = ROOT / rel
    if not path.exists():
        return {"path": rel, "error": "not found", "injected": 0}

    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    injections: list[int] = []

    for i, line in enumerate(lines):
        m = LOGGER_PAT.match(line)
        if not m:
            continue
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        next_s = lines[j].strip() if j < len(lines) else ""
        if next_s == "raise":
            continue
        injections.append(i)
        indent = m.group(1)
        print(f"  L{i+1:4d}: {line.rstrip()[:80]}")
        if not APPLY:
            print(f"         → insert: {indent}raise")

    if injections and APPLY:
        for idx in reversed(injections):
            indent = LOGGER_PAT.match(lines[idx]).group(1)
            lines.insert(idx + 1, f"{indent}raise\n")
        path.write_text("".join(lines), encoding="utf-8")
        print(f"  ZAPISANO: {rel} (+{len(injections)} raise)")

    return {"path": rel, "injected": len(injections), "applied": APPLY and bool(injections)}


total = 0
changed = 0
for rel in TARGET_FILES:
    r = process_file(rel)
    n = r.get("injected", 0)
    if n:
        print(f"{'APPLY' if APPLY else 'DRY  '} {rel}: +{n}")
        total += n
        if r.get("applied"):
            changed += 1

mode = "APPLY" if APPLY else "DRY-RUN"
print(f"\n{mode}: {total} raise łącznie, {changed if APPLY else '?'} plików zmodyfikowanych")
