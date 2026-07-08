"""cielingo_core.timing — phase snapshots, timing control, phased-state models."""
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


try:
    from ciel_sot_agent.phased_state import (
        ALPHA,
        BETA,
        B0,
        FileState,
        build_states,
        compute_phase,
        compute_raw_energy,
        frac64,
        normalize,
        relational_relevance,
        sha256_seed,
        weight_layer,
        weight_type,
    )
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/cielingo_core/timing/__init__.py:19 quiet except scope=<module> reason=no_log_no_raise")
    ALPHA = 0.18
    BETA = 0.12
    B0 = 1024.0
    FileState = None
    build_states = None
    compute_phase = None
    compute_raw_energy = None
    frac64 = None
    normalize = None
    relational_relevance = None
    sha256_seed = None
    weight_layer = None
    weight_type = None


class PhaseSnapshot:
    def __init__(self, phase: float = 0.0, label: str = ""):
        self.phase = phase
        self.label = label

    def as_dict(self) -> dict:
        return {"phase": self.phase, "label": self.label}


class TimingController:
    def __init__(self, base_frequency_hz: float = 7.83):
        self.base_frequency_hz = base_frequency_hz
        self._cycle = 0

    def tick(self) -> int:
        self._cycle += 1
        return self._cycle

    def reset(self) -> None:
        self._cycle = 0

    @property
    def cycle(self) -> int:
        return self._cycle


__all__ = [
    "ALPHA", "BETA", "B0", "FileState",
    "build_states", "compute_phase", "compute_raw_energy",
    "frac64", "normalize", "relational_relevance",
    "sha256_seed", "weight_layer", "weight_type",
    "PhaseSnapshot", "TimingController",
]
