"""CIELingo GLOBAL coordination with lazy runtime boundaries.

Importing a pure GLOBAL contract must not boot the CIEL runtime, resolve host
memory paths, or require optional numerical dependencies. Runtime bridges are
therefore imported only when their exported wrappers are called.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
import warnings


_BINDING_STATUS = Path("/dev/shm/ciel_noema/ciel_binding_status")
if not (_BINDING_STATUS.exists() and _BINDING_STATUS.read_text().strip() == "ACTIVE"):
    warnings.warn("CIEL ORBITAL BINDING: not ACTIVE on import of " + __name__)


def build_lingo_frame(text: str, **kwargs: Any) -> dict:
    """Call the optional runtime bridge without importing it at package load."""
    try:
        from ciel_sot_agent.cielingo_bridge import build_lingo_frame as implementation
    except ImportError as exc:
        raise ImportError("ciel_sot_agent.cielingo_bridge not available") from exc
    return implementation(text, **kwargs)


def run_ciel_pipeline(
    orbital_state: dict,
    context: str = "global_layer",
    *,
    root: str = ".",
) -> dict:
    """Call the optional CIEL runtime only when pipeline execution is requested."""
    try:
        from ciel_sot_agent.ciel_pipeline import run_ciel_pipeline as implementation
    except ImportError as exc:
        raise ImportError("ciel_sot_agent.ciel_pipeline not available") from exc
    return implementation(orbital_state, context=context, root=root)


class GlobalLayer:
    def __init__(self, root: str = "."):
        self.root = root
        self._state: dict = {}

    def run_pipeline(self, orbital_state: dict, context: str = "global_layer") -> dict:
        return run_ciel_pipeline(orbital_state, context=context, root=self.root)

    def build_frame(self, text: str, **kwargs: Any) -> dict:
        return build_lingo_frame(text, **kwargs)

    def status(self) -> dict:
        return {
            "root": self.root,
            "pipeline_available": True,
            "lingo_bridge_available": True,
            "runtime_import_mode": "lazy",
        }


__all__ = [
    "GlobalLayer",
    "build_lingo_frame",
    "run_ciel_pipeline",
]
