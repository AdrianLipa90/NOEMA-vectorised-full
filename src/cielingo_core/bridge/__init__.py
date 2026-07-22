"""cielingo_core.bridge — HTRI phase bus, brain map, Collatz sync, orbital router.

CIEL ORBITAL BINDING — hardcoded przy imporcie.
Wszystkie heavy importy są leniwe (lazy) — import bridge nie ściąga
  `cielingo` (19s), `ciel_geometry` (5s), ani `ciel_sot_agent`.
"""
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

from importlib import import_module
from importlib.util import find_spec
from pathlib import Path

_CIEL_BINDING_PATH = Path("/dev/shm/ciel_noema") / "ciel_binding_status"
if not (_CIEL_BINDING_PATH.exists() and _CIEL_BINDING_PATH.read_text().strip() == "ACTIVE"):
    import warnings
    warnings.warn("CIEL ORBITAL BINDING: not ACTIVE — bridge imported in degraded mode")

_cielingo_exists = find_spec("cielingo") is not None
_ciel_sot_exists = find_spec("ciel_sot_agent") is not None

_EXPORTS: dict[str, tuple[str, str | None, str]] = {
    "KAPPA_INFO": ("ciel_geometry.phasenav.metatime_contract", "INFORMATION_KAPPA", ""),
}

if _cielingo_exists:
    _EXPORTS.update({
        "PhaseBusNode": ("cielingo.htri_phase_bus", "PhaseBusNode", ""),
        "PhaseBusReport": ("cielingo.htri_phase_bus", "PhaseBusReport", ""),
        "bind_card_to_phase_bus": ("cielingo.htri_phase_bus", "bind_card_to_phase_bus", ""),
        "phase_bus_report": ("cielingo.htri_phase_bus", "phase_bus_report", ""),
        "select_phase_bus_cards": ("cielingo.htri_phase_bus", "select_phase_bus_cards", ""),
        "BRAIN_BY_ID": ("cielingo.htri_brain_map", "BRAIN_BY_ID", "{}"),
        "BRAIN_MAP": ("cielingo.htri_brain_map", "BRAIN_MAP", "()"),
        "BrainOscillator": ("cielingo.htri_brain_map", "BrainOscillator", ""),
        "DOMAINS": ("cielingo.htri_brain_map", "DOMAINS", "()"),
        "brain_phase_topology": ("cielingo.htri_brain_map", "brain_phase_topology", ""),
        "oscillator_for_card": ("cielingo.htri_brain_map", "oscillator_for_card", ""),
        "BASE_FREQUENCY_HZ": ("cielingo.collatz_semantic_htri_sync", "BASE_FREQUENCY_HZ", "7.83"),
        "CardSyncState": ("cielingo.collatz_semantic_htri_sync", "CardSyncState", ""),
        "DEFAULT_OSCILLATORS": ("cielingo.collatz_semantic_htri_sync", "DEFAULT_OSCILLATORS", "24"),
        "synchronize_card": ("cielingo.collatz_semantic_htri_sync", "synchronize_card", ""),
        "synchronization_report": ("cielingo.collatz_semantic_htri_sync", "synchronization_report", ""),
        "OrchORbitalDecision": ("cielingo.orchorbital_router", "OrchORbitalDecision", ""),
        "route_orchorbital": ("cielingo.orchorbital_router", "route_orchorbital", ""),
    })
else:
    _EXPORTS.update({
        "PhaseBusNode": ("", "", "None"),
        "PhaseBusReport": ("", "", "None"),
        "bind_card_to_phase_bus": ("", "", "None"),
        "phase_bus_report": ("", "", "None"),
        "select_phase_bus_cards": ("", "", "None"),
        "BRAIN_BY_ID": ("", "", "{}"),
        "BRAIN_MAP": ("", "", "()"),
        "BrainOscillator": ("", "", "None"),
        "DOMAINS": ("", "", "()"),
        "brain_phase_topology": ("", "", "None"),
        "oscillator_for_card": ("", "", "None"),
        "BASE_FREQUENCY_HZ": ("", "", "7.83"),
        "CardSyncState": ("", "", "None"),
        "DEFAULT_OSCILLATORS": ("", "", "24"),
        "synchronize_card": ("", "", "None"),
        "synchronization_report": ("", "", "None"),
        "OrchORbitalDecision": ("", "", "None"),
        "route_orchorbital": ("", "", "None"),
    })

if _ciel_sot_exists:
    _EXPORTS["build_orbital_bridge"] = ("ciel_sot_agent.orbital_bridge", "build_orbital_bridge", "")
else:
    _EXPORTS["build_orbital_bridge"] = ("", "", "None")


from cielingo_core.bridge.phasenav_learning_bridge import (
    PhaseNavLearningBridge,
    phasenav_learn_trace,
    phasenav_enrich_text,
    phasenav_scan_scars,
)

try:
    from cielingo_core.bridge import filesense_boundary, global_filesense_adapter, noema_marker_boundary
    from cielingo_core.bridge import auto_verify, gap_report
except Exception as exc:
    _NOEMA_QUIET_EXCEPT_LOGGER.debug("bridge: optional module import failed: %s", exc)

__all__ = list(_EXPORTS.keys()) + [
    "PhaseNavLearningBridge",
    "phasenav_learn_trace",
    "phasenav_enrich_text",
    "phasenav_scan_scars",
    "filesense_boundary",
    "global_filesense_adapter",
    "noema_marker_boundary",
]


def __getattr__(name: str):
    if name in _EXPORTS:
        module_name, attr_name, fallback_expr = _EXPORTS[name]
        if module_name:
            value = getattr(import_module(module_name), attr_name)
        else:
            value = eval(fallback_expr, {})
        globals()[name] = value
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
