#!/usr/bin/env python3
"""Probe CIELInferenceSurface.process() — co zwraca, czy orchorbital jest w pipeline."""
import sys, json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OMEGA_ROOT = REPO_ROOT / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM" / "ciel_omega"
for p in (str(REPO_ROOT), str(OMEGA_ROOT)):
    if p not in sys.path:
        sys.path.insert(0, p)

# Czytaj kod process() bez instancjowania
import importlib.util, inspect
spec = importlib.util.spec_from_file_location(
    "ciel_inference_surface",
    OMEGA_ROOT / "ciel_inference_surface.py"
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

surf_cls = mod.CIELInferenceSurface
orch_cls = mod.CIELOrchestrator

print("=== CIELInferenceSurface.process source ===")
print(inspect.getsource(surf_cls.process))

print("\n=== CIELInferenceSurface.__init__ source ===")
print(inspect.getsource(surf_cls.__init__))
