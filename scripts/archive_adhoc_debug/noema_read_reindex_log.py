#!/usr/bin/env python3
"""Tylko odczyt logu reindex."""
from pathlib import Path
LOG = Path("/media/adrian/New Volume/CIEL_memories/logs/reindex_card_mode.log")
lines = LOG.read_text(encoding="utf-8").splitlines()
print(f"Log: {len(lines)} linii")
for l in lines:
    print(l)
