#!/usr/bin/env python3
"""Oczyszcza PhaseMemory z REPO-style noema_docs entries.

Usuwa wpisy noema_docs które NIE są naturalną prozą — tabele, REPO bullets,
import-listy, nagłówki sekcji. Zostawia tylko czyste zdania i paragrafy.

Zasada digest-before-erase: wpisy REPO-style (struktura pliku, import-listy)
nie są 'pamięcią doświadczeń' — to artefakty złego chunkowania markdown.
Bezpieczne do usunięcia bez digestowania.
"""
import sys, re, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import numpy as np
from ciel_geometry.cielingo_phase_memory import PhaseMemory
from ciel_geometry.paths import P

mem_path = Path(P.MEMORY.PHASE_MEMORY_DIR)
print(f"Ładowanie PhaseMemory z: {mem_path}")
mem = PhaseMemory.load_or_create(mem_path)
print(f"Łącznie wpisów: {mem.size}")

# Wpisy noema_docs
noema_indices = [
    i for i in range(mem.size)
    if i < len(mem.metadata) and mem.metadata[i].get("source") == "noema_docs"
]
print(f"noema_docs: {len(noema_indices)}")

# Strict prose filter — silniejszy niż daemon's NL filter
_REPO_MARKERS_STRICT = (
    "**Purpose**:", "**Imports**:", "**Exports**:", "**Active**:", "**Uses**:",
    "**Status**:", "**Entry points**:", "**Optional deps**:", "**Dependencies**:",
    "**Description**:", "**id_karty:**", '"method":', '"samples":',
    "- **Purpose", "- **Import", "#### `",
    "#### `",
)

def is_prose(t: str) -> bool:
    """True jeśli tekst to czysta proza, False jeśli REPO/code/table."""
    t = t.strip()
    if len(t) < 30:
        return False
    # Startswith checks
    if t.startswith(('#', '{', '[', '```', '- **', '|', '---')):
        return False
    if t.startswith('REPO-'):
        return False
    # REPO markers w ciele
    if any(m in t for m in _REPO_MARKERS_STRICT):
        return False
    # Tabele inline (bold headers bez kolon)
    bold_count = len(re.findall(r'\*\*[A-Z][a-zA-Z0-9_/ ]{0,15}\*\*', t))
    if bold_count >= 3:
        return False
    # Import-listy: wiele `backtick` elementów
    backtick_items = re.findall(r'`[^`\n]{1,40}`', t)
    if len(backtick_items) >= 3 and len(t) < 200:
        return False
    # Dunder-heavy (Python internals)
    dunder_count = len(re.findall(r'__\w+__', t))
    if dunder_count >= 2:
        return False
    # Non-ASCII non-alpha > 20%
    non_ascii_nonalpha = sum(1 for c in t if ord(c) > 127 and not c.isalpha())
    if non_ascii_nonalpha > len(t) * 0.20:
        return False
    # Starts with lowercase word that's typically a code identifier
    first_word = t.split()[0] if t.split() else ''
    if first_word and first_word[0].islower() and first_word.endswith(('-exports', '-by-')):
        return False
    return True

# Klasyfikuj
keep = []  # (idx, text, meta)
remove = []  # (idx, text, meta)
for i in noema_indices:
    t = mem.texts[i]
    meta = mem.metadata[i]
    if is_prose(t):
        keep.append(i)
    else:
        remove.append(i)

print(f"\nDo zachowania (prose): {len(keep)}")
print(f"Do usunięcia (REPO/code): {len(remove)}")
print(f"\nPrzykłady DO USUNIĘCIA:")
for i in remove[:8]:
    print(f"  [{i}] {repr(mem.texts[i][:100])}")
print(f"\nPrzykłady DO ZACHOWANIA:")
for i in keep[:8]:
    print(f"  [{i}] {repr(mem.texts[i][:100])}")

# Zbuduj nowe struktury BEZ usuniętych wpisów
remove_set = set(remove)
new_texts = []
new_vectors = []
new_weights = []
new_metadata = []

for i in range(mem.size):
    if i in remove_set:
        continue
    new_texts.append(mem.texts[i])
    new_vectors.append(mem.vectors[i])
    new_weights.append(mem.weights[i])
    new_metadata.append(mem.metadata[i])

print(f"\nRebuild: {mem.size} → {len(new_texts)} entries (usunięto {len(remove_set)})")

# Zastąp dane
mem.texts = new_texts
mem.vectors = np.array(new_vectors, dtype=np.float64) if new_vectors else np.zeros((0, 36))
mem.weights = np.array(new_weights, dtype=np.float64) if new_weights else np.zeros((0, 36))
mem.metadata = new_metadata

# Rebuild hash index
mem._hash_index = {}
import hashlib
for idx, t in enumerate(mem.texts):
    h = hashlib.sha256(t.encode()).hexdigest()[:16]
    mem._hash_index[h] = idx

mem.save()
print(f"Zapisano. PhaseMemory size: {mem.size}")
print(f"noema_docs zostało: {sum(1 for m in mem.metadata if m.get('source') == 'noema_docs')}")
