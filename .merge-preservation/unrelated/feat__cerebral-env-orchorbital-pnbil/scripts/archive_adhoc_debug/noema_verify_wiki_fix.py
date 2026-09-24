#!/usr/bin/env python3
"""Verify the Wikipedia title guesser no longer fabricates random titles
from ordinary lowercase Polish sentences."""
from __future__ import annotations

import sys
sys.path.insert(0, "src")
sys.path.insert(0, "scripts")

from ciel_speaker import _wiki_title_from_query

TESTS = [
    "pamiętasz co mówiliśmy wcześniej?",
    "jak się czujesz?",
    "opowiedz mi o Kuramoto",  # genuine capitalized name -> should still work
    "co to jest phasenav?",
]
for t in TESTS:
    print(repr(t), "->", repr(_wiki_title_from_query(t)))
