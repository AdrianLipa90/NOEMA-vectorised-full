#!/usr/bin/env python3
"""Diagnostyka: co engine.answer() zwraca dla pytania o NOEMA."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.cielingo_inference import CIELingoInference

engine = CIELingoInference()
Q = "Czym jest system NOEMA i jak działa jego architektura?"

result = engine.answer(Q, k=15)
print(f"answer: {result['answer'][:200]!r}")
print(f"n_sources: {result['n_sources']}")
print(f"decision: {result['decision']}")
print(f"operator: {result['operator']}")
print()

print("=== SOURCES ===")
for i, s in enumerate(result.get("sources", [])):
    print(f"[{i}] sim={s['sim']:.4f} src={s['source']!r}")
    print(f"     {s['text'][:120]!r}")
    print()

# Też sprawdź co memory.query zwraca bez filtra NL
print("=== RAW memory.query (k=15, min_sim=0, include_sources=noema_docs) ===")
phi = engine.encode(Q)
from ciel_geometry.phasenav.operator_algebra import generate_operator_map
op_map = generate_operator_map()
op_id = result['operator']
op_vec = op_map.get(op_id, phi)
import numpy as np
phi_t = (phi + 0.3 * op_vec) / np.linalg.norm(phi + 0.3 * op_vec + 1e-9)

raw = engine.memory.query(phi_t, k=15, min_sim=0.0, include_sources={"noema_docs"})
print(f"Raw count: {len(raw)}")
for r in raw:
    m = r.get("metadata", {})
    print(f"  sim={r['sim']:.4f} src={m.get('source','?')!r} | {r['text'][:100]!r}")
