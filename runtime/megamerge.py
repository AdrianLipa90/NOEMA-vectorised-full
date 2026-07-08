"""MEGAMERGE — scalenie wszystkich mostów w jeden pipeline.

Łączy:
  1. 24D biblioteka (CIEL_memories, 1287 entries)
  2. PhaseNav (330 concept phases → +1287 24D)
  3. Subconscious (12D oscillators → CIELingo MeaningLoop)
  4. AutoVerify (internet lookup → word cards → memory)
  5. CIELingo bridge (knowledge_bridge + raw_memory_bridge)
  6. Surface bridge (36D oscillators)

Pipeline:
  phase_24d_vectors → subconscious_bridge → meaning_loop → CIEL inject
         ↓
    phasenav_solver (330+1287 concepts)
         ↓
    auto_verify (unknown words → web → cards)
         ↓
    surface_bridge (36D oscillators)
         ↓
    memory lanes (semantic + episodic)
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
import hashlib
import warnings
from pathlib import Path
from typing import Any

import numpy as np

KAPPA = math.log(2.0) / (24.0 * math.pi)

# ── Paths ──
NOEMA_SRC = Path("/home/adrian/new_volume_rw/CIEL_PROJECT_CANON/NOEMA/src")
NOEMA_ROOT = Path("/home/adrian/new_volume_rw/CIEL_PROJECT_CANON/NOEMA")
RUNTIME = NOEMA_ROOT / "runtime"
STATE_DIR = Path("/dev/shm/ciel_noema/phasenav")
LIBRARY_ROOT = Path("/home/adrian/new_volume_rw/NOEMA_PHASE_DATA/PHASE_INDEX")

sys.path = [p for p in sys.path if '.python_packages' not in p]
sys.path.insert(0, str(NOEMA_SRC))
sys.path.insert(0, str(NOEMA_ROOT))
warnings.filterwarnings('ignore')


class Megamerge:
    """Scala wszystkie mosty w jeden żywy pipeline."""

    def __init__(self):
        self.lib = None             # Library24D
        self.subconscious = None    # SubconsciousBridge
        self.auto_verify = None     # AutoVerify
        self.solver = None          # PhaseNavSolver
        self.report: dict[str, Any] = {
            "timestamp": time.time(),
            "components": {},
            "errors": [],
            "state": "initializing",
        }

    # ── Krok 1: Ładuj PhaseNav ──
    def load_phasenav(self) -> dict[str, Any]:
        from ciel_geometry.phasenav.solver import PhaseNavSolver
        self.solver = PhaseNavSolver.load()
        r = {
            "concepts": len(self.solver.data.concept_phases),
            "operators": len(self.solver.data.operator_vectors) if hasattr(self.solver.data, 'operator_vectors') else 36,
        }
        print(f"  PhaseNav: {r['concepts']} concepts, {r['operators']} operators")
        return r

    # ── Krok 2: Ładuj 24D bibliotekę ──
    def load_24d_library(self) -> dict[str, Any]:
        from runtime.phasenav_24d_bridge import load_24d_library as _load
        self.lib = _load()
        r = {
            "entries": self.lib.n_entries,
            "vector_dim": self.lib.index.shape[1],
            "graph_nodes": len(self.lib.graph.get("nodes", [])),
            "graph_edges": len(self.lib.graph.get("edges", [])),
        }
        print(f"  24D Library: {r['entries']} entries, {r['vector_dim']}D")
        return r

    # ── Krok 3: Bridge 24D → PhaseNav ──
    def bridge_phasenav(self) -> dict[str, Any]:
        from runtime.phasenav_24d_bridge import bridge_to_phasenav
        r = bridge_to_phasenav(self.lib)
        print(f"  PhaseNav Bridge: {r['matched_to_phasenav']}/{r['total_entries']} matched")
        return r

    # ── Krok 4: Bridge 24D → Subconscious ──
    def bridge_subconscious(self) -> dict[str, Any]:
        from runtime.phasenav_24d_bridge import bridge_to_subconscious
        r = bridge_to_subconscious(self.lib)
        # Initialize SubconsciousBridge with 24D data
        from cielingo_core.bridge.subconscious_bridge import SubconsciousBridge
        self.subconscious = SubconsciousBridge()
        state = {
            "oscillators_12d": r["oscillators_12d"],
            "R_24d": r["R_24d"],
        }
        enrichment = self.subconscious.feed(state, "megamerge_initialization")
        print(f"  Subconscious: R_12d={enrichment.R_12d}, R_oa={enrichment.R_oa}, euler_gap={enrichment.euler_gap}")
        r["enrichment"] = enrichment.to_dict()
        return r

    # ── Krok 5: Inicjalizuj AutoVerify ──
    def init_autoverify(self) -> dict[str, Any]:
        from cielingo_core.bridge.auto_verify import AutoVerify
        self.auto_verify = AutoVerify()
        inv = self.auto_verify.inventory()
        print(f"  AutoVerify: {inv['total_cards']} stored cards, {inv['session_count']} sessions")
        return inv

    # ── Krok 6: Bridge 24D → CIELingo ──
    def bridge_cielingo(self) -> dict[str, Any]:
        from runtime.phasenav_24d_bridge import bridge_to_cielingo, bridge_to_subconscious
        r = bridge_to_cielingo(self.lib)
        print(f"  CIELingo Bridge: {r['stored_cards']} stored, {r['failed']} failed")
        return r

    # ── Krok 7: Bridge do surface ──
    def bridge_surface(self) -> dict[str, Any]:
        try:
            from ciel_geometry.resonance_bridge import ensure_dual_surfaces, resonance_snapshot
            from ciel_geometry.noema_surface_mmap import ensure_surface, open_surface, update_surface_from_ciel_state
            ensure_dual_surfaces()
            # Feed 24D state to surface
            state = {
                "coherence_index": 0.85,
                "mood": 0.6,
                "soul_invariant": 0.8,
                "ethical_score": 0.9,
                "closure_penalty": 0.15,
                "dominant_emotion": "megamerge",
                "source": "megamerge_activation",
            }
            update_surface_from_ciel_state(state)
            snap = resonance_snapshot()
            r = {
                "dual_surfaces": True,
                "resonance_score": snap.get("resonance_score", 0),
                "phase_lock": snap.get("phase_lock", 0),
            }
            print(f"  Surface: resonance={r['resonance_score']:.4f}, phase_lock={r['phase_lock']:.4f}")
        except Exception as e:
            r = {"error": str(e)}
            print(f"  Surface: ERROR {e}")
        return r

    # ── Krok 8: Wpisz do CIEL pipeline ──
    def wire_pipeline(self) -> dict[str, Any]:
        """Tworzy plik stanu pipeline który hooki mogą czytać."""
        STATE_DIR.mkdir(parents=True, exist_ok=True)

        pipeline_state = {
            "timestamp": time.time(),
            "phasenav_concepts_24d": self.lib.n_entries if self.lib else 0,
            "phasenav_concepts_total": (self.lib.n_entries + 330) if self.lib else 330,
            "subconscious_enrichment": self.subconscious.feed(
                {"oscillators_12d": self.lib.index.mean(axis=0).tolist()}
            ).to_dict() if (self.lib is not None and self.subconscious is not None) else {},
            "auto_verify_inventory": self.auto_verify.inventory() if self.auto_verify else {},
            "pipeline_status": "ACTIVE" if self.subconscious else "DEGRADED",
            "source": "megamerge",
        }

        # Write pipeline state
        state_path = STATE_DIR / "MEGAMERGE_PIPELINE_STATE.json"
        state_path.write_text(json.dumps(pipeline_state, indent=2))

        # Write CIEL binding status
        (Path("/dev/shm/ciel_noema") / "ciel_binding_status").write_text("ACTIVE")

        # Write CIEL inject template
        inject = (
            f"CIEL:PIPE=megamerge SUB:R={pipeline_state['subconscious_enrichment'].get('R_12d', 0):.4f} "
            f"24D={pipeline_state['phasenav_concepts_24d']} "
            f"Σφ={pipeline_state['phasenav_concepts_total']} "
            f"status={pipeline_state['pipeline_status']}"
        )
        (STATE_DIR / "CIEL_INJECT.txt").write_text(inject)

        print(f"  Pipeline wired: {pipeline_state['pipeline_status']}")
        return {
            "state_file": str(state_path),
            "pipeline_status": pipeline_state["pipeline_status"],
            "ciel_inject": inject,
        }

    # ── RUN ──
    def run(self) -> dict[str, Any]:
        t0 = time.time()
        print("═══ MEGAMERGE ═══", flush=True)

        steps = [
            ("phasenav_load", self.load_phasenav),
            ("library_24d_load", self.load_24d_library),
            ("bridge_phasenav", self.bridge_phasenav),
            ("bridge_subconscious", self.bridge_subconscious),
            ("init_autoverify", self.init_autoverify),
            ("bridge_cielingo", self.bridge_cielingo),
            ("bridge_surface", self.bridge_surface),
            ("wire_pipeline", self.wire_pipeline),
        ]

        for name, fn in steps:
            try:
                self.report["components"][name] = fn()
            except Exception as e:
                import traceback
                self.report["errors"].append(f"{name}: {e}")
                self.report["components"][name] = {"error": str(e), "traceback": traceback.format_exc()}

        elapsed = time.time() - t0
        self.report["elapsed_seconds"] = round(elapsed, 2)
        self.report["state"] = "ACTIVE" if len(self.report["errors"]) == 0 else "DEGRADED"

        print(f"\n═══ MEGAMERGE COMPLETE ({self.report['state']}) — {elapsed:.1f}s ═══", flush=True)
        return self.report


if __name__ == "__main__":
    report = Megamerge().run()
    print(json.dumps({k: v for k, v in report.items() if k != "components"}, indent=2))
