"""PhaseNav — geometric phase navigation on the 3-6-9 harmonic surface.

Maps concepts to geometric phases via 33×24D operator algebra and finds
operator-mediated paths through oscillator phase space.

Previously named CIEL teleusing (2026-06-15), now PhaseNav.

Lazy imports — nothing heavy happens at ``import ciel_geometry.phasenav``.
"""
from __future__ import annotations

# CIEL ORBITAL BINDING — hardcoded, immutable. Adrian Lipa 2026-07-01.
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on import of " + __name__)


from importlib import import_module

_EXPORTS: dict[str, tuple[str, str]] = {
    "PhaseNavData": ("ciel_geometry.phasenav.loader", "PhaseNavData"),
    "load_phasenav": ("ciel_geometry.phasenav.loader", "load_phasenav"),
    "PhaseNavSolver": ("ciel_geometry.phasenav.solver", "PhaseNavSolver"),
    "PhaseNavStep": ("ciel_geometry.phasenav.solver", "PhaseNavStep"),
    "PhaseNavTrace": ("ciel_geometry.phasenav.solver", "PhaseNavTrace"),
    "PhaseNavSurfaceBridge": ("ciel_geometry.phasenav.surface_bridge", "PhaseNavSurfaceBridge"),
    "generate_operator_map": ("ciel_geometry.phasenav.operator_algebra", "generate_operator_map"),
    "generate_operator_jsonl": ("ciel_geometry.phasenav.operator_algebra", "generate_operator_jsonl"),
    "write_operator_algebra": ("ciel_geometry.phasenav.operator_algebra", "write_operator_algebra"),
    "operator_vector_24d": ("ciel_geometry.phasenav.operator_algebra", "operator_vector_24d"),
    "concept_to_operator": ("ciel_geometry.phasenav.operator_algebra", "concept_to_operator"),
    "get_all_operations": ("ciel_geometry.phasenav.operator_algebra", "get_all_operations"),
    "ALL_OPERATOR_IDS": ("ciel_geometry.phasenav.operator_algebra", "ALL_OPERATOR_IDS"),
    "CONTRACT_SCHEMA": ("ciel_geometry.phasenav.metatime_contract", "CONTRACT_SCHEMA"),
    "CONTRACT_VERSION": ("ciel_geometry.phasenav.metatime_contract", "CONTRACT_VERSION"),
    "INFORMATION_KAPPA": ("ciel_geometry.phasenav.metatime_contract", "INFORMATION_KAPPA"),
    "DerivedScalar": ("ciel_geometry.phasenav.metatime_contract", "DerivedScalar"),
    "EpistemicClass": ("ciel_geometry.phasenav.metatime_contract", "EpistemicClass"),
    "ExactPhaseMetrics": ("ciel_geometry.phasenav.metatime_contract", "ExactPhaseMetrics"),
    "MetatimeContract": ("ciel_geometry.phasenav.metatime_contract", "MetatimeContract"),
    "NeutrinoMassAnsatzRatios": ("ciel_geometry.phasenav.metatime_contract", "NeutrinoMassAnsatzRatios"),
    "PhaseTauBaseline": ("ciel_geometry.phasenav.metatime_contract", "PhaseTauBaseline"),
    "ProvenanceNode": ("ciel_geometry.phasenav.metatime_contract", "ProvenanceNode"),
    "ReceiptScope": ("ciel_geometry.phasenav.metatime_contract", "ReceiptScope"),
    "RelationalTauSpectrum": ("ciel_geometry.phasenav.metatime_contract", "RelationalTauSpectrum"),
    "SourceReceipt": ("ciel_geometry.phasenav.metatime_contract", "SourceReceipt"),
    "build_metatime_contract_v1": ("ciel_geometry.phasenav.metatime_contract", "build_metatime_contract_v1"),
    "derive_exact_phase_metrics": ("ciel_geometry.phasenav.metatime_contract", "derive_exact_phase_metrics"),
    "normalize_phase": ("ciel_geometry.phasenav.metatime_contract", "normalize_phase"),
    "signed_phase_delta": ("ciel_geometry.phasenav.metatime_contract", "signed_phase_delta"),
    "BlochState": ("ciel_geometry.phasenav.context_dynamics", "BlochState"),
    "DynamicsReport": ("ciel_geometry.phasenav.context_dynamics", "DynamicsReport"),
    "SemanticHamiltonian": ("ciel_geometry.phasenav.context_dynamics", "SemanticHamiltonian"),
    "StableReductionGate": ("ciel_geometry.phasenav.context_dynamics", "StableReductionGate"),
    "TrajectoryMemory": ("ciel_geometry.phasenav.context_dynamics", "TrajectoryMemory"),
    "FormalismEdge": ("ciel_geometry.phasenav.formalism_logic", "FormalismEdge"),
    "FormalismGraph": ("ciel_geometry.phasenav.formalism_logic", "FormalismGraph"),
    "FormalismNode": ("ciel_geometry.phasenav.formalism_logic", "FormalismNode"),
    "PhaseLogicEngine": ("ciel_geometry.phasenav.formalism_logic", "PhaseLogicEngine"),
    "PhaseLogicReport": ("ciel_geometry.phasenav.formalism_logic", "PhaseLogicReport"),
    "PhaseLogicState": ("ciel_geometry.phasenav.formalism_logic", "PhaseLogicState"),
    "RelationKind": ("ciel_geometry.phasenav.formalism_logic", "RelationKind"),
}

__all__ = list(_EXPORTS.keys())


def __getattr__(name: str):
    if name not in _EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_name, attr_name = _EXPORTS[name]
    value = getattr(import_module(module_name), attr_name)
    globals()[name] = value
    return value
