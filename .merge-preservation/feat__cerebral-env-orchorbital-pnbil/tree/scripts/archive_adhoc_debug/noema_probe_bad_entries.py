#!/usr/bin/env python3
"""Diagnostyka: znajdz fizyczne artykuly i CODEX w noema_docs."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.cielingo_inference import CIELingoInference

engine = CIELingoInference()
mem = engine.memory

print(f"PhaseMemory total: {mem.size}")
noema = [(i, mem.texts[i]) for i in range(mem.size)
         if i < len(mem.metadata) and mem.metadata[i].get("source") == "noema_docs"]
print(f"noema_docs: {len(noema)}")
print()

print("=== SZUKAM: fizyka, CODEX, Python code w noema_docs ===")
for i, t in noema:
    markers = []
    if "branching" in t or "LHCb" in t or "luminosity" in t or "\\to\\mu" in t:
        markers.append("FIZYKA")
    if "CODEXGPT" in t or "tablice Przeznaczenia" in t or "kosmogonia" in t:
        markers.append("CODEX")
    if "import numpy" in t or "def pmns" in t:
        markers.append("PYTHON")
    if markers:
        print(f"[{i}] {'+'.join(markers)}: {t[:120]!r}")

print()
# Sprawdź metadane tych złych wpisów
print("=== METADANE zepsutych wpisów ===")
for i, t in noema:
    if "branching" in t or "CODEXGPT" in t or "import numpy" in t:
        print(f"[{i}] meta: {mem.metadata[i]}")
        print(f"     text: {t[:80]!r}")
