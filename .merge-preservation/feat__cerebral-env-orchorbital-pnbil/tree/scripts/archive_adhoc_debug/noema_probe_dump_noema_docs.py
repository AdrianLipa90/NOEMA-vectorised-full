#!/usr/bin/env python3
"""Dump wszystkich noema_docs entries — szukamy garbage."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.cielingo_inference import CIELingoInference

engine = CIELingoInference()
mem = engine.memory

noema = [(i, mem.texts[i], mem.metadata[i]) for i in range(mem.size)
         if i < len(mem.metadata) and mem.metadata[i].get("source") == "noema_docs"]
print(f"Total noema_docs: {len(noema)}")
print()

# Klasyfikuj wpisy
nl_markers_bad = [
    "coupling phase", "A_h", "exp(i", "phi_i", "Braid",
    "CODEXGPT", "tablice Przeznaczenia", "kosmogonia",
    "import numpy", "def pmns", "pmns(", "theta12",
    "branching", "LHCb", "luminosity", "centre-of-mass",
    "luminosity of", "$B^0", "\\mu^+", "fb^{-1}",
    "proton-proton", "TeV", "detector",
    "import ", "def ", "class ", "return ",
]

bad = []
good = []
for i, t, meta in noema:
    is_bad = any(m in t for m in nl_markers_bad)
    if is_bad:
        bad.append((i, t, meta))
    else:
        good.append((i, t, meta))

print(f"=== ZLE WPISY ({len(bad)}) ===")
for i, t, meta in bad:
    print(f"[{i}] src={meta.get('source')} added={meta.get('added_at','?')[:16] if meta.get('added_at') else '?'}")
    print(f"     {repr(t[:200])}")
    print()

print(f"\n=== DOBRE WPISY ({len(good)}) - pierwsze 30 ===")
for i, t, meta in good[:30]:
    print(f"[{i}] {repr(t[:150])}")
