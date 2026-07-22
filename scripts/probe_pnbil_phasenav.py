#!/usr/bin/env python3
"""Czytaj pn_bil/phasenav.py — jak działa seed_from_sha256 i czy można użyć na tekście."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pn_bil.phasenav import PHASENAV_24D_COMPONENTS, seed_from_sha256, normalised_distance
import inspect

# Źródło
print("=== PHASENAV_24D_COMPONENTS ===")
for c in PHASENAV_24D_COMPONENTS:
    print(f"  {c}")

# Pokaż wszystkie funkcje
from pn_bil import phasenav as pn_mod
print("\n=== phasenav.py functions ===")
for name, obj in inspect.getmembers(pn_mod, inspect.isfunction):
    sig = str(inspect.signature(obj))[:100]
    print(f"  def {name}{sig}")

# Pokaż build_phase_vector - czy można wywołać na tekście (sha256 stringa)
print("\n=== build_phase_vector source ===")
from pn_bil.phasenav import build_phase_vector
print(inspect.getsource(build_phase_vector)[:2000])

# Test: wektoryzuj pytanie jako tekst
import hashlib
question = "Czym jest holonomia fazowa w CIELingo?"
sha = hashlib.sha256(question.encode()).hexdigest()
seed = seed_from_sha256(sha)
print(f"\n=== Test seed z pytania ===")
print(f"  sha256 = {sha[:20]}...")
print(f"  seed   = {seed}")

# Czy można wywołać semantic_collatz na tym seedzie?
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src/cielingo"))
try:
    from cielingo.semantic_collatz import semantic_collatz_route, route_summary
    route = semantic_collatz_route(seed, max_steps=16)
    summary = route_summary(route)
    print(f"  collatz dominant_mode = {summary['dominant_mode']}")
    print(f"  steps={summary['steps']}, expand={summary['expand_count']}, reduce={summary['reduce_count']}")
except Exception as e:
    print(f"  semantic_collatz error: {e}")
