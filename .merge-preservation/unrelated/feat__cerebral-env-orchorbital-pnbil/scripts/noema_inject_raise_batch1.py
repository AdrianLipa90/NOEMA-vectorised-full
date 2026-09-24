#!/usr/bin/env python3
"""Faza 2 quiet-except — batch 1: niskie ryzyko, brak HTTP handlerów.

Pliki: noema_library_loader, noema_audit_consolidator,
       noema_linux_cards_daemon, noema_phase_archiver.

Dry-run domyślnie. APPLY=1 env var żeby zapisać.
"""
from __future__ import annotations
import os, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPLY = os.environ.get("APPLY", "0") == "1"

LOGGER_PAT = re.compile(r'^(\s*)_NOEMA_QUIET_EXCEPT_LOGGER\.exception\(')

TARGET_FILES = [
    "scripts/noema_library_loader.py",
    "scripts/noema_audit_consolidator.py",
    "scripts/noema_linux_cards_daemon.py",
    "scripts/noema_phase_archiver.py",
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
        # Sprawdź czy następna niepusta linia to już raise
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        next_s = lines[j].strip() if j < len(lines) else ""
        if next_s == "raise":
            continue
        injections.append(i)
        indent = m.group(1)
        print(f"  L{i+1:4d}: {line.rstrip()[:80]}")
        print(f"         → insert: {indent}raise")

    if injections and APPLY:
        for idx in reversed(injections):
            indent = LOGGER_PAT.match(lines[idx]).group(1)
            lines.insert(idx + 1, f"{indent}raise\n")
        path.write_text("".join(lines), encoding="utf-8")
        print(f"  ZAPISANO: {rel} (+{len(injections)} raise)")

    return {"path": rel, "injected": len(injections), "applied": APPLY and bool(injections)}


total = 0
for rel in TARGET_FILES:
    print(f"\n=== {rel} ===")
    r = process_file(rel)
    total += r["injected"]

mode = "APPLY" if APPLY else "DRY-RUN"
print(f"\n{mode}: {total} raise łącznie w {len(TARGET_FILES)} plikach")
print("Aby zastosować: APPLY=1 python3 noema_inject_raise_batch1.py")
