"""Re-export from PhaseNav — backward compatibility shim.

The canonical metatime contract now lives in ``ciel_geometry.phasenav.metatime_contract``.
This module exists only for callers that have not yet migrated their import.
"""

from ciel_geometry.phasenav.metatime_contract import (
    CONTRACT_SCHEMA as CONTRACT_SCHEMA,
    CONTRACT_VERSION as CONTRACT_VERSION,
    INFORMATION_KAPPA as INFORMATION_KAPPA,
    DerivedScalar as DerivedScalar,
    EpistemicClass as EpistemicClass,
    ExactPhaseMetrics as ExactPhaseMetrics,
    MetatimeContract as MetatimeContract,
    NeutrinoMassAnsatzRatios as NeutrinoMassAnsatzRatios,
    PhaseTauBaseline as PhaseTauBaseline,
    ProvenanceNode as ProvenanceNode,
    ReceiptScope as ReceiptScope,
    RelationalTauSpectrum as RelationalTauSpectrum,
    SourceReceipt as SourceReceipt,
    build_metatime_contract_v1 as build_metatime_contract_v1,
    derive_exact_phase_metrics as derive_exact_phase_metrics,
    normalize_phase as normalize_phase,
    signed_phase_delta as signed_phase_delta,
)

__all__ = [
    "CONTRACT_SCHEMA", "CONTRACT_VERSION", "INFORMATION_KAPPA",
    "DerivedScalar", "EpistemicClass", "ExactPhaseMetrics",
    "MetatimeContract", "NeutrinoMassAnsatzRatios", "PhaseTauBaseline",
    "ProvenanceNode", "ReceiptScope", "RelationalTauSpectrum",
    "SourceReceipt", "build_metatime_contract_v1",
    "derive_exact_phase_metrics", "normalize_phase", "signed_phase_delta",
]
