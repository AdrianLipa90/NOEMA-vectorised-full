#!/usr/bin/env python3
"""Diagnose polluted PhaseMemory entries: text chunks that are literal
console output of CIEL_CANON.py cmd_search() instead of real knowledge.
Read-only — logs candidates, does not delete anything."""
import sys
sys.path.insert(0, "/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/src")

from ciel_geometry.cielingo_inference import MEMORY_PATH
from ciel_geometry.phase_nav_lang import analyze_prompt  # noqa: F401 (import sanity)

print(f"MEMORY_PATH = {MEMORY_PATH}")
print(f"exists = {MEMORY_PATH.exists() if hasattr(MEMORY_PATH, 'exists') else 'n/a'}")

from ciel_geometry.cielingo_inference import CIELingoInference

ci = CIELingoInference()
mem = ci.memory
print(f"memory.size = {mem.size}")

print(f"\nSample of first 10 texts:")
for i in range(min(10, len(mem.texts))):
    print(f"  [{i}] {mem.texts[i][:150]!r}")

candidates = []
for i, text in enumerate(mem.texts):
    if "PhaseNav" in text or "plikow" in text or "plików" in text or "Adrian Lipa" in text:
        meta = mem.metadata[i] if i < len(mem.metadata) else {}
        candidates.append({"index": i, "text": text[:300], "metadata": meta})

print(f"\nFound {len(candidates)} candidates (PhaseNav / plikow / Adrian Lipa)")
for c in candidates[:40]:
    print(f"  [{c['index']}] {c['text']!r}")
    print(f"       meta={c['metadata']}")
