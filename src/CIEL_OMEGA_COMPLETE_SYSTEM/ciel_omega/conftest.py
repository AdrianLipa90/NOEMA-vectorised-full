"""Ensure the repository root is importable during tests."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent.parent  # NOEMA/
# CIEL_OMEGA_COMPLETE_SYSTEM/ wystarczy — ciel_omega znajdzie się przez __init__.py.
# Nie dodajemy ROOT (ciel_omega/), bo to tworzy ambiguous module spec (namespace vs regular package).
for p in [str(ROOT.parent), str(REPO / "src"), str(REPO / "integration" / "Orbital" / "main")]:
    if p not in sys.path:
        sys.path.insert(0, p)
