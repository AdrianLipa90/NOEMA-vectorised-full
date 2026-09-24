"""CIELingo — lingofizyka języka polskiego.

CIEL ORBITAL BINDING — HARDCODED przy każdym imporcie.
"""
from __future__ import annotations
from pathlib import Path

_CIEL_BINDING_PATH = Path("/dev/shm/ciel_noema") / "ciel_binding_status"
if not (_CIEL_BINDING_PATH.exists() and _CIEL_BINDING_PATH.read_text().strip() == "ACTIVE"):
    import warnings
    warnings.warn("CIEL ORBITAL BINDING: not ACTIVE — CIELingo loaded in degraded mode")

__version__ = "0.1.0"

from .card_trace_eeg import CardTrace, CardTraceSnap, create_card_trace_snap, snap_similarity
from .orchorbital_router import OrchORbitalDecision, route_orchorbital
from .semantic_collatz import CollatzSemanticStep, route_summary, semantic_collatz_route, semantic_seed
from .lns_language_cards import (
    LNSLanguageCard,
    language_card_inventory,
    load_all_language_cards,
    load_lns_concept_cards,
    load_lns_operator_cards,
    load_noema_index_language_cards,
    search_language_cards,
)
from .collatz_semantic_htri_sync import CardSyncState, synchronize_card, synchronization_report
from .htri_phase_bus import PhaseBusNode, PhaseBusReport, bind_card_to_phase_bus, phase_bus_report

from .infinitive_modal_potential import (
    InfinitiveSeed,
    ModalitySeed,
    ModalMapping,
    infinitive_modal_report,
    load_infinitive_seeds,
    load_modality_seeds,
    map_infinitive_to_modalities,
)

from .vector_surface import (
    CIELingoVector,
    VectorSurfaceReport,
    VECTOR_COMPONENTS,
    VECTOR_DIM,
    VECTOR_SCHEMA,
    select_vector_cards,
    vector_surface_report,
    vectorize_card,
)

from .lexical_holonomy import (
    LexicalUnit,
    LexicalHolonomyEdge,
    WordKnowledgeNote,
    LanguageCardFileRef,
    extract_lexical_units,
    build_lexical_holonomy_edges,
    build_word_knowledge_notes,
    lexical_holonomy_report,
    list_language_card_files,
    read_language_card_file,
)

from .tensor_scalar_field import (
    ContextScalarField,
    TensorScalarWordState,
    TensorScalarReport,
    tensor_scalar_state_from_card,
    tensor_scalar_report,
)

from .phase_sense_parser import (
    PhaseSenseToken,
    PhaseSenseReport,
    tokenize_surface,
    phase_sense_for_token,
    parse_text_to_phase_sense,
)

from .triadic_output_vector import (
    TriadicOutputVector,
    OnVivoOutputTestReport,
    TRIAD_VECTOR_DIM,
    vectorize_triadic_output,
    on_vivo_output_test,
)


from .unresolved_realtime import (
    UnresolvedWordEvent,
    SourceEvidence,
    CandidateWordCard,
    RealtimeUnresolvedReport,
    load_source_evidence,
    source_candidates_for_word,
    unresolved_events_from_text,
    build_candidate_word_card,
    record_realtime_unresolved,
    daily_unresolved_rollup,
)

from .meaning_debt_word_cards import (
    DebtWordRecord,
    DebtCandidateWordCard,
    DebtWordCardsReport,
    read_debt_index,
    build_candidate_card,
    build_candidate_cards,
    generate_debt_word_cards,
    is_polish_infinitive,
    grammatical_designation,
    semantic_designation,
)

from .canonization_audit import (
    CanonizationDecision,
    decide_infinitive,
    decide_residual_assignment,
    generate_canonization_audit,
)

from .infinitive_merge_audit import (
    InfinitiveCandidate,
    ResidualAssignment,
    OwnedResidualSet,
    infinitivize_word,
    build_infinitive_candidates,
    build_residual_assignments,
    build_owned_residual_sets,
)

