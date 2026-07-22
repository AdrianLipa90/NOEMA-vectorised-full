"""CIEL/Ω Memory — Rule/heuristics weighting engine.

Split from: unified_memory.py (lines 170–228)
"""
from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Any, Dict
try:
    from .defaults import (
        DEFAULT_HEURISTICS_SELF,
        DEFAULT_HEURISTICS_USER,
        DEFAULT_RULES_IMMUTABLE,
        clamp,
    )
    from .unified_memory import RuleHeuristicsEngine
except ImportError:
    from memory.monolith.defaults import (
        DEFAULT_HEURISTICS_SELF,
        DEFAULT_HEURISTICS_USER,
        DEFAULT_RULES_IMMUTABLE,
        clamp,
    )
    from memory.monolith.unified_memory import RuleHeuristicsEngine

