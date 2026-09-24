#!/usr/bin/env python3
"""Faza 2 quiet-except — batch 3: ciel_hub_daemon i inne nie-HTTP.

APPLY=1 env var żeby zapisać.
"""
from __future__ import annotations
import os, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPLY = os.environ.get("APPLY", "0") == "1"
LOGGER_PAT = re.compile(r'^(\s*)_NOEMA_QUIET_EXCEPT_LOGGER\.exception\(')

TARGET_FILES = [
    "scripts/ciel_hub_daemon.py",
    "scripts/ciel_memory_consolidator.py",
    "scripts/ciel_memory_stop.py",
    "scripts/build_file_wij.py",
    "scripts/noema_self_model.py",
    "scripts/noema_checkpoint.py",
    "scripts/ciel_orbital_monitor.py",
    "scripts/ciel_hw_monitor.py",
    "scripts/ciel_coupling.py",
    "scripts/ciel_local.py",
    "scripts/ciel_memory_dump.py",
    "scripts/noema_self_reflect.py",
    "scripts/ciel_noema_phasenav_daemon.py",
    "scripts/noema_wavefield_bridge.py",
    "scripts/noema_imaginal_server.py",
    "scripts/ciel_binding_monitor.py",
    "scripts/noema_plan_bridge.py",
    "scripts/noema_agent_lock.py",
    "scripts/noema_dual_sync.py",
    "scripts/noema_voice_daemon.py",
    "scripts/noema_sonic_daemon.py",
    "scripts/dream_whisper.py",
    "scripts/ciel_monitor.py",
    "scripts/noema_dashboard.py",
    "scripts/ciel_code_learner.py",
    "scripts/opencode_raw_sessions_to_cielingo.py",
    "scripts/ingest_memory_files.py",
    "scripts/cielingo_canonization_pipeline.py",
    "scripts/ciel_noema_cielingo_sync.py",
    "scripts/noema_quiet_except_audit.py",
    "scripts/codex_bridge_to_ciel.py",
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
        if (lines[j].strip() if j < len(lines) else "") == "raise":
            continue
        injections.append(i)
    if injections and APPLY:
        for idx in reversed(injections):
            indent = LOGGER_PAT.match(lines[idx]).group(1)
            lines.insert(idx + 1, f"{indent}raise\n")
        path.write_text("".join(lines), encoding="utf-8")
    return {"path": rel, "injected": len(injections), "applied": APPLY and bool(injections)}


total = 0
changed = 0
for rel in TARGET_FILES:
    r = process_file(rel)
    n = r.get("injected", 0)
    if n:
        mode = "APPLY" if APPLY else "DRY  "
        print(f"{mode} {rel}: +{n}")
        total += n
        if r.get("applied"):
            changed += 1
    elif "error" in r:
        print(f"SKIP  {rel}: {r['error']}")

mode = "APPLY" if APPLY else "DRY-RUN"
print(f"\n{mode}: {total} raise łącznie, {changed if APPLY else total} plików")
