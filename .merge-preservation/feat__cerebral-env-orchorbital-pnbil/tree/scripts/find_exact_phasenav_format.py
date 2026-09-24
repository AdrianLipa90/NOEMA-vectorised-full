#!/usr/bin/env python3
"""Find the exact 'PhaseNav: X, Y. (N plikow)' format string in JS/HTML/py of the portal."""
import re
from pathlib import Path

ROOTS = [
    Path("/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/runtime"),
    Path("/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/scripts"),
    Path("/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/src"),
]
SKIP_DIRS = {"venv", ".git", "__pycache__", "node_modules"}
EXTS = {".py", ".html", ".js"}

PATTERN = re.compile(r"plikow\)|plikow\"|plikow'")

hits = []
for root in ROOTS:
    for path in root.rglob("*"):
        if path.suffix not in EXTS:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if PATTERN.search(line):
                hits.append(f"{path}:{i}: {line.strip()[:200]}")

print(f"Found {len(hits)} matches")
for h in hits:
    print(h)
