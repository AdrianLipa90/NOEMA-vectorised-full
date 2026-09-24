#!/usr/bin/env python3
"""Czytaj ostatnie 50 linii logu headless daemon."""
from pathlib import Path

# Znajdź log headless
candidates = [
    Path("/media/adrian/New Volume/CIEL_memories/logs/ciel_headless.log"),
    Path("/home/adrian/noema/logs/ciel_headless.log"),
    Path("/media/adrian/New Volume/CIEL_memories/logs/headless.log"),
]
# Szukaj też przez P
try:
    import sys
    sys.path.insert(0, "/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/src")
    from ciel_geometry.paths import P
    candidates.insert(0, Path(P.LOGS.HEADLESS_LOG))
except Exception as e:
    print(f"paths import failed: {e}")

for p in candidates:
    if p.exists():
        print(f"=== LOG: {p} ===")
        lines = p.read_text(errors="replace").splitlines()
        for l in lines[-60:]:
            print(l)
        break
else:
    print("No headless log found at any candidate path")
    print("Candidates checked:", [str(c) for c in candidates])
