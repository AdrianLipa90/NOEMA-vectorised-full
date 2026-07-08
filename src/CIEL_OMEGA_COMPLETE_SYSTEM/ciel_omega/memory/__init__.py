"""CIEL/Ω Memory Architecture

Phase-based memory system with eight channels (M0-M7) plus audit (M8).
Implements disk-radial model where memories orbit identity attractor.

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
"""

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

from .potential import (
    MemoryPotential,
)

from .dynamics import (
    MemorySystemState,
    MemoryDynamicsEngine,
)

# Holonomy and EBA condition
from .holonomy import (
    MemoryLoop,
    HolonomyCalculator,
    define_standard_loops,
    create_loop_from_trajectory,
    compute_eba_potential_component,
)

# Implemented channels
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
from .working_types import (
    WorkingTrace,
    WorkingItem,
    WorkingSnapshot,
)

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

# Legacy (deprecated but kept for compatibility)
from .long_term import LongTermMemory
from .memory_log import MemoryLog

# Tiered orchestrator (overarching coordinator across all memory tiers)
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


__all__ = [
    # Base infrastructure
    'PhaseState',
    'MemoryChannelParams',
    'CHANNEL_PARAMS',
    'BaseMemoryChannel',
    'IdentityField',
    
    'PerceptualMemory',
    'PerceptualTrace',
    'PerceptualItem',
    'PerceptualSnapshot',

    # Coupling
    'COUPLING_MATRIX',
    'CHANNEL_NAMES',
    'CouplingEngine',
    'print_coupling_summary',
    
    # Potential & Dynamics
    'MemoryPotential',
    'MemorySystemState',
    'MemoryDynamicsEngine',
    
    # Holonomy & EBA
    'MemoryLoop',
    'HolonomyCalculator',
    'define_standard_loops',
    'create_loop_from_trajectory',
    'compute_eba_potential_component',
    
    # Memory Channels
    'BraidInvariantMemory',
    'BraidUnit',
    'EpisodicMemory',
    'Episode',
    'AuditJournalMemory',
    'JournalEntry',
    'IdentityMemory',
    'IdentityTrace',
    'IdentityAnchorCandidate',
    'IdentityMemorySnapshot',
    'IdentityConsolidationScore',
    'SemanticMemory',
    'ProceduralMemory',
    'SemanticTrace',
    'SemanticCandidate',
    'SemanticItem',
    'SemanticConsolidationScore',
    'ProceduralTrace',
    'ProceduralCandidate',
    'ProceduralItem',
    'ProceduralConsolidationScore',
    'WorkingMemory',
    'WorkingTrace',
    'WorkingItem',
    'WorkingSnapshot',
    'HolonomicMemoryOrchestrator',
    'ConsolidationEvents',
    'EBAEvaluation',
    'OrchestratorCycleResult',
    'OrchestratorSnapshot',
    'AffectiveEthicalMemory',
    'AffectiveTrace',
    'AffectiveCandidate',
    'AffectiveItem',
    'AffectiveConsolidationScore',
    'LinguisticCouplingProfile',
    'LinguisticSemanticCoupling',
    'analyze_linguistic_coupling',
    'lexical_semantic_matrix',

    # Legacy
    'LongTermMemory',
    'MemoryLog',

    # Tiered orchestrator
    'TieredMemoryOrchestrator',
    'TieredWriteResult',
    'TieredReadResult',
    'TieredSnapshot',
    'WriteMode',
    'ReadMode',
    'Tier',
    'get_tiered_orchestrator',
    'tiered_write',
    'tiered_read',
    'tiered_snapshot',
    'tiered_health',
    'tiered_consolidate',
    'process_user_input_via_tiers',
]
