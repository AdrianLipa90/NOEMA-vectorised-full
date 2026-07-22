#!/usr/bin/env python3
"""Sprawdź log od końca i rozmiar — wykryj DONE lub truncację."""
from pathlib import Path
import os

LOG = Path("/media/adrian/New Volume/CIEL_memories/logs/reindex_card_mode.log")

size = LOG.stat().st_size
print(f"Rozmiar logu: {size} bajtów")

# Czytaj jako bytes — wykryj null bytes, offset itp.
data = LOG.read_bytes()
print(f"Null bytes: {data.count(b'\x00')}")

# Konwertuj na text ignorując błędy
text = data.decode("utf-8", errors="replace")
lines = text.splitlines()
print(f"Wszystkie linie: {len(lines)}")
for i, l in enumerate(lines):
    stripped = l.rstrip('\x00').strip()
    if stripped:
        print(f"  [{i+1}] {stripped[:120]}")
