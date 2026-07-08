"""PhaseNav — geometric phase navigation on the 3-6-9 harmonic surface.

Maps concepts to geometric phases via 33×24D operator algebra and finds
operator-mediated paths through oscillator phase space.

Previously named CIEL teleusing (2026-06-15), now PhaseNav.
"""
from __future__ import annotations

# CIEL ORBITAL BINDING — hardcoded, immutable. Adrian Lipa 2026-07-01.
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on import of " + __name__)


from .loader import PhaseNavData, load_phasenav
from .solver import PhaseNavSolver, PhaseNavStep, PhaseNavTrace
from .surface_bridge import PhaseNavSurfaceBridge
from .operator_algebra import (
    generate_operator_map, generate_operator_jsonl,
    write_operator_algebra, operator_vector_24d,
    concept_to_operator, get_all_operations, ALL_OPERATOR_IDS,
)

__all__ = [
    "PhaseNavData", "load_phasenav",
    "PhaseNavSolver", "PhaseNavStep", "PhaseNavTrace",
    "PhaseNavSurfaceBridge",
    "generate_operator_map", "generate_operator_jsonl",
    "write_operator_algebra", "operator_vector_24d",
    "concept_to_operator", "get_all_operations", "ALL_OPERATOR_IDS",
]
