#!/usr/bin/env python3
"""Find where CIELingo Chat web UI formats replies as 'PhaseNav: X, Y. (N plikow)'."""
import re
from pathlib import Path

ROOTS = [
    Path("/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/scripts"),
    Path("/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/runtime"),
    Path("/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/src"),
    Path("/media/adrian/New Volume/CIEL_PROJECT_CANON/CIEL-Omega-ApokalypOS/scripts"),
    Path("/media/adrian/New Volume/CIEL_PROJECT_CANON/CIEL-Omega-ApokalypOS/src/ciel_sot_agent"),
]
SKIP_DIRS = {"venv", ".git", "__pycache__", "node_modules"}
EXTS = {".py", ".html", ".js"}

PATTERNS = [
    re.compile(r"plikow"),
    re.compile(r"query_text"),
    re.compile(r"CIELingo Chat"),
    re.compile(r"hub-\d"),
]

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
            if any(p.search(line) for p in PATTERNS):
                hits.append(f"{path}:{i}: {line.strip()[:160]}")

print(f"Found {len(hits)} matches")
for h in hits:
    print(h)
