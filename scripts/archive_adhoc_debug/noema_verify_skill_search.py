#!/usr/bin/env python3
"""Check if this is Polish declension (pamięć vs pamięci) not a new bug."""
from __future__ import annotations

import sys
sys.path.insert(0, "src")
sys.path.insert(0, "scripts")

from ciel_speaker import _phase_search, _load_skill_descs

for text in ["pamięć", "pamięci", "memory"]:
    hits = [h for h in _phase_search(text, top_n=5) if h.get("source_type") == "skill"]
    print(repr(text), "->", [(h["name"], h["similarity"]) for h in hits])

descs = _load_skill_descs()
matches = [n for n, d in descs.items() if "pamięć" in (n + " " + d).casefold()]
print("skills containing exact 'pamięć':", matches[:5])
