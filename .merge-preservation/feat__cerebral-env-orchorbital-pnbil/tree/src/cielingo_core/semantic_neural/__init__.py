"""cielingo_core.semantic_neural — semantic encoder and Collatz routing."""
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


try:
    from cielingo.semantic_encoder import (
        CIELingoSemanticEncoder,
        EncoderResult,
        SECTOR_NAMES,
        encode,
        get_encoder,
    )
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/cielingo_core/semantic_neural/__init__.py:11 quiet except scope=<module> reason=no_log_no_raise")
    CIELingoSemanticEncoder = None
    EncoderResult = None
    SECTOR_NAMES = ()
    encode = None
    get_encoder = None

try:
    from cielingo.semantic_collatz import (
        CollatzSemanticStep,
        semantic_collatz_route,
        semantic_seed,
        route_summary,
    )
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/cielingo_core/semantic_neural/__init__.py:25 quiet except scope=<module> reason=no_log_no_raise")
    CollatzSemanticStep = None
    semantic_collatz_route = None
    semantic_seed = None
    route_summary = None


__all__ = [
    "CIELingoSemanticEncoder", "EncoderResult", "SECTOR_NAMES",
    "encode", "get_encoder",
    "CollatzSemanticStep", "semantic_collatz_route",
    "semantic_seed", "route_summary",
]
