#!/usr/bin/env python3
"""Thin wrapper — redirects to ciel_confidence_system.report."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from ciel_confidence_system.report import *

if __name__ == "__main__":
    from ciel_confidence_system.report import main
    main()
