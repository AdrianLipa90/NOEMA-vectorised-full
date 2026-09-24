#!/usr/bin/env python3
"""
ciel_ingest.py — Data ingestion pipeline (thin wrapper).

Przekierowuje do ciel_confidence_system.ingest.
Nowa lokalizacja: scripts/ciel_confidence_system/ingest.py
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from ciel_confidence_system.ingest import *

if __name__ == "__main__":
    from ciel_confidence_system.ingest import main
    main()
