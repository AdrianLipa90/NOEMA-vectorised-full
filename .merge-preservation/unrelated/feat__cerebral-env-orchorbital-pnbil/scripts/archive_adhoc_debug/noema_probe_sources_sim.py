#!/usr/bin/env python3
"""Sprawdz sim wartosci prose_sentence entries i czy sa w sources[:15]."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.cielingo_inference import CIELingoInference

engine = CIELingoInference()

result = engine.answer("Czym jest system NOEMA i jak działa jego architektura?", k=15)
sources = result.get("sources", [])
print(f"Total sources: {len(sources)}")

prose = [s for s in sources if s.get("source_type") == "prose_sentence"]
print(f"prose_sentence entries: {len(prose)}")
print(f"\nPierwsze 15 sources (po re-sort):")
for i, s in enumerate(sources[:15]):
    stype = s.get("source_type", "")
    label = "[PROSE]" if stype == "prose_sentence" else "[REPO]"
    sim = s.get("sim", 0)
    print(f"  [{i}] sim={sim:+.4f} {label} | {repr(s.get('text','')[:80])}")

print(f"\nProse entries sim distribution:")
neg = [s for s in prose if s.get("sim", 0) < 0]
pos = [s for s in prose if s.get("sim", 0) >= 0]
print(f"  sim >= 0: {len(pos)}")
print(f"  sim < 0:  {len(neg)}")
print(f"\nWszystkie prose sims:")
for s in prose:
    sim = s.get("sim", 0)
    print(f"  sim={sim:+.4f} | {repr(s.get('text','')[:70])}")
