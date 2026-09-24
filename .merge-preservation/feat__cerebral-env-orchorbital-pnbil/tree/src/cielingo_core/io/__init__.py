"""cielingo_core.io — web fetching, RSS, utility I/O."""
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


try:
    from cielingo.web_fetcher import (
        FetchResult,
        RSS_FEEDS,
        fetch as _fetch,
        fetch_news,
    )
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/cielingo_core/io/__init__.py:10 quiet except scope=<module> reason=no_log_no_raise")
    FetchResult = None
    RSS_FEEDS = {}
    _fetch = None
    fetch_news = None


def fetch_text(url: str, *, timeout: int = 15, cache: bool = True) -> str | None:
    if _fetch is None:
        raise ImportError("cielingo.web_fetcher not available")
    result = _fetch(url, timeout=timeout, cache=cache)
    return result.text if result and result.text else None


import logging as _log
try:
    from cielingo_core.io import jsonl
except Exception as exc:
    _log.getLogger(__name__).debug("io: optional module import failed: %s", exc)

__all__ = [
    "FetchResult", "RSS_FEEDS", "fetch_text", "fetch_news",
    "jsonl",
]
