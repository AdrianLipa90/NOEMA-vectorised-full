"""cielingo_core.bridge — HTRI phase bus, brain map, Collatz sync, orbital router.

CIEL ORBITAL BINDING — hardcoded przy imporcie.
"""
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

from pathlib import Path

_CIEL_BINDING_PATH = Path("/dev/shm/ciel_noema") / "ciel_binding_status"
if not (_CIEL_BINDING_PATH.exists() and _CIEL_BINDING_PATH.read_text().strip() == "ACTIVE"):
    import warnings
    warnings.warn("CIEL ORBITAL BINDING: not ACTIVE — bridge imported in degraded mode")

try:
    from cielingo.htri_phase_bus import (
        KAPPA_INFO,
        PhaseBusNode,
        PhaseBusReport,
        bind_card_to_phase_bus,
        phase_bus_report,
        select_phase_bus_cards,
    )
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/cielingo_core/bridge/__init__.py:21 quiet except scope=<module> reason=no_log_no_raise")
    KAPPA_INFO = None
    PhaseBusNode = None
    PhaseBusReport = None
    bind_card_to_phase_bus = None
    phase_bus_report = None
    select_phase_bus_cards = None

try:
    from cielingo.htri_brain_map import (
        BRAIN_BY_ID,
        BRAIN_MAP,
        BrainOscillator,
        DOMAINS,
        brain_phase_topology,
        oscillator_for_card,
    )
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/cielingo_core/bridge/__init__.py:38 quiet except scope=<module> reason=no_log_no_raise")
    BRAIN_BY_ID = {}
    BRAIN_MAP = ()
    BrainOscillator = None
    DOMAINS = ()
    brain_phase_topology = None
    oscillator_for_card = None

try:
    from cielingo.collatz_semantic_htri_sync import (
        BASE_FREQUENCY_HZ,
        CardSyncState,
        DEFAULT_OSCILLATORS,
        synchronize_card,
        synchronization_report,
    )
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/cielingo_core/bridge/__init__.py:54 quiet except scope=<module> reason=no_log_no_raise")
    BASE_FREQUENCY_HZ = 7.83
    CardSyncState = None
    DEFAULT_OSCILLATORS = 24
    synchronize_card = None
    synchronization_report = None

try:
    from cielingo.orchorbital_router import (
        OrchORbitalDecision,
        route_orchorbital,
    )
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/cielingo_core/bridge/__init__.py:66 quiet except scope=<module> reason=no_log_no_raise")
    OrchORbitalDecision = None
    route_orchorbital = None

try:
    from ciel_sot_agent.orbital_bridge import build_orbital_bridge as _build_orbital_bridge
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/cielingo_core/bridge/__init__.py:72 quiet except scope=<module> reason=assign_fallback")
    _build_orbital_bridge = None


def build_orbital_bridge(root: str, encoder_phase: float | None = None) -> dict:
    if _build_orbital_bridge is None:
        raise ImportError("ciel_sot_agent.orbital_bridge not available")
    return _build_orbital_bridge(root, encoder_phase=encoder_phase)


__all__ = [
    "KAPPA_INFO", "PhaseBusNode", "PhaseBusReport",
    "bind_card_to_phase_bus", "phase_bus_report", "select_phase_bus_cards",
    "BRAIN_BY_ID", "BRAIN_MAP", "BrainOscillator", "DOMAINS",
    "brain_phase_topology", "oscillator_for_card",
    "BASE_FREQUENCY_HZ", "CardSyncState", "DEFAULT_OSCILLATORS",
    "synchronize_card", "synchronization_report",
    "OrchORbitalDecision", "route_orchorbital",
    "build_orbital_bridge",
]
