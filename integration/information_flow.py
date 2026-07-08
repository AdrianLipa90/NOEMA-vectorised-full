"""Compatibility bridge for legacy ``integration.information_flow`` imports.

Canonical implementation lives under:
    src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/integration/information_flow.py

This shim is intentionally thin so local pipeline imports resolve without
duplicating the information-flow memory base.
"""
from __future__ import annotations

from pathlib import Path
import sys

_ROOT = Path(__file__).resolve().parents[1]
_OMEGA_ROOT = _ROOT / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM"
if str(_OMEGA_ROOT) not in sys.path:
    sys.path.insert(0, str(_OMEGA_ROOT))

from ciel_omega.integration.information_flow import InformationFlow

__all__ = ["InformationFlow"]
