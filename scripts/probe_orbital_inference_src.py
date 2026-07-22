#!/usr/bin/env python3
"""Probe build_orbital_ethical_inference_surface i aux/binary surface."""
import sys, inspect
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OMEGA_ROOT = REPO_ROOT / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM" / "ciel_omega"
for p in (str(REPO_ROOT), str(OMEGA_ROOT)):
    if p not in sys.path:
        sys.path.insert(0, p)

# 1. Źródło build_orbital_ethical_inference_surface
try:
    from inference.topology_api import build_orbital_ethical_inference_surface  # type: ignore
    print("=== build_orbital_ethical_inference_surface source ===")
    print(inspect.getsource(build_orbital_ethical_inference_surface))
except Exception as e:
    print(f"topology_api import error: {e}")

# 2. Co jest w inference/
inf_dir = OMEGA_ROOT / "inference"
print(f"\n=== {inf_dir} contents ===")
if inf_dir.exists():
    for f in sorted(inf_dir.iterdir()):
        print(f"  {f.name}")

# 3. Szukaj aux i binarki
print("\n=== aux directories in CIEL_PROJECT_CANON ===")
for root_check in [
    REPO_ROOT / "aux",
    Path("/media/adrian/New Volume/CIEL_memories/aux"),
    Path("/media/adrian/REPOZYTORIA_GIT1/phasenav-binary-immune-surface-v0.4-gitrepo.zip"),
]:
    exists = root_check.exists()
    print(f"  {root_check}: {'EXISTS' if exists else 'missing'}")
    if exists and root_check.is_dir():
        for f in sorted(root_check.iterdir())[:10]:
            print(f"    {f.name}")

# 4. Sprawdź middleware
try:
    from inference.middleware import CIELMiddleware  # type: ignore
    print("\n=== CIELMiddleware methods ===")
    for name, obj in inspect.getmembers(CIELMiddleware, predicate=inspect.isfunction):
        print(f"  def {name}{str(inspect.signature(obj))[:100]}")
except Exception as e:
    print(f"\nMiddleware error: {e}")