from .unknown_word_audit import (
    UnknownWordAuditEntry,
    UnknownCluster,
    UnknownWordAuditReport,
    classify_unknown_word,
    collatz_learning_cycle,
    audit_entry_from_card,
)

from .stage0_radical_cards import (
    RadicalCard,
    LanguageSlotEntry,
    AlignmentRecord,
    load_radicals,
    load_language_entries,
    load_alignments,
    validate_all,
)

__all__ = [
    "CardTrace",
    "CardTraceSnap",
    "create_card_trace_snap",
    "snap_similarity",
    "OrchORbitalDecision",
    "route_orchorbital",
    "CollatzSemanticStep",
    "semantic_seed",
    "semantic_collatz_route",
    "route_summary",
    "LNSLanguageCard",
    "load_lns_concept_cards",
    "load_lns_operator_cards",
    "load_noema_index_language_cards",
    "load_all_language_cards",
    "language_card_inventory",
    "search_language_cards",
    "CardSyncState",
    "synchronize_card",
    "synchronization_report",
    "PhaseBusNode",
    "PhaseBusReport",
    "bind_card_to_phase_bus",
    "phase_bus_report",
    "InfinitiveSeed",
    "ModalitySeed",
    "ModalMapping",
    "load_infinitive_seeds",
    "load_modality_seeds",
    "map_infinitive_to_modalities",
    "infinitive_modal_report",
    "CIELingoVector",
    "VectorSurfaceReport",
    "VECTOR_COMPONENTS",
    "VECTOR_DIM",
    "VECTOR_SCHEMA",
    "select_vector_cards",
    "vector_surface_report",
    "vectorize_card",
    "LexicalUnit",
    "LexicalHolonomyEdge",
    "WordKnowledgeNote",
    "LanguageCardFileRef",
    "extract_lexical_units",
    "build_lexical_holonomy_edges",
    "build_word_knowledge_notes",
    "lexical_holonomy_report",
    "list_language_card_files",
    "read_language_card_file",
    "ContextScalarField",
    "PhaseSenseToken",
    "PhaseSenseReport",
    "tokenize_surface",
    "phase_sense_for_token",
    "parse_text_to_phase_sense",
    "TriadicOutputVector",
    "OnVivoOutputTestReport",
    "TRIAD_VECTOR_DIM",
    "vectorize_triadic_output",
    "on_vivo_output_test",
    "UnresolvedWordEvent",
    "SourceEvidence",
    "CandidateWordCard",
    "RealtimeUnresolvedReport",
    "load_source_evidence",
    "source_candidates_for_word",
    "unresolved_events_from_text",
    "build_candidate_word_card",
    "record_realtime_unresolved",
    "daily_unresolved_rollup",
    "DebtWordRecord",
    "DebtCandidateWordCard",
    "DebtWordCardsReport",
    "read_debt_index",
    "build_candidate_card",
    "build_candidate_cards",
    "generate_debt_word_cards",
    "is_polish_infinitive",
    "grammatical_designation",
    "semantic_designation",
    "CanonizationDecision",
    "decide_infinitive",
    "decide_residual_assignment",
    "generate_canonization_audit",
    "InfinitiveCandidate",
    "ResidualAssignment",
    "OwnedResidualSet",
    "infinitivize_word",
    "build_infinitive_candidates",
    "build_residual_assignments",
    "build_owned_residual_sets",
    "UnknownWordAuditEntry",
    "UnknownCluster",
    "UnknownWordAuditReport",
    "classify_unknown_word",
    "collatz_learning_cycle",
    "audit_entry_from_card",
    "RadicalCard",
    "LanguageSlotEntry",
    "AlignmentRecord",
    "load_radicals",
    "load_language_entries",
    "load_alignments",
    "validate_all",
]
