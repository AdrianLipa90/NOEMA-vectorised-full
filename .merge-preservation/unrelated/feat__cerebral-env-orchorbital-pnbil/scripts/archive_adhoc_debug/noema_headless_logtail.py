#!/usr/bin/env python3
"""Pokaż koniec loga headless i szukaj handle/chat/error."""
from pathlib import Path

log_path = Path("/media/adrian/New Volume/CIEL_memories/logs/ciel_headless.jsonl")
text = log_path.read_text(errors="replace")
lines = text.split("\n")
print(f"Total lines: {len(lines)}")
print(f"\n=== OSTATNIE 120 LINII ===")
for l in lines[-120:]:
    print(l)
