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
from .cognitive_book_analysis import (
    BookAnalysis,
    ChunkThought,
    ConceptEdge,
    ConceptNode,
    CorpusAnalysis,
    analyze_book_path,
    analyze_corpus,
    analyze_default_corpora,
    default_corpus_specs,
    render_cognitive_book_report,
)
from .berry_phase import BerryPhase, BerryPhaseFrame
from .database_modules import (
    MemoryDatabaseModule,
    MemoryDatabaseSpec,
    build_memory_database_modules,
    default_memory_database_specs,
    discover_memory_database_modules,
    memory_database_catalog,
)
from .layered_memory import (
    LayerTransportEdge,
    LayeredMemorySnapshot,
    LayeredMemorySystem,
    MemoryLayerSnapshot,
)
from .architecture_map import (
    ArchitectureEdge,
    ArchitectureModule,
    ARCHITECTURE_EDGES,
    ARCHITECTURE_MODULES,
    memory_architecture_map,
)
from .legacy_monographs import (
    LEGACY_MONOGRAPHS,
    LegacyMonograph,
    collect_legacy_monographs,
    collect_legacy_reference_glossary,
    legacy_reference_bridge,
)
from .raw_log_pipeline import (
    DEFAULT_AUDIT_LOG,
    DEFAULT_CANON_SINK,
    DEFAULT_OBSERVER_LOG,
    RawLogEntry,
    RawLogSeedPipeline,
    SeedReport,
    build_thought_frame,
    load_raw_log_entries,
    seed_raw_logs,
)
from .sleep_consolidation import (
    DEFAULT_SLEEP_REPORT_ROOT,
    SleepConsolidationReport,
    analyze_sleep_mode_corpus,
    analyze_sleep_mode_default_corpus,
    default_sleep_corpus_paths,
)
from .sleep_scheduler import (
    DEFAULT_SLEEP_SCHEDULER_LOG,
    DEFAULT_SLEEP_SCHEDULER_PID,
    DEFAULT_SLEEP_SCHEDULER_ROOT,
    DEFAULT_SLEEP_SCHEDULER_STATE,
    SleepModeScheduler,
    SleepSchedulerConfig,
    SleepSchedulerCycle,
    build_sleep_scheduler,
)
try:
    from ..core.braid.narrative import (
        BraidNarrativeAssembler,
        BraidNarrativeLedgerJSONL,
        BraidNarrativeSnapshot,
        assemble_braid_narrative,
    )
except Exception:  # pragma: no cover - compatibility for top-level `memory` imports
    from core.braid.narrative import (  # type: ignore[no-redef]
        BraidNarrativeAssembler,
        BraidNarrativeLedgerJSONL,
        BraidNarrativeSnapshot,
        assemble_braid_narrative,
    )

try:
    from ..mathematics.metatime_intention import collect_glossary
except Exception:  # pragma: no cover - compatibility for top-level `memory` imports
    from mathematics.metatime_intention import collect_glossary  # type: ignore[no-redef]

# Legacy (deprecated but kept for compatibility)
from .long_term import LongTermMemory
from .memory_log import MemoryLog


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
    'BookAnalysis',
    'ChunkThought',
    'ConceptEdge',
    'ConceptNode',
    'CorpusAnalysis',
    'analyze_book_path',
    'analyze_corpus',
    'analyze_default_corpora',
    'default_corpus_specs',
    'render_cognitive_book_report',
    'BerryPhase',
    'BerryPhaseFrame',
    'MemoryDatabaseSpec',
    'MemoryDatabaseModule',
    'build_memory_database_modules',
    'default_memory_database_specs',
    'discover_memory_database_modules',
    'memory_database_catalog',
    'MemoryLayerSnapshot',
    'LayerTransportEdge',
    'LayeredMemorySnapshot',
    'LayeredMemorySystem',
    'LEGACY_MONOGRAPHS',
    'LegacyMonograph',
    'ArchitectureEdge',
    'ArchitectureModule',
    'ARCHITECTURE_EDGES',
    'ARCHITECTURE_MODULES',
    'memory_architecture_map',
    'collect_legacy_monographs',
    'collect_legacy_reference_glossary',
    'legacy_reference_bridge',
    'DEFAULT_AUDIT_LOG',
    'DEFAULT_CANON_SINK',
    'DEFAULT_OBSERVER_LOG',
    'RawLogEntry',
    'RawLogSeedPipeline',
    'SeedReport',
    'build_thought_frame',
    'load_raw_log_entries',
    'seed_raw_logs',
    'DEFAULT_SLEEP_REPORT_ROOT',
    'SleepConsolidationReport',
    'default_sleep_corpus_paths',
    'analyze_sleep_mode_corpus',
    'analyze_sleep_mode_default_corpus',
    'DEFAULT_SLEEP_SCHEDULER_ROOT',
    'DEFAULT_SLEEP_SCHEDULER_STATE',
    'DEFAULT_SLEEP_SCHEDULER_PID',
    'DEFAULT_SLEEP_SCHEDULER_LOG',
    'SleepSchedulerConfig',
    'SleepSchedulerCycle',
    'SleepModeScheduler',
    'build_sleep_scheduler',
    'BraidNarrativeAssembler',
    'BraidNarrativeLedgerJSONL',
    'BraidNarrativeSnapshot',
    'assemble_braid_narrative',
    'collect_glossary',

    # Legacy
    'LongTermMemory',
    'MemoryLog',
]
