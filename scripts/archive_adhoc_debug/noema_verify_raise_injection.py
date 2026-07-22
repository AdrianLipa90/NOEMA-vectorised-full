#!/usr/bin/env python3
"""Weryfikacja: policz _NOEMA_QUIET_EXCEPT_LOGGER bez raise po sobie."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOGGER_PAT = re.compile(r'^(\s*)_NOEMA_QUIET_EXCEPT_LOGGER\.exception\(')

missing = []
fixed = 0

for path in sorted((ROOT / "scripts").rglob("*.py")):
    try:
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    except Exception:
        continue
    for i, line in enumerate(lines):
        if not LOGGER_PAT.match(line):
            continue
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        next_s = lines[j].strip() if j < len(lines) else ""
        if next_s == "raise":
            fixed += 1
        else:
            rel = str(path.relative_to(ROOT))
            missing.append(f"  {rel}:{i+1} → {next_s[:50]!r}")

print(f"Z raise: {fixed}")
print(f"Bez raise: {len(missing)}")
if missing:
    print("\nBrakujące (pierwsze 20):")
    for m in missing[:20]:
        print(m)
