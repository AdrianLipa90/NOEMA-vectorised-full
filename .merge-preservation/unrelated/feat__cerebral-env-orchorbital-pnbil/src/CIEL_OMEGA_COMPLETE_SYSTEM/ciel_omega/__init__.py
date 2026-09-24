"""CIEL/Ω Quantum Consciousness Suite.

Canonical root exports for the single Omega execution axis.
"""
from __future__ import annotations

# CIEL ORBITAL BINDING — hardcoded, immutable. Adrian Lipa 2026-07-01.
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on import of " + __name__)


__version__ = "2.0.0"
__author__ = "Adrian Lipa / Intention Lab"
__all__ = [
    "CIELOrchestrator",
    "CIELClient",
    "UnifiedSystem",
    "GGUFOverlay",
    "GGUFOverlayReport",
    "__version__",
    "__author__",
]


def __getattr__(name: str):
    if name == "CIELOrchestrator":
        from .ciel_orchestrator import CIELOrchestrator
        return CIELOrchestrator
    if name == "CIELClient":
        from .ciel_client import CIELClient
        return CIELClient
    if name == "UnifiedSystem":
        from .unified_system import UnifiedSystem
        return UnifiedSystem
    if name in {"GGUFOverlay", "GGUFOverlayReport"}:
        from .ciel.gguf_overlay import GGUFOverlay, GGUFOverlayReport

        return GGUFOverlay if name == "GGUFOverlay" else GGUFOverlayReport
    raise AttributeError(f"module 'ciel_omega' has no attribute {name!r}")
