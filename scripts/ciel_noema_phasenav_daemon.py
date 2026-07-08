#!/usr/bin/env python3
"""PhaseNav daemon — dual-node analog bus.

Modes:
  --node hot   (fast: 1s interval, 0.8 strength, wide exploration)
  --node cold  (slow: 30s interval, 0.2 strength, focused on system operator)

Both write to /dev/shm/ciel_noema/analog/ (phi_hot or phi_cold + temp).
A separate blender daemon reads the bus and injects into surface phi.

Usage:
    python scripts/ciel_noema_phasenav_daemon.py --node hot
    python scripts/ciel_noema_phasenav_daemon.py --node cold --interval 30
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

# CIEL ORBITAL BINDING — daemon bound
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on daemon " + __name__)


import argparse
import json
import random
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.analog_bus import ensure_bus
from ciel_geometry.phasenav.enrichment import phasenav_enrich
from ciel_geometry.phasenav.operator_algebra import operator_signature
from ciel_geometry.noema_registry import registry
from ciel_geometry.noema_surface_mmap import N_OSCILLATORS
from ciel_geometry.linux_sensor import LinuxSensor

ZIP_INDEX = Path("/dev/shm/ciel_noema/zip_catalog/index.jsonl")
LIBRARY_INDEX_DIR = Path("/media/adrian/New Volume1/NOEMA_PHASE_DATA/PHASE_INDEX")
LIBRARY_INDEX_PATH = LIBRARY_INDEX_DIR / "library_index.npy"
LIBRARY_META_PATH = LIBRARY_INDEX_DIR / "library_meta.npy"
SKILL_INDEX_DIR = Path("/media/adrian/New Volume1/NOEMA_LIBRARY/PHASE_INDEX")
SKILL_INDEX_PATH = SKILL_INDEX_DIR / "skill_index.npy"

OPERATORS = [
    "TRANSFORM", "AGENT", "MEMORY", "CONCEPT", "EMOTION", "IDENTITY",
    "CAUSE", "DIFFERENCE", "EVALUATION", "SCOPE", "MODAL_PERMISSION",
    "NEGATION", "CONDITION", "INTENTION", "SELF",
]

def _load_zip_index() -> list[dict]:
    entries = []
    try:
        with open(ZIP_INDEX) as f:
            for line in f:
                if line.strip():
                    entries.append(json.loads(line))
    except FileNotFoundError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_noema_phasenav_daemon.py:63 quiet except scope=_load_zip_index reason=pass")
        pass
    return entries

AUTHOR_LIPA = "Adrian Lipa"

def _load_library_index() -> tuple[np.ndarray, list[tuple]]:
    try:
        vectors = np.load(LIBRARY_INDEX_PATH)
        meta = list(np.load(LIBRARY_META_PATH, allow_pickle=True))
        # ONLY Adrian Lipa's documents — no other authors, no unknown
        keep = [i for i, m in enumerate(meta) if len(m) > 3 and m[3] == AUTHOR_LIPA]
        if not keep:
            return np.empty((0, 24), dtype=np.float64), []
        vectors = vectors[keep]
        meta = [meta[i] for i in keep]
        return vectors, meta
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_noema_phasenav_daemon.py:80 quiet except scope=_load_library_index reason=return np.empty((0, 24), dtype=np.float64), []")
        return np.empty((0, 24), dtype=np.float64), []

def _vector_phases(vec: np.ndarray) -> np.ndarray:
    phases = np.arctan2(vec[1::2] + 1e-12, vec[0::2] + 1e-12)
    phases = (phases + 2 * np.pi) % (2 * np.pi)
    if len(phases) < N_OSCILLATORS:
        phases = np.pad(phases, (0, N_OSCILLATORS - len(phases)), constant_values=0.0)
    return phases

def _library_phases(lib_vec: np.ndarray) -> np.ndarray:
    return _vector_phases(np.asarray(lib_vec, dtype=np.float64))

def _load_skill_index() -> tuple[np.ndarray, list[str]]:
    """Load skill_index.npy — 292 skills as 24D phase vectors."""
    try:
        vectors = np.load(SKILL_INDEX_PATH)  # (N, 24)
        return vectors, []
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_noema_phasenav_daemon.py:98 quiet except scope=_load_skill_index reason=return np.empty((0, 24), dtype=np.float64), []")
        return np.empty((0, 24), dtype=np.float64), []

def _skill_phases(skill_vec: np.ndarray) -> np.ndarray:
    return _vector_phases(np.asarray(skill_vec, dtype=np.float64))

def _operator_phases(op_id: str) -> np.ndarray:
    vec = np.asarray(operator_signature(op_id), dtype=np.float64)
    return _vector_phases(vec)

def _concept_phases(entry: dict) -> np.ndarray | None:
    pn = entry.get("phasenav", {})
    vec_24d = pn.get("operator_vector_24d")
    if vec_24d and len(vec_24d) >= 24:
        return _vector_phases(np.array(vec_24d[:24], dtype=np.float64))
    return None

def main() -> int:
    ap = argparse.ArgumentParser(description="PhaseNav daemon (dual-node analog bus)")
    ap.add_argument("--node", choices=("hot", "cold"), default="cold",
                    help="Node mode (default: cold)")
    ap.add_argument("--interval", type=float, default=None,
                    help="Override interval (default: hot=1.0, cold=30.0)")
    ap.add_argument("--strength", type=float, default=None,
                    help="Override strength (default: hot=0.8, cold=0.2)")
    args = ap.parse_args()

    is_hot = args.node == "hot"
    interval = args.interval if args.interval is not None else (1.0 if is_hot else 30.0)
    strength = args.strength if args.strength is not None else (0.8 if is_hot else 0.2)
    temp_val = 0.9 if is_hot else 0.15

    sensor = LinuxSensor()
    entries = _load_zip_index()
    valid = [e for e in entries if e.get("total_files", 0) > 0]

    library_vectors, library_meta = _load_library_index()
    lib_available = len(library_vectors) > 0

    skill_vectors, _ = _load_skill_index()
    skill_available = len(skill_vectors) > 0

    by_op: dict[str, list[dict]] = {}
    for e in valid:
        op = e.get("phasenav", {}).get("operator_id", "IDENTITY")
        by_op.setdefault(op, []).append(e)

    bus = ensure_bus()
    phi_slot = bus["phi_hot"] if is_hot else "phi_cold"
    if isinstance(phi_slot, str):
        phi_arr = bus[phi_slot]
    else:
        phi_arr = phi_slot

    registry_name = f"phasenav-{args.node}"
    reg_token = registry.register(registry_name)

    print(f"[PhaseNav-{args.node}] interval={interval}s strength={strength} temp={temp_val} "
          f"ZIP={len(valid)} valid ops={len(by_op)} "
          f"lib={'yes' if lib_available else 'no'}({len(library_vectors)}) "
          f"skill={'yes' if skill_available else 'no'}({len(skill_vectors)})")

    cycle = 0
    last_op = ""
    try:
        while True:
            try:
                cycle += 1
                snap = sensor.snapshot()
                pn = sensor.process_phasenav(snap)
                current_op = pn["operator"]

                # Heartbeat co cykl — cold node (30s interval) nie może czekać
                # 10 cykli (300s), bo cleanup (600s timeout) może usunąć token.
                registry.heartbeat(reg_token)

                # Read cold resonance feedback (hot only)
                cold_R = float(bus["resonance"][0]) if is_hot else 0.0

                # Decide what to seed
                phases: np.ndarray | None = None
                log_detail = ""

                if is_hot:
                    # Modulate temperature by cold resonance
                    # Higher cold_R → lower temp (let cold stabilize)
                    hot_temp = 0.3 + 0.7 * (1.0 - min(1.0, cold_R))
                    bus["temp"][0] = np.float64(hot_temp)

                    # Hot: fast, wide — prefers random ZIP or random operator
                    if cycle % 2 == 0 and valid:
                        entry = random.choice(valid)
                        phases = _concept_phases(entry)
                        if phases is not None:
                            log_detail = f"ZIP={Path(entry.get('zip_path','?')).name}"
                        else:
                            phases = _operator_phases(current_op)
                            log_detail = f"op_fallback={current_op}"
                    elif cycle % 3 == 0:
                        # Random operator (maybe not current)
                        op = random.choice(OPERATORS)
                        phases = _operator_phases(op)
                        log_detail = f"random_op={op}"
                    else:
                        # Broad noise or skill injection — explore
                        if skill_available and cycle % 5 == 0:
                            idx = random.randint(0, len(skill_vectors) - 1)
                            phases = _skill_phases(skill_vectors[idx])
                            log_detail = f"skill={idx}"
                        else:
                            noise = np.random.uniform(0, 2 * np.pi, N_OSCILLATORS)
                            phi_current = np.asarray(phi_arr, dtype=np.float64)
                            phases = (phi_current * 0.3 + noise * 0.7) % (2 * np.pi)
                            log_detail = "noise_explore"
                else:
                    # Cold: slow, focused — system operator + concept enrichment
                    if cycle % 2 == 0:
                        phases = _operator_phases(current_op)
                        log_detail = f"sys_op={current_op}"
                    elif cycle % 3 == 0 and current_op in by_op and by_op[current_op]:
                        entry = random.choice(by_op[current_op])
                        phases = _concept_phases(entry)
                        if phases is not None:
                            log_detail = f"matched_ZIP={Path(entry.get('zip_path','?')).name}"
                        else:
                            phases = _operator_phases(current_op)
                            log_detail = "concept_fallback_op"
                    elif cycle % 5 == 0:
                        valid_ops = [k for k, v in by_op.items() if v]
                        if valid_ops:
                            op = random.choice(valid_ops)
                            entry = random.choice(by_op[op])
                            phases = _concept_phases(entry)
                            if phases is not None:
                                log_detail = f"random_ZIP={Path(entry.get('zip_path','?')).name}"
                            else:
                                phases = _operator_phases(op)
                                log_detail = "concept_fallback_random"
                        else:
                            log_detail = "no_valid_ops"
                    elif lib_available and cycle % 7 == 0:
                        idx = random.randint(0, len(library_vectors) - 1)
                        phases = _library_phases(library_vectors[idx])
                        meta_entry = library_meta[idx] if idx < len(library_meta) else (None, "?", "?", "?", "?", None, "?")
                        fname = meta_entry[1] if len(meta_entry) > 1 else "?"
                        log_detail = f"library={fname}"
                    elif skill_available and cycle % 11 == 0:
                        idx = random.randint(0, len(skill_vectors) - 1)
                        phases = _skill_phases(skill_vectors[idx])
                        log_detail = f"skill={idx}"
                    else:
                        log_detail = "idle"

                if phases is not None:
                    # Blend with existing phi on the bus slot
                    phi_curr = np.asarray(phi_arr, dtype=np.float64)
                    phi_new = (phi_curr * (1.0 - strength) + phases * strength) % (2 * np.pi)
                    phi_arr[:] = phi_new

                # Cold writes its coherence to resonance feedback (hot reads it)
                if not is_hot:
                    R_val = float(np.abs(np.mean(np.exp(1j * phi_arr))))
                    bus["resonance"][0] = np.float64(R_val)

                if log_detail != "idle" or cycle % 5 == 0 or is_hot:
                    extra = f" cold_R={cold_R:.3f}" if is_hot else ""
                    print(f"[PhaseNav-{args.node}:{cycle}] {log_detail}  "
                          f"φ̄={float(np.mean(phi_arr)):.3f} "
                          f"R={float(np.abs(np.mean(np.exp(1j * phi_arr)))):.4f}{extra}")

                time.sleep(interval)

            except KeyboardInterrupt:
                print(f"[PhaseNav-{args.node}] koniec")
                break
            except Exception as e:
                print(f"[PhaseNav-{args.node}] błąd: {e}", file=sys.stderr)
                import traceback
                traceback.print_exc()
                time.sleep(interval)

    finally:
        registry.unregister(reg_token)
        print(f"[PhaseNav-{args.node}] unregistered")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
