"""cielingo_core.meaning — meaning-debt cards, canonization, unknown-word audit."""
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


try:
    from cielingo.meaning_debt_word_cards import (
        CANDIDATE_CONFIDENCE,
        DebtCandidateWordCard,
        DebtWordCardsReport,
        DebtWordRecord,
        build_candidate_card,
        build_candidate_cards,
        generate_debt_word_cards,
        read_debt_index,
    )
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/cielingo_core/meaning/__init__.py:14 quiet except scope=<module> reason=no_log_no_raise")
    CANDIDATE_CONFIDENCE = 0.5
    DebtCandidateWordCard = None
    DebtWordCardsReport = None
    DebtWordRecord = None
    build_candidate_card = None
    build_candidate_cards = None
    generate_debt_word_cards = None
    read_debt_index = None

try:
    from cielingo.canonization_audit import (
        LOW_CONFIDENCE_MAPPING_TYPES,
        TRUSTED_LOCAL_INFINITIVE_MAPPING_TYPES,
        decide_infinitive,
        generate_canonization_audit as build_audit,
        read_jsonl as read_infinitive_candidates,
    )
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/cielingo_core/meaning/__init__.py:33 quiet except scope=<module> reason=no_log_no_raise")
    LOW_CONFIDENCE_MAPPING_TYPES = set()
    TRUSTED_LOCAL_INFINITIVE_MAPPING_TYPES = set()
    decide_infinitive = None
    build_audit = None
    read_infinitive_candidates = None

try:
    from cielingo.unknown_word_audit import (
        UNKNOWN_AUDIT_VERSION,
        UnknownWordAuditEntry as UnknownWordAuditRecord,
        UnknownWordAuditReport,
        audit_unknown_words as build_audit_report,
        classify_unknown_word,
        load_unknown_candidate_cards as load_candidates,
    )
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/cielingo_core/meaning/__init__.py:50 quiet except scope=<module> reason=no_log_no_raise")
    UNKNOWN_AUDIT_VERSION = None
    UnknownWordAuditRecord = None
    UnknownWordAuditReport = None
    build_audit_report = None
    classify_unknown_word = None
    load_candidates = None

try:
    from cielingo.stage0_radical_cards import (
        AlignmentRecord,
        LanguageSlotEntry,
        RadicalCard,
        load_radicals as load_radical_cards,
        load_language_entries as load_slot_entries,
    )
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/cielingo_core/meaning/__init__.py:66 quiet except scope=<module> reason=no_log_no_raise")
    AlignmentRecord = None
    LanguageSlotEntry = None
    RadicalCard = None
    load_radical_cards = None
    load_slot_entries = None


__all__ = [
    "CANDIDATE_CONFIDENCE", "DebtCandidateWordCard", "DebtWordCardsReport",
    "DebtWordRecord", "build_candidate_card", "build_candidate_cards",
    "generate_debt_word_cards", "read_debt_index",
    "LOCAL_CANON_CONFIDENCE_FLOOR",
    "TRUSTED_LOCAL_INFINITIVE_MAPPING_TYPES",
    "audit_report", "build_audit", "read_infinitive_candidates",
    "read_meaning_debt_bundle_report",
    "UNKNOWN_AUDIT_VERSION", "UnknownWordAuditRecord",
    "UnknownWordAuditReport", "build_audit_report",
    "classify_unknown_word", "load_candidates",
    "AlignmentRecord", "LanguageSlotEntry", "RadicalCard",
    "load_radical_cards", "load_slot_entries",
    "export_bundle",
]

import logging as _log
try:
    from cielingo_core.meaning import export_bundle
except Exception as exc:
    _log.getLogger(__name__).debug("meaning: optional module import failed: %s", exc)
