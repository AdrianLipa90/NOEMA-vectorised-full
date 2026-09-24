#!/usr/bin/env python3
"""Faza 2 quiet-except remediation — dodaj `raise` po każdym logu.

Zasada: _NOEMA_QUIET_EXCEPT_LOGGER.exception(...) → log → raise.
Kod po logu staje się dead-code (celowo — dokumentuje stare zachowanie).

Dry-run: python3 noema_inject_raise.py
Apply:   python3 noema_inject_raise.py --apply

Raport zapisywany do QUIET_EXCEPT_RAISE_REPORT.json
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = ROOT / "QUIET_EXCEPT_RAISE_REPORT.json"

LOGGER_PAT = re.compile(r'^(\s*)_NOEMA_QUIET_EXCEPT_LOGGER\.exception\(')


def _process_file(path: Path, apply: bool) -> dict:
    try:
        source = path.read_text(encoding="utf-8")
    except Exception as e:
        return {"path": str(path.relative_to(ROOT)), "error": str(e), "injected": 0}

    lines = source.splitlines(keepends=True)
    injections: list[int] = []  # 0-based indices AFTER which to insert raise

    i = 0
    while i < len(lines):
        m = LOGGER_PAT.match(lines[i])
        if m:
            indent = m.group(1)
            raise_line = f"{indent}raise\n"
            # Sprawdź czy następna niepusta linia to już raise
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            next_stripped = lines[j].strip() if j < len(lines) else ""
            if next_stripped != "raise":
                injections.append(i)
        i += 1

    if not injections:
        return {"path": str(path.relative_to(ROOT)), "injected": 0, "changed": False}

    if apply:
        # Wstaw raise od końca żeby indeksy się nie przesuwały
        for idx in reversed(injections):
            indent = LOGGER_PAT.match(lines[idx]).group(1)
            lines.insert(idx + 1, f"{indent}raise\n")
        path.write_text("".join(lines), encoding="utf-8")

    return {
        "path": str(path.relative_to(ROOT)),
        "injected": len(injections),
        "changed": apply,
        "locations": [i + 1 for i in injections],  # 1-based line numbers
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Modyfikuj pliki (bez tego: dry-run)")
    ap.add_argument("--file", help="Ogranicz do jednego pliku (ścieżka względem root)")
    args = ap.parse_args()

    if args.file:
        files = [ROOT / args.file]
    else:
        files = sorted(ROOT.rglob("scripts/**/*.py"))

    results = []
    total_injected = 0
    changed_files = []

    for path in files:
        if not path.exists():
            continue
        # Pomiń sam plik naprawczy
        if path.name in ("noema_inject_raise.py", "noema_quiet_except_repair.py",
                          "noema_quiet_except_audit.py"):
            continue
        result = _process_file(path, args.apply)
        results.append(result)
        n = result.get("injected", 0)
        if n:
            total_injected += n
            changed_files.append(result["path"])
            print(f"  {'APPLY' if args.apply else 'DRY '} {result['path']}: +{n} raise")

    mode = "APPLIED" if args.apply else "DRY-RUN"
    print(f"\n{mode}: {total_injected} raise do wstawienia w {len(changed_files)} plikach")

    report = {
        "mode": mode,
        "total_raise_injected": total_injected,
        "files_affected": len(changed_files),
        "changed_files": changed_files,
        "details": [r for r in results if r.get("injected", 0)],
    }
    REPORT_JSON.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(f"Raport: {REPORT_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
