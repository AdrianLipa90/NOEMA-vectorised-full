#!/usr/bin/env python3
"""One-off check: is the 7124-row 'aktor/actor' hit count in doc_analysis
real celebrity/movie-actor garbage data, or a substring false-positive from
words like attractor/refactor/factory/factor/reactor?
"""
from __future__ import annotations

import re
import sqlite3
import sys
sys.path.insert(0, "src")

from ciel_geometry.paths import P

DB = str(P.DB.KNOWLEDGE)

FALSE_POSITIVE_PREFIXES = ("attractor", "refactor", "factory", "factor", "reactor")
PATTERN = re.compile(r"\b(aktor\w*|actor\w*)\b", re.IGNORECASE)


def main() -> int:
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(
        "SELECT rowid, filename, source_type, essence FROM doc_analysis "
        "WHERE essence LIKE '%aktor%' OR essence LIKE '%actor%'"
    )
    real_hits = []
    for id_, filename, source_type, essence in cur.fetchall():
        if essence is None:
            continue
        matches = PATTERN.findall(essence)
        genuine = [m for m in matches if not any(m.lower().startswith(p) for p in FALSE_POSITIVE_PREFIXES)]
        if genuine:
            real_hits.append((id_, filename, source_type, genuine[:3]))

    print(f"Total substring hits: checked, genuine (non-attractor/refactor/factory/factor/reactor) hits: {len(real_hits)}")
    for h in real_hits[:30]:
        print(h)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
