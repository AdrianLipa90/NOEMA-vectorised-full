"""CIEL/Ω Memory — Unified orchestrator: capture → TMP → bifurcation → durable.

Split from: unified_memory.py (lines 478–601)
"""
from __future__ import annotations
import datetime as dt
import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional
try:
    from .data_types import DataVector, MemoriseD
    from .defaults import (
        DEFAULT_HEURISTICS_SELF,
        DEFAULT_HEURISTICS_USER,
        DEFAULT_RULES_IMMUTABLE,
    )
    from .tmp_processor import TMPKernel
    from .tsm_storage import TSMWriterSQL
    from .wpm_storage import WPMWriterHDF5
    from .unified_memory import UnifiedMemoryOrchestrator
except ImportError:
    from memory.monolith.data_types import DataVector, MemoriseD
    from memory.monolith.defaults import (
        DEFAULT_HEURISTICS_SELF,
        DEFAULT_HEURISTICS_USER,
        DEFAULT_RULES_IMMUTABLE,
    )
    from memory.monolith.tmp_processor import TMPKernel
    from memory.monolith.tsm_storage import TSMWriterSQL
    from memory.monolith.wpm_storage import WPMWriterHDF5
    from memory.monolith.unified_memory import UnifiedMemoryOrchestrator

_SYSTEM_ROOT = Path(__file__).resolve().parents[3]
