#!/usr/bin/env python3
"""Probe CIELInferenceSurface — jakie metody/pipeline ma do dyspozycji."""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OMEGA_ROOT = REPO_ROOT / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM" / "ciel_omega"
for p in (str(REPO_ROOT), str(OMEGA_ROOT)):
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from ciel_inference_surface import CIELInferenceSurface, CIELOrchestrator  # type: ignore
    surf = CIELInferenceSurface()
    orch = CIELOrchestrator()

    print("=== CIELInferenceSurface methods ===")
    for name in dir(surf):
        if not name.startswith("__"):
            print(f"  {name}")

    print("\n=== CIELOrchestrator methods ===")
    for name in dir(orch):
        if not name.startswith("__"):
            print(f"  {name}")

    # Spróbuj wywołać inferencję na przykładowym pytaniu
    print("\n=== Test infer('Czym jest holonomia fazowa?') ===")
    for method in ("infer", "answer", "process", "run", "step", "query"):
        if hasattr(surf, method):
            try:
                result = getattr(surf, method)("Czym jest holonomia fazowa?")
                print(f"  surf.{method}() → {str(result)[:300]}")
            except Exception as e:
                print(f"  surf.{method}() ERROR: {e}")

except Exception as e:
    print(f"Import error: {e}")
    import traceback; traceback.print_exc()
