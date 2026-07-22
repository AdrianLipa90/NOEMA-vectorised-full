#!/usr/bin/env python3
"""Probe: co jest w PhaseMemory po filtrze NL + wysoka similarity."""
import logging, sys, re
from pathlib import Path

_log = logging.getLogger(__name__)

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ciel_geometry.cielingo_inference import CIELingoInference

engine = CIELingoInference()
print(f"PhaseMemory size: {engine.memory.size} entries")

# Sprawdź skład źródeł
sources_count: dict[str, int] = {}
for i in range(engine.memory.size):
    try:
        meta = engine.memory._metadata[i] if hasattr(engine.memory, '_metadata') else {}
        src = (meta.get("source") or "?") if isinstance(meta, dict) else "?"
        sources_count[src] = sources_count.get(src, 0) + 1
    except Exception as exc:
        _log.debug("metadata access failed at index %s: %s", i, exc)
print(f"Sources: {sources_count}\n")

def is_nl(t: str) -> bool:
    t = t.strip()
    if len(t) < 30: return False
    if t.startswith(("#", "{", "[", "```")): return False
    if "**id_karty:**" in t or '"method":' in t or '"samples":' in t: return False
    if "## Tożsamość" in t or "poziom_orbitalny" in t: return False
    return True

# Query PhaseMemory dla pytania o NOEMA
from ciel_geometry.cielingo_phase_encoder import fast_encode_text_weighted
phi, weights = fast_encode_text_weighted("Czym jest system NOEMA i jak działa jego architektura?")
results = engine.memory.query(phi, k=20, min_sim=0.10, weights=weights, exclude_sources={"raw_logs"})
if not results:
    results = engine.memory.query(phi, k=20, min_sim=0.10, weights=weights)

nl_results = [r for r in results if is_nl(r.get("text", ""))]
print(f"=== Query: NOEMA architektura ===")
print(f"Wyniki raw: {len(results)}, po filtrze NL: {len(nl_results)}\n")
for r in nl_results[:5]:
    meta = r.get("metadata", {})
    print(f"sim={r['sim']:.3f} src={meta.get('source','?')}")
    print(f"  {r['text'][:200]}")
    print()

# Query dla PhaseNav
phi2, weights2 = fast_encode_text_weighted("PhaseNav operator fazy")
results2 = engine.memory.query(phi2, k=20, min_sim=0.10, weights=weights2, exclude_sources={"raw_logs"})
if not results2:
    results2 = engine.memory.query(phi2, k=20, min_sim=0.10, weights=weights2)
nl2 = [r for r in results2 if is_nl(r.get("text", ""))]
print(f"=== Query: PhaseNav operator fazy ===")
print(f"Wyniki raw: {len(results2)}, po filtrze NL: {len(nl2)}\n")
for r in nl2[:5]:
    meta = r.get("metadata", {})
    print(f"sim={r['sim']:.3f} src={meta.get('source','?')}")
    print(f"  {r['text'][:200]}")
    print()
