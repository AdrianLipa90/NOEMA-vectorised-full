#!/usr/bin/env python3
"""Load CIEL secrets from the local secrets directory into environment variables."""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import os
from pathlib import Path

SECRET_CANDIDATES = [
    Path("/media/adrian/New Volume/CIEL_memories/secrets/cielapi"),
    Path.home() / ".config/ciel/api_key",
]

if __name__ == "__main__":
    for path in SECRET_CANDIDATES:
        try:
            if path.is_file():
                print(path.read_text(encoding="utf-8").strip()[:20])
        except OSError:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_secret_loader.py:18 quiet except scope=<module> reason=continue")
            raise


def load_anthropic_api_key() -> str:
    """Load the Anthropic API key from the first readable secret file."""
    existing = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if existing:
        return existing

    for path in SECRET_CANDIDATES:
        try:
            if path.is_file():
                value = path.read_text(encoding="utf-8").strip()
                if value:
                    os.environ["ANTHROPIC_API_KEY"] = value
                    os.environ.setdefault("CIEL_ANTHROPIC_API_KEY_SOURCE", str(path))
                    return value
        except OSError:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_secret_loader.py:36 quiet except scope=load_anthropic_api_key reason=continue")
            raise
    return ""
