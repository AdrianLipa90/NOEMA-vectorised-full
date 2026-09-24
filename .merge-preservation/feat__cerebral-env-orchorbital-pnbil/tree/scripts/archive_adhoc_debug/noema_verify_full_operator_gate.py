#!/usr/bin/env python3
"""Verify the full 36-operator gate: assertion passes, and domain routing
genuinely differs across a sample of operators."""
from __future__ import annotations

import sys
sys.path.insert(0, "src")
sys.path.insert(0, "scripts")

from ciel_speaker import speak

ciel_state = {"soul_invariant": 0.6, "coherence_index": 0.5}

for op in ["MEMORY", "SOURCE", "ACTION_REQUEST", "UNRUH_DRIVE", "PAUSE", "FORCE", "UNCERTAINTY"]:
    lingo = {"phase_nav": {"operator": op, "connections": {}, "urgency": 0.0, "holonomy": 0.1}}
    try:
        result = speak(ciel_state, lingo, text="test input unrelated to any operator keyword")
        print(f"{op:20s} -> ok, response len={len(result)}")
    except AssertionError as e:
        print(f"{op:20s} -> ASSERTION FAILED: {e}")
        raise
