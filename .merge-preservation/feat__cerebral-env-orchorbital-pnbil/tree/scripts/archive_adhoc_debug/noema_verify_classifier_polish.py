#!/usr/bin/env python3
"""Verify concept_classifier.classify_text() after Polish anchors + diacritic
regex fix."""
from __future__ import annotations

import sys
sys.path.insert(0, "src")

from ciel_geometry.phasenav.concept_classifier import classify_text

TESTS = [
    "pamiętasz co mówiliśmy wcześniej?",
    "kim jesteś?",
    "jak się czujesz?",
    "co to jest phasenav?",
]

for t in TESTS:
    op, score = classify_text(t)
    print(f"{t!r} -> {op} (score={score})")
