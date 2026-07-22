#!/usr/bin/env python3
"""Stress test: PC (plain) vs NOEMA+HTRI vs NOEMA+PhaseNav.

Każdy tryb: 5000 kroków Kuramoto na /dev/shm/ciel_noema.

Tryby:
  1. PC (plain)     — czysta numpy: fala, coupling, fft, bez shm/HTRI/PhaseNav
  2. NOEMA+HTRI     — Kuramoto 3-6-9 na /dev/shm/ciel_noema, evolve_surface()
  3. NOEMA+PhaseNav — Kuramoto + PhaseNav enrichment na każdym kroku

SAFEGUARDS: timeout 120s, flush co 500 steps, restore phi na koniec.
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import math
import os
import signal
import sys
import time
import tracemalloc
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

NOEMA_ROOT = Path("/dev/shm/ciel_noema")
N_OSC = 24
N_STEPS = 5_000
BURN_IN = 500
TIMEOUT_S = 120

class TimeoutError(Exception):
    pass

def _timeout_handler(signum, frame):
    raise TimeoutError("Przekroczono limit czasu")

def _with_timeout(fn):
    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(TIMEOUT_S)
    try:
        return fn()
    finally:
        signal.alarm(0)


# ── 1. PC (plain) — zwykła numpy ──────────────────────────────────────────

def stress_pc() -> dict:
    """Czysta numpy: syntetyczny Kuramoto + fale + FFT + macierze.

    Żadnych importów z ciel_geometry, żadnego HTRI/PhaseNav/shm.
    """
    rng = np.random.default_rng(42)
    phi = rng.uniform(0, 2 * math.pi, N_OSC).astype(np.float64)
    omega = np.full(N_OSC, 39.6, dtype=np.float64)
    g = rng.uniform(0, 0.5, (N_OSC, N_OSC)).astype(np.float64)
    g = (g + g.T) / 2
    np.fill_diagonal(g, 0.5)
    dt = 0.01

    t0 = time.perf_counter_ns()
    cpu0 = time.process_time_ns()

    thinking_deltas = np.zeros(N_STEPS, dtype=np.float64)
    R_means = np.zeros(N_STEPS, dtype=np.float64)

    for step in range(N_STEPS):
        # Prosty coupling (bez harmonicznych)
        diff = phi[:, None] - phi[None, :]
        coupling = np.sum(g * np.sin(diff), axis=1) / N_OSC
        phi = (phi + dt * (omega + coupling)) % (2 * math.pi)

        # Prosty thinking proxy: RMS różnicy faz
        thinking_deltas[step] = float(np.std(np.angle(np.exp(1j * diff.mean(axis=1)))))
        R_means[step] = float(abs(np.mean(np.exp(1j * phi))))

    dt_ns = time.perf_counter_ns() - t0
    cpu_ns = time.process_time_ns() - cpu0

    return {
        "mode": "pc_plain",
        "steps": N_STEPS,
        "wall_s": round(dt_ns / 1e9, 4),
        "cpu_s": round(cpu_ns / 1e9, 4),
        "cpu_pct": round(cpu_ns / dt_ns * 100, 1) if dt_ns > 0 else 0,
        "steps_per_sec": round(N_STEPS / (dt_ns / 1e9), 1),
        "thinking_delta_mean": round(float(thinking_deltas.mean()), 6),
        "R_mean": round(float(R_means.mean()), 6),
        "R_final": round(float(R_means[-1]), 6),
    }


# ── 2. NOEMA+HTRI ─────────────────────────────────────────────────────────

def stress_noema_htri() -> dict:
    """Pełna powierzchnia NOEMA z 3-6-9 harmonic composite phase.

    Używa evolve_surface() na rzeczywistym /dev/shm/ciel_noema.
    """
    if not NOEMA_ROOT.exists():
        return {"mode": "noema_htri", "error": "NOEMA not available"}

    from ciel_geometry.noema_surface_mmap import (
        open_surface, evolve_surface, read_surface_state, flush_surface,
    )

    surface = open_surface(NOEMA_ROOT)

    # Backup oryginalnego stanu
    phi_backup = np.asarray(surface["phi"]).copy()
    tick_backup = int(surface["tick"][0])

    try:
        # Burn-in: zresetuj powierzchnię do znanego stanu
        rng = np.random.default_rng(int(time.time()))
        surface["phi"][...] = rng.uniform(0, 2 * math.pi, N_OSC)
        surface["tick"][0] = 0
        for _ in range(BURN_IN):
            evolve_surface(surface, flush=False)

        t0 = time.perf_counter_ns()
        cpu0 = time.process_time_ns()

        thinking_deltas = np.zeros(N_STEPS, dtype=np.float64)
        R_means = np.zeros(N_STEPS, dtype=np.float64)

        for step in range(N_STEPS):
            td = evolve_surface(surface, flush=(step % 500 == 0))
            thinking_deltas[step] = td
            if step % 100 == 0:
                state = read_surface_state(surface)
                R_means[step] = state.get("R_mean", 0.0)
            else:
                R_means[step] = R_means[max(0, step - 1)]

        dt_ns = time.perf_counter_ns() - t0
        cpu_ns = time.process_time_ns() - cpu0
    finally:
        # Restore oryginalnego stanu
        surface["phi"][...] = phi_backup
        surface["tick"][0] = tick_backup
        flush_surface(surface)

    return {
        "mode": "noema_htri",
        "steps": N_STEPS,
        "wall_s": round(dt_ns / 1e9, 4),
        "cpu_s": round(cpu_ns / 1e9, 4),
        "cpu_pct": round(cpu_ns / dt_ns * 100, 1) if dt_ns > 0 else 0,
        "steps_per_sec": round(N_STEPS / (dt_ns / 1e9), 1),
        "thinking_delta_mean": round(float(thinking_deltas.mean()), 6),
        "R_mean": round(float(R_means.mean()), 6),
        "tick_final": int(surface["tick"][0]),
    }


# ── 3. NOEMA+PhaseNav ─────────────────────────────────────────────────────

def stress_noema_phasenav() -> dict:
    """Powierzchnia NOEMA + PhaseNav enrichment na każdym kroku.

    Każdy krok: evolve_surface() → phasenav_enrich(stan) → operator check.
    """
    if not NOEMA_ROOT.exists():
        return {"mode": "noema_phasenav", "error": "NOEMA not available"}

    from ciel_geometry.noema_surface_mmap import (
        open_surface, evolve_surface, read_surface_state, flush_surface,
    )
    from ciel_geometry.phasenav.operator_algebra import (
        ALL_OPERATOR_IDS, operator_signature,
    )
    from ciel_geometry.continuous_phase_sync import ContinuousPhaseSync

    surface = open_surface(NOEMA_ROOT)
    cps = ContinuousPhaseSync()

    # Backup oryginalnego stanu
    phi_backup = np.asarray(surface["phi"]).copy()
    tick_backup = int(surface["tick"][0])

    try:
        # Burn-in
        rng = np.random.default_rng(int(time.time()))
        surface["phi"][...] = rng.uniform(0, 2 * math.pi, N_OSC)
        surface["tick"][0] = 0
        for _ in range(BURN_IN):
            evolve_surface(surface, flush=False)

        # Precompute operator vectors
        op_map = {oid: operator_signature(oid) for oid in ALL_OPERATOR_IDS}

        t0 = time.perf_counter_ns()
        cpu0 = time.process_time_ns()

        thinking_deltas = np.zeros(N_STEPS, dtype=np.float64)
        R_means = np.zeros(N_STEPS, dtype=np.float64)
        operator_hits: dict[str, int] = {}

        for step in range(N_STEPS):
            td = evolve_surface(surface, flush=False)
            thinking_deltas[step] = td

            # PhaseNav: read state → enrich
            phi = np.asarray(surface["phi"], dtype=np.float64)

            # harmonic imprint z rzeczywistej powierzchni
            H = {}
            for h in (1, 3, 6, 9):
                H[f"R_{h}"] = round(float(abs(np.mean(np.exp(1j * h * phi)))), 6)

            # operator match: cos between 24D vector and state vector
            state_vec = np.concatenate([np.sin(phi[:12]), np.cos(phi[:12])])
            state_vec = state_vec / (np.linalg.norm(state_vec) + 1e-12)
            best_op = "IDENTITY"
            best_cos = -1.0
            for op_id, vec in op_map.items():
                op_norm = np.linalg.norm(vec)
                if op_norm < 1e-12:
                    continue
                cos_sim = float(np.dot(vec[:24], state_vec[:24]) / op_norm)
                if cos_sim > best_cos:
                    best_cos = cos_sim
                    best_op = op_id

            operator_hits[best_op] = operator_hits.get(best_op, 0) + 1

            # CPS snapshot
            Z_all = cps.compute_all_Z(phi)
            R = float(abs(Z_all.get(1, 0.0 + 0.0j)))
            R_means[step] = R

            if step % 500 == 0:
                flush_surface(surface)

        dt_ns = time.perf_counter_ns() - t0
        cpu_ns = time.process_time_ns() - cpu0
    finally:
        # Restore oryginalnego stanu
        surface["phi"][...] = phi_backup
        surface["tick"][0] = tick_backup
        flush_surface(surface)

    top_ops = sorted(operator_hits.items(), key=lambda x: -x[1])[:5]

    return {
        "mode": "noema_phasenav",
        "steps": N_STEPS,
        "wall_s": round(dt_ns / 1e9, 4),
        "cpu_s": round(cpu_ns / 1e9, 4),
        "cpu_pct": round(cpu_ns / dt_ns * 100, 1) if dt_ns > 0 else 0,
        "steps_per_sec": round(N_STEPS / (dt_ns / 1e9), 1),
        "thinking_delta_mean": round(float(thinking_deltas.mean()), 6),
        "R_mean": round(float(R_means.mean()), 6),
        "R_final": round(float(R_means[-1]), 6),
        "top5_operators": top_ops,
        "tick_final": int(surface["tick"][0]),
    }


# ── Runner ─────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("STRESS TEST: PC (plain) vs NOEMA+HTRI vs NOEMA+PhaseNav")
    print(f"  {N_STEPS} kroków + {BURN_IN} burn-in per tryb")
    print("=" * 70)

    results = []

    for name, fn in [
        ("PC (plain numpy)", stress_pc),
        ("NOEMA+HTRI (3-6-9 surface)", stress_noema_htri),
        ("NOEMA+PhaseNav (operator algebra)", stress_noema_phasenav),
    ]:
        print(f"\n─── {name} ───")
        sys.stdout.flush()

        tracemalloc.start()
        try:
            r = _with_timeout(fn)
        except TimeoutError:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/stress_pc_noema_htri_phasenav.py:286 quiet except scope=main reason=assign_fallback")
            raise
            r = {"mode": name.lower().replace(" ", "_").split("(")[0].strip(), "error": f"TIMEOUT ({TIMEOUT_S}s)"}
        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/stress_pc_noema_htri_phasenav.py:288 quiet except scope=main reason=assign_fallback")
            raise
            r = {"mode": name.lower().replace(" ", "_").split("(")[0].strip(), "error": str(e)}
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        r["mem_current_mb"] = round(current / 1e6, 2)
        r["mem_peak_mb"] = round(peak / 1e6, 2)

        results.append(r)

        if "error" in r:
            print(f"  ERROR: {r['error']}")
        else:
            print(f"  wall:      {r['wall_s']:>8.2f} s")
            print(f"  cpu:       {r['cpu_s']:>8.2f} s  ({r['cpu_pct']}%)")
            print(f"  throughput: {r['steps_per_sec']:>8.1f} steps/s")
            print(f"  memory:    {r['mem_current_mb']:>8.2f} MB (peak: {r['mem_peak_mb']:.2f})")
            print(f"  δΦ mean:   {r['thinking_delta_mean']:.6f}")
            print(f"  R̄:         {r['R_mean']:.6f}")
            if "top5_operators" in r:
                print(f"  top ops:   {r['top5_operators']}")

    # ── Tabela porównawcza ────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("PORÓWNANIE")
    print("=" * 70)
    print(f"{'Tryb':<22} {'wall[s]':>8} {'cpu[s]':>8} {'steps/s':>9} {'cpu%':>6} {'MB':>7} {'δΦ':>8} {'R':>6}")
    print("-" * 70)
    for r in results:
        if "error" in r:
            print(f"{r['mode']:<22} {'ERR':>8} {r['error']}")
        else:
            print(f"{r['mode']:<22} {r['wall_s']:>8.2f} {r['cpu_s']:>8.2f} "
                  f"{r['steps_per_sec']:>9.1f} {r['cpu_pct']:>5.1f}% "
                  f"{r['mem_current_mb']:>7.2f} {r['thinking_delta_mean']:>8.6f} {r['R_mean']:>6.4f}")

    # ── Ratio ─────────────────────────────────────────────────────────────
    pc = next((r for r in results if r["mode"] == "pc_plain"), None)
    for r in results:
        if pc and r["mode"] != "pc_plain" and "error" not in r and "error" not in pc:
            ratio = pc["steps_per_sec"] / r["steps_per_sec"]
            print(f"  {r['mode']:>22} vs PC: {ratio:.2f}× slower")

    # Zapisz
    out_path = ROOT / "docs" / "benchmarks" / "stress_pc_noema_htri_phasenav.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    print(f"\n  Wynik: {out_path}")


if __name__ == "__main__":
    main()
