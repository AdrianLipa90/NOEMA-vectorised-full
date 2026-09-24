#!/usr/bin/env python3
"""Test pełnego pipeline: CIELingo + orchorbital + pn_bil 24D."""
import sys, json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM" / "ciel_omega"))

from ciel_geometry.cielingo_inference import CIELingoInference

ci = CIELingoInference()

tests = [
    "Czym jest holonomia fazowa w CIELingo?",
    "Kim jesteś?",
    "Jak działa synchronizacja Kuramoto?",
]

for q in tests:
    r = ci.answer(q, k=5)
    print(f"\n=== {q} ===")
    print(f"  orchorbital_mode : {r.get('orchorbital_mode', 'n/a')}")
    print(f"  pnbil_vector     : {r.get('pnbil_vector', 'n/a')}")
    orch = r.get('orchorbital_decision')
    if orch:
        print(f"  orch.decision    : {orch.get('decision')}")
        print(f"  orch.score       : {orch.get('association_score'):.3f}")
    print(f"  operator         : {r.get('operator')}")
    print(f"  n_sources        : {r.get('n_sources')}")
    ans = r.get('answer', '')
    # sprawdź czy nie ma pollution
    polluted = any(p in ans for p in ["PhaseNav:", "plikow", "Adrian Lipa, Adrian Lipa"])
    print(f"  answer [{len(ans)}c]    : {ans[:200]!r}")
    print(f"  pollution        : {'FAIL' if polluted else 'OK'}")
