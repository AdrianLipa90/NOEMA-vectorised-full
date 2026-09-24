#!/usr/bin/env python3
"""Probe CIELInferenceSurface — tylko inspect, bez instancji."""
import sys, inspect
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OMEGA_ROOT = REPO_ROOT / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM" / "ciel_omega"
for p in (str(REPO_ROOT), str(OMEGA_ROOT)):
    if p not in sys.path:
        sys.path.insert(0, p)

import importlib.util
spec = importlib.util.spec_from_file_location(
    "ciel_inference_surface",
    OMEGA_ROOT / "ciel_inference_surface.py"
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

for name, obj in inspect.getmembers(mod, inspect.isclass):
    print(f"\n=== class {name} ===")
    for mname, mobj in inspect.getmembers(obj, predicate=inspect.isfunction):
        sig = str(inspect.signature(mobj))[:120]
        print(f"  def {mname}{sig}")
    # pokaż docstring
    if obj.__doc__:
        print(f"  doc: {obj.__doc__[:200]}")
