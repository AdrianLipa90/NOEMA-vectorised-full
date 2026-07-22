"""cielingo_core.lingophysics — tensor-scalar fields, holonomy, potentials, phase parsing."""

from ciel_geometry.phasenav.metatime_contract import INFORMATION_KAPPA


try:
    from cielingo.tensor_scalar_field import (
        AFFECT_CHANNELS,
        SCALAR_CHANNELS,
        TENSOR_AXES,
        TENSOR_SCALAR_SCHEMA,
        TENSOR_SHAPE,
        ContextScalarField,
        TensorScalarReport,
        TensorScalarWordState,
        tensor_scalar_state_from_card,
        tensor_scalar_report,
        write_tensor_scalar_report,
    )
except ImportError:
    AFFECT_CHANNELS = ()
    SCALAR_CHANNELS = ()
    TENSOR_AXES = ()
    TENSOR_SCALAR_SCHEMA = None
    TENSOR_SHAPE = (3, 3)
    ContextScalarField = None
    TensorScalarReport = None
    TensorScalarWordState = None
    tensor_scalar_state_from_card = None
    tensor_scalar_report = None
    write_tensor_scalar_report = None

try:
    from cielingo.lexical_holonomy import (
        LexicalHolonomyEdge,
        LexicalUnit,
        WordKnowledgeNote,
        build_lexical_holonomy_edges,
        build_word_knowledge_notes,
        extract_lexical_units,
        lexical_holonomy_report,
        list_language_card_files,
        read_language_card_file,
        write_lexical_holonomy_report,
    )
except ImportError:
    LexicalHolonomyEdge = None
    LexicalUnit = None
    WordKnowledgeNote = None
    build_lexical_holonomy_edges = None
    build_word_knowledge_notes = None
    extract_lexical_units = None
    lexical_holonomy_report = None
    list_language_card_files = None
    read_language_card_file = None
    write_lexical_holonomy_report = None

try:
    from cielingo.infinitive_modal_potential import (
        EPSILON_R,
        InfinitiveSeed,
        ModalMapping,
        ModalitySeed,
        infinitive_modal_report,
        load_infinitive_seeds,
        load_modality_seeds,
        map_infinitive_to_modalities,
        write_report,
    )
except ImportError:
    EPSILON_R = INFORMATION_KAPPA
    InfinitiveSeed = None
    ModalMapping = None
    ModalitySeed = None
    infinitive_modal_report = None
    load_infinitive_seeds = None
    load_modality_seeds = None
    map_infinitive_to_modalities = None
    write_report = None

try:
    from cielingo.phase_sense_parser import (
        PHASE_SENSE_SCHEMA,
        PhaseSenseReport,
        PhaseSenseToken,
        parse_text_to_phase_sense,
        phase_sense_for_token,
        tokenize_surface,
        write_phase_sense_report,
    )
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/cielingo_core/lingophysics/__init__.py:90 quiet except scope=<module> reason=no_log_no_raise")
    PHASE_SENSE_SCHEMA = None
    PhaseSenseReport = None
    PhaseSenseToken = None
    parse_text_to_phase_sense = None
    phase_sense_for_token = None
    tokenize_surface = None
    write_phase_sense_report = None

try:
    from cielingo.triadic_output_vector import (
        TRIADIC_OUTPUT_SCHEMA,
        TRIAD_LANES,
        TRIAD_VECTOR_DIM,
        OnVivoOutputTestReport,
        TriadicOutputVector,
        on_vivo_output_test,
        vectorize_triadic_output,
        write_output_test_report,
    )
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/cielingo_core/lingophysics/__init__.py:110 quiet except scope=<module> reason=no_log_no_raise")
    TRIADIC_OUTPUT_SCHEMA = None
    TRIAD_LANES = ()
    TRIAD_VECTOR_DIM = 72
    OnVivoOutputTestReport = None
    TriadicOutputVector = None
    on_vivo_output_test = None
    vectorize_triadic_output = None
    write_output_test_report = None

try:
    from cielingo.unresolved_realtime import (
        CANDIDATE_CONFIDENCE,
        CANDIDATE_SCHEMA,
        UNRESOLVED_SCHEMA,
        UnresolvedWordEvent,
        SourceEvidence,
        CandidateWordCard,
        RealtimeUnresolvedReport,
        build_candidate_word_card,
        daily_unresolved_rollup,
        load_source_evidence,
        normalize_word,
        record_realtime_unresolved,
        source_candidates_for_word,
        unresolved_events_from_text,
    )
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/cielingo_core/lingophysics/__init__.py:137 quiet except scope=<module> reason=no_log_no_raise")
    CANDIDATE_CONFIDENCE = 0.5
    CANDIDATE_SCHEMA = None
    UNRESOLVED_SCHEMA = None
    UnresolvedWordEvent = None
    SourceEvidence = None
    CandidateWordCard = None
    RealtimeUnresolvedReport = None
    build_candidate_word_card = None
    daily_unresolved_rollup = None
    load_source_evidence = None
    normalize_word = None
    record_realtime_unresolved = None
    source_candidates_for_word = None
    unresolved_events_from_text = None


__all__ = [
    "AFFECT_CHANNELS", "SCALAR_CHANNELS", "TENSOR_AXES",
    "TENSOR_SCALAR_SCHEMA", "TENSOR_SHAPE",
    "ContextScalarField", "TensorScalarReport", "TensorScalarWordState",
    "tensor_scalar_state_from_card", "tensor_scalar_report",
    "write_tensor_scalar_report",
    "LexicalHolonomyEdge", "LexicalUnit", "WordKnowledgeNote",
    "build_lexical_holonomy_edges", "build_word_knowledge_notes",
    "extract_lexical_units", "lexical_holonomy_report",
    "list_language_card_files", "read_language_card_file",
    "write_lexical_holonomy_report",
    "EPSILON_R", "InfinitiveSeed", "KAPPA_INFO", "ModalMapping",
    "ModalitySeed", "infinitive_modal_report", "load_infinitive_seeds",
    "load_modality_seeds", "map_infinitive_to_modalities", "write_report",
    "PHASE_SENSE_SCHEMA", "PhaseSenseReport", "PhaseSenseToken",
    "parse_text_to_phase_sense", "phase_sense_for_token",
    "tokenize_surface", "write_phase_sense_report",
    "TRIADIC_OUTPUT_SCHEMA", "TRIAD_LANES", "TRIAD_VECTOR_DIM",
    "OnVivoOutputTestReport", "TriadicOutputVector",
    "on_vivo_output_test", "vectorize_triadic_output",
    "write_output_test_report",
    "CANDIDATE_CONFIDENCE", "CANDIDATE_SCHEMA", "UNRESOLVED_SCHEMA",
    "UnresolvedWordEvent", "SourceEvidence", "CandidateWordCard",
    "RealtimeUnresolvedReport", "build_candidate_word_card",
    "daily_unresolved_rollup", "load_source_evidence", "normalize_word",
    "record_realtime_unresolved", "source_candidates_for_word",
    "unresolved_events_from_text",
    "sentence_equation_calculator",
]

import logging as _log
try:
    from cielingo_core.lingophysics import sentence_equation_calculator
except Exception as exc:
    _log.getLogger(__name__).debug("lingophysics: optional module import failed: %s", exc)
