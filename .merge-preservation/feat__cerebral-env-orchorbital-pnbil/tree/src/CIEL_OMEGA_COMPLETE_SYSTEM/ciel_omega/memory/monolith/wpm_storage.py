"""CIEL/Ω Memory — WPM durable store (HDF5 wave archive).

Split from: unified_memory.py (lines 394–472)
Requires h5py (optional dependency).
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, Optional
try:
    from .data_types import MemoriseD
    from .unified_memory import WPMWriterHDF5
except ImportError:
    from memory.monolith.data_types import MemoriseD
    from memory.monolith.unified_memory import WPMWriterHDF5

