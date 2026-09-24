"""NOEMA nonlocal database card layer.

This package treats nonlocality as a NOEMA-surface/proxy/file-packet
semantics layer unless an external Source-of-Truth supplies stronger evidence.
"""
from __future__ import annotations

from .cards import NoemaCard, load_cards, validate_cards, card_registry_digest

__all__ = ["NoemaCard", "load_cards", "validate_cards", "card_registry_digest"]
