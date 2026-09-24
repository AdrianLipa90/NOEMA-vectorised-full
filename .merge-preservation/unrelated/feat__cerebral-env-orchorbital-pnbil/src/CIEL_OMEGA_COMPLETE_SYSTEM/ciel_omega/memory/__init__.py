"""CIEL/Ω Memory Architecture

Phase-based memory system with eight channels (M0-M7) plus audit (M8).
Implements disk-radial model where memories orbit identity attractor.

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base import (
        PhaseState,
        MemoryChannelParams,
        CHANNEL_PARAMS,
        BaseMemoryChannel,
        IdentityField,
    )
    from .perceptual_memory import PerceptualMemory
    from .perceptual_types import (
        PerceptualTrace,
        PerceptualItem,
        PerceptualSnapshot,
    )
    from .coupling import (
        COUPLING_MATRIX,
        CHANNEL_NAMES,
        CouplingEngine,
        print_coupling_summary,
    )
    from .potential import MemoryPotential
    from .dynamics import MemorySystemState, MemoryDynamicsEngine
    from .holonomy import (
        MemoryLoop,
        HolonomyCalculator,
        define_standard_loops,
        create_loop_from_trajectory,
        compute_eba_potential_component,
    )
    from .braid_invariant import BraidInvariantMemory, BraidUnit
    from .episodic import EpisodicMemory, Episode
    from .audit_journal import AuditJournalMemory, JournalEntry
    from .identity_memory import IdentityMemory
    from .identity_types import (
        IdentityTrace,
        IdentityAnchorCandidate,
        IdentityMemorySnapshot,
        IdentityConsolidationScore,
    )
    from .semantic_memory import SemanticMemory
    from .procedural_memory import ProceduralMemory
    from .working_memory import WorkingMemory
    from .working_types import WorkingTrace, WorkingItem, WorkingSnapshot
    from .orchestrator_types import (
        ConsolidationEvents,
        EBAEvaluation,
        OrchestratorCycleResult,
        OrchestratorSnapshot,
    )
    from .orchestrator import HolonomicMemoryOrchestrator
    from .affective_memory import AffectiveEthicalMemory
    from .affective_types import (
        AffectiveTrace,
        AffectiveCandidate,
        AffectiveItem,
        AffectiveConsolidationScore,
    )
    from .semantic_types import (
        SemanticTrace,
        SemanticCandidate,
        SemanticItem,
        SemanticConsolidationScore,
    )
    from .procedural_types import (
        ProceduralTrace,
        ProceduralCandidate,
        ProceduralItem,
        ProceduralConsolidationScore,
    )
    from .linguistic_coupling import (
        LinguisticCouplingProfile,
        LinguisticSemanticCoupling,
        analyze_linguistic_coupling,
        lexical_semantic_matrix,
    )
    from .long_term import LongTermMemory
    from .memory_log import MemoryLog
    from .tiered_orchestrator import (
        TieredMemoryOrchestrator,
        TieredWriteResult,
        TieredReadResult,
        TieredSnapshot,
        WriteMode,
        ReadMode,
        Tier,
        get_orchestrator as get_tiered_orchestrator,
        write as tiered_write,
        read as tiered_read,
        snapshot as tiered_snapshot,
        health as tiered_health,
        consolidate as tiered_consolidate,
        process_user_input_via_tiers,
    )

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "PhaseState": (".base", "PhaseState"),
    "MemoryChannelParams": (".base", "MemoryChannelParams"),
    "CHANNEL_PARAMS": (".base", "CHANNEL_PARAMS"),
    "BaseMemoryChannel": (".base", "BaseMemoryChannel"),
    "IdentityField": (".base", "IdentityField"),
    "PerceptualMemory": (".perceptual_memory", "PerceptualMemory"),
    "PerceptualTrace": (".perceptual_types", "PerceptualTrace"),
    "PerceptualItem": (".perceptual_types", "PerceptualItem"),
    "PerceptualSnapshot": (".perceptual_types", "PerceptualSnapshot"),
    "COUPLING_MATRIX": (".coupling", "COUPLING_MATRIX"),
    "CHANNEL_NAMES": (".coupling", "CHANNEL_NAMES"),
    "CouplingEngine": (".coupling", "CouplingEngine"),
    "print_coupling_summary": (".coupling", "print_coupling_summary"),
    "MemoryPotential": (".potential", "MemoryPotential"),
    "MemorySystemState": (".dynamics", "MemorySystemState"),
    "MemoryDynamicsEngine": (".dynamics", "MemoryDynamicsEngine"),
    "MemoryLoop": (".holonomy", "MemoryLoop"),
    "HolonomyCalculator": (".holonomy", "HolonomyCalculator"),
    "define_standard_loops": (".holonomy", "define_standard_loops"),
    "create_loop_from_trajectory": (".holonomy", "create_loop_from_trajectory"),
    "compute_eba_potential_component": (".holonomy", "compute_eba_potential_component"),
    "BraidInvariantMemory": (".braid_invariant", "BraidInvariantMemory"),
    "BraidUnit": (".braid_invariant", "BraidUnit"),
    "EpisodicMemory": (".episodic", "EpisodicMemory"),
    "Episode": (".episodic", "Episode"),
    "AuditJournalMemory": (".audit_journal", "AuditJournalMemory"),
    "JournalEntry": (".audit_journal", "JournalEntry"),
    "IdentityMemory": (".identity_memory", "IdentityMemory"),
    "IdentityTrace": (".identity_types", "IdentityTrace"),
    "IdentityAnchorCandidate": (".identity_types", "IdentityAnchorCandidate"),
    "IdentityMemorySnapshot": (".identity_types", "IdentityMemorySnapshot"),
    "IdentityConsolidationScore": (".identity_types", "IdentityConsolidationScore"),
    "SemanticMemory": (".semantic_memory", "SemanticMemory"),
    "ProceduralMemory": (".procedural_memory", "ProceduralMemory"),
    "WorkingMemory": (".working_memory", "WorkingMemory"),
    "WorkingTrace": (".working_types", "WorkingTrace"),
    "WorkingItem": (".working_types", "WorkingItem"),
    "WorkingSnapshot": (".working_types", "WorkingSnapshot"),
    "ConsolidationEvents": (".orchestrator_types", "ConsolidationEvents"),
    "EBAEvaluation": (".orchestrator_types", "EBAEvaluation"),
    "OrchestratorCycleResult": (".orchestrator_types", "OrchestratorCycleResult"),
    "OrchestratorSnapshot": (".orchestrator_types", "OrchestratorSnapshot"),
    "HolonomicMemoryOrchestrator": (".orchestrator", "HolonomicMemoryOrchestrator"),
    "AffectiveEthicalMemory": (".affective_memory", "AffectiveEthicalMemory"),
    "AffectiveTrace": (".affective_types", "AffectiveTrace"),
    "AffectiveCandidate": (".affective_types", "AffectiveCandidate"),
    "AffectiveItem": (".affective_types", "AffectiveItem"),
    "AffectiveConsolidationScore": (".affective_types", "AffectiveConsolidationScore"),
    "SemanticTrace": (".semantic_types", "SemanticTrace"),
    "SemanticCandidate": (".semantic_types", "SemanticCandidate"),
    "SemanticItem": (".semantic_types", "SemanticItem"),
    "SemanticConsolidationScore": (".semantic_types", "SemanticConsolidationScore"),
    "ProceduralTrace": (".procedural_types", "ProceduralTrace"),
    "ProceduralCandidate": (".procedural_types", "ProceduralCandidate"),
    "ProceduralItem": (".procedural_types", "ProceduralItem"),
    "ProceduralConsolidationScore": (".procedural_types", "ProceduralConsolidationScore"),
    "LinguisticCouplingProfile": (".linguistic_coupling", "LinguisticCouplingProfile"),
    "LinguisticSemanticCoupling": (".linguistic_coupling", "LinguisticSemanticCoupling"),
    "analyze_linguistic_coupling": (".linguistic_coupling", "analyze_linguistic_coupling"),
    "lexical_semantic_matrix": (".linguistic_coupling", "lexical_semantic_matrix"),
    "LongTermMemory": (".long_term", "LongTermMemory"),
    "MemoryLog": (".memory_log", "MemoryLog"),
    "TieredMemoryOrchestrator": (".tiered_orchestrator", "TieredMemoryOrchestrator"),
    "TieredWriteResult": (".tiered_orchestrator", "TieredWriteResult"),
    "TieredReadResult": (".tiered_orchestrator", "TieredReadResult"),
    "TieredSnapshot": (".tiered_orchestrator", "TieredSnapshot"),
    "WriteMode": (".tiered_orchestrator", "WriteMode"),
    "ReadMode": (".tiered_orchestrator", "ReadMode"),
    "Tier": (".tiered_orchestrator", "Tier"),
    "get_tiered_orchestrator": (".tiered_orchestrator", "get_orchestrator"),
    "tiered_write": (".tiered_orchestrator", "write"),
    "tiered_read": (".tiered_orchestrator", "read"),
    "tiered_snapshot": (".tiered_orchestrator", "snapshot"),
    "tiered_health": (".tiered_orchestrator", "health"),
    "tiered_consolidate": (".tiered_orchestrator", "consolidate"),
    "process_user_input_via_tiers": (".tiered_orchestrator", "process_user_input_via_tiers"),
}


def __getattr__(name: str):
    if name in _LAZY_IMPORTS:
        mod_path, attr = _LAZY_IMPORTS[name]
        import importlib
        mod = importlib.import_module(mod_path, package=__name__)
        val = getattr(mod, attr)
        globals()[name] = val
        return val
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = list(_LAZY_IMPORTS.keys())
