#!/usr/bin/env python3
"""Test parse_json() bez dostępu do DB."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import noema_library_loader as ldr

cards = [
    "/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/cards/noema_nonlocal_db/001_DOCTOR.noema.card.json",
    "/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/cards/noema_nonlocal_db/002_PIPELINE_SURFACE.noema.card.json",
    "/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/cards/noema_nonlocal_db/003_HTRI_KURAMOTO_120.noema.card.json",
    "/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/cards/base/noema_nonlocal_db/013_HOLONOMY_MEDIUM.noema.card.json",
]

for c in cards:
    p = Path(c)
    if not p.exists():
        print(f"BRAK: {p.name}")
        continue
    r = ldr.parse_json(p)
    is_raw = r.strip().startswith('{')
    print(f"{'RAW JSON' if is_raw else 'NL OK '} {p.name} ({len(r)} chars)")
    if not is_raw:
        print(f"  → {repr(r[:120])}")
