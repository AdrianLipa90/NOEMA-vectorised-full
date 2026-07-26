"""Small, side-effect-free secret loader used by NOEMA command scripts.

Secrets are resolved in an explicit order and are never logged:

1. ``ANTHROPIC_API_KEY`` environment variable;
2. the configured ``P.SECRETS.ANTHROPIC`` file;
3. the legacy configured ``P.SECRETS.CIELAPI`` file.

The module returns ``None`` when no key is available. It does not invent a
credential, contact a network service, or write secrets to disk.
"""

from __future__ import annotations

import os
from pathlib import Path

from ciel_geometry.paths import P


def _read_secret(path: str | os.PathLike[str] | None) -> str | None:
    if not path:
        return None
    candidate = Path(path).expanduser()
    try:
        value = candidate.read_text(encoding="utf-8").strip()
    except OSError:
        return None
    return value or None


def load_anthropic_api_key() -> str | None:
    """Return the configured Anthropic key without exposing it in logs."""
    env_value = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if env_value:
        return env_value

    for attribute in ("ANTHROPIC", "CIELAPI"):
        try:
            value = _read_secret(getattr(P.SECRETS, attribute))
        except AttributeError:
            value = None
        if value:
            return value
    return None


__all__ = ["load_anthropic_api_key"]
