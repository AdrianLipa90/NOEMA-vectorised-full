"""cielingo_core.language_spaces — LNS language cards and Polish linguistic DB."""
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


try:
    from cielingo.lns_language_cards import (
        DEFAULT_LNS_REL,
        LNSLanguageCard,
        load_all_language_cards,
        search_language_cards,
    )
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/cielingo_core/language_spaces/__init__.py:10 quiet except scope=<module> reason=no_log_no_raise")
    DEFAULT_LNS_REL = None
    LNSLanguageCard = None
    load_all_language_cards = None
    search_language_cards = None

try:
    from cielingo.polish.linguistic_database import (
        Lexeme,
        PolishLinguisticDatabase,
        load_polish_database,
    )
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/cielingo_core/language_spaces/__init__.py:22 quiet except scope=<module> reason=no_log_no_raise")
    Lexeme = None
    PolishLinguisticDatabase = None
    load_polish_database = None


__all__ = [
    "DEFAULT_LNS_REL", "LNSLanguageCard",
    "load_all_language_cards", "search_language_cards",
    "Lexeme", "PolishLinguisticDatabase", "load_polish_database",
]
