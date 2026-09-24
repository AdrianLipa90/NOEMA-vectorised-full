#!/usr/bin/env python3
"""Find the code that formats PhaseNav search results as the chat reply string."""
import re
from pathlib import Path

ROOTS = [
    Path("/media/adrian/New Volume/"),
]
SKIP_DIRS = {"venv", ".git", "__pycache__", "node_modules"}

PATTERNS = [
    re.compile(r"PhaseNav:\s*\{"),
    re.compile(r"f[\"']PhaseNav:"),
    re.compile(r"plikow\)"),
]

hits = []
for root in ROOTS:
    for path in root.rglob("*.py"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if any(p.search(line) for p in PATTERNS):
                hits.append(f"{path}:{i}: {line.strip()}")

print(f"Found {len(hits)} matches")
for h in hits:
    print(h)
