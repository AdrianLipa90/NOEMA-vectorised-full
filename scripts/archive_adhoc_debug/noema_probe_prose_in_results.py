#!/usr/bin/env python3
"""Sprawdz ile prose_sentence entries trafia do results z PhaseMemory query."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import numpy as np
from ciel_geometry.cielingo_inference import CIELingoInference

engine = CIELingoInference()
mem = engine.memory

# Policz prose_sentence entries w PhaseMemory
prose_indices = set(
    i for i in range(mem.size)
    if i < len(mem.metadata) and mem.metadata[i].get("source_type") == "prose_sentence"
)
print(f"prose_sentence w PhaseMemory: {len(prose_indices)}")

# Symuluj phi_bypass query dla Q1
question = "Czym jest system NOEMA i jak działa jego architektura?"
phi = engine.encode(question)
op_id, op_vec, op_sim = engine.detect_operator(phi)
phi_transformed = engine.apply_operator(phi, op_id, op_vec, strength=0.3)

_noema_idx = [
    i for i, m in enumerate(mem.metadata)
    if i < len(mem.vectors) and m.get("source") == "noema_docs"
]
print(f"noema_docs in mem: {len(_noema_idx)}")

if len(_noema_idx) >= 3:
    _phi_centroid = np.mean(mem.vectors[_noema_idx], axis=0)
    _phi_bypass = 0.5 * phi_transformed + 0.5 * _phi_centroid
    _norm = np.linalg.norm(_phi_bypass)
    if _norm > 1e-9:
        _phi_bypass = _phi_bypass / _norm
    _phi_query = _phi_bypass
else:
    _phi_query = phi_transformed

results = mem.query(_phi_query, k=512, min_sim=0.0, include_sources={"noema_docs"})
print(f"\nQuery results: {len(results)}")
prose_in_results = [r for r in results if r.get("metadata", {}).get("source_type") == "prose_sentence"]
print(f"prose_sentence in results: {len(prose_in_results)}")
print("\nProse entries (sim order):")
for r in prose_in_results:
    print(f"  sim={r['sim']:.4f} | {repr(r['text'][:80])}")

# Sprawdz kilka prose ktore sa BRAK w results (jesli sa brakujace)
result_texts = {r["text"] for r in results}
missing_prose = [(i, mem.texts[i]) for i in prose_indices if mem.texts[i] not in result_texts]
print(f"\nBrakujace prose entries (NIE w results): {len(missing_prose)}")
for i, t in missing_prose[:5]:
    print(f"  [{i}] {repr(t[:100])}")
