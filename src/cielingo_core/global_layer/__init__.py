"""cielingo_core.global_layer — system-level coordination and CIEL pipeline."""
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)



# CIEL ORBITAL BINDING — hardcoded, immutable. Adrian Lipa 2026-07-01.
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on import of " + __name__)
try:
    from ciel_sot_agent.cielingo_bridge import build_lingo_frame
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/cielingo_core/global_layer/__init__.py:11 quiet except scope=<module> reason=assign_fallback")
    build_lingo_frame = None

try:
    from ciel_sot_agent.ciel_pipeline import run_ciel_pipeline
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/cielingo_core/global_layer/__init__.py:16 quiet except scope=<module> reason=assign_fallback")
    run_ciel_pipeline = None


class GlobalLayer:
    def __init__(self, root: str = "."):
        self.root = root
        self._state: dict = {}

    def run_pipeline(self, orbital_state: dict, context: str = "global_layer") -> dict:
        if run_ciel_pipeline is None:
            raise ImportError("ciel_sot_agent.ciel_pipeline not available")
        return run_ciel_pipeline(orbital_state, context=context, root=self.root)

    def build_frame(self, text: str, **kwargs) -> dict:
        if build_lingo_frame is None:
            raise ImportError("ciel_sot_agent.cielingo_bridge not available")
        return build_lingo_frame(text, **kwargs)

    def status(self) -> dict:
        return {
            "root": self.root,
            "pipeline_available": run_ciel_pipeline is not None,
            "lingo_bridge_available": build_lingo_frame is not None,
        }


__all__ = [
    "GlobalLayer",
    "build_lingo_frame",
    "run_ciel_pipeline",
]
