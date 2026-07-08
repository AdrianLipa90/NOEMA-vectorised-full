#!/usr/bin/env python3
"""
ciel_confidence.py — Confidence scoring engine (thin wrapper).

Przekierowuje do ciel_confidence_system.engine dla backward compatibility.
Nowa lokalizacja: scripts/ciel_confidence_system/engine.py
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from ciel_confidence_system.engine import *

if __name__ == "__main__":
    from ciel_confidence_system.engine import main
    main()
