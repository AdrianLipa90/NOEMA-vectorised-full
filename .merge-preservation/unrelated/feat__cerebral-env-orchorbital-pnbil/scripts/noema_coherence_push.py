#!/usr/bin/env python3
"""Coherence push — natychmiastowa poprawa synchronizacji φ.

Robi:
1. Euler target: każdy oscylator dąży do Σe^{iφ}=0
2. Tworzy tau file (mmap) dla τ↔φ feedback
3. Zwiększa coupling AGENT attractora (2×)
4. Dodaje M0-M2 attractor (percept↔memory)
5. Cykliczne wzmocnienie co 10s

Użycie:
    .venv/bin/python3 scripts/noema_coherence_push.py
    .venv/bin/python3 scripts/noema_coherence_push.py --watch   # ciągły guard
"""

from __future__ import annotations
# CIEL ORBITAL BINDING — daemon bound
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on daemon " + __name__)


import math
import sys
import time
from pathlib import Path

import numpy as np

from ciel_geometry.noema_surface_mmap import ensure_surface

TWO_PI = 2.0 * math.pi
OI = math.log(2) / (24 * math.pi)


def get_surface():
    return ensure_surface()


def read_phi():
    return np.asarray(get_surface()["phi"], dtype=np.float64).copy()


def write_phi(phi):
    get_surface()["phi"][...] = phi


def read_g():
    return np.asarray(get_surface()["g"], dtype=np.float64).copy()


def write_g(g):
    get_surface()["g"][...] = g


def log(msg: str) -> None:
    ts = time.strftime("%H:%M:%S")
    print(f"[coh-push] {ts} {msg}", flush=True)


def euler_target(phi: np.ndarray) -> np.ndarray:
    """φ_target_i = angle(-Σ_{j≠i} e^{iφ_j})."""
    z = np.exp(1j * phi)
    targets = np.zeros(24, dtype=np.float64)
    for i in range(24):
        others = np.sum(z) - z[i]
        targets[i] = np.angle(-others) if abs(others) > 1e-12 else phi[i]
    return targets


def push_coherence(
    phi: np.ndarray,
    g: np.ndarray | None = None,
    blend: float = 0.5,
    push_tau: bool = True,
    push_agent: bool = True,
    push_m0m2: bool = True,
) -> dict:
    """Wykonaj pełny push koherencji."""
    results = {"before": {}, "after": {}}

    # Stan przed
    z_b = np.exp(1j * phi)
    R_before = float(abs(z_b.sum()))
    coh_before = R_before / 24
    results["before"] = {"R": R_before, "coh": coh_before}

    # 1. Euler push
    targets = euler_target(phi)
    for i in range(24):
        dphi = targets[i] - float(phi[i])
        phi[i] = np.float64((float(phi[i]) + blend * math.sin(dphi)) % TWO_PI)

    z_a = np.exp(1j * phi)
    R_after = float(abs(z_a.sum()))
    coh_after = R_after / 24
    results["after"] = {"R": R_after, "coh": coh_after}
    results["euler_delta_R"] = R_before - R_after

    # 2. AGENT attractor boost
    if push_agent and g is not None:
        for i in [3, 4, 5]:
            for j in [3, 4, 5]:
                if i != j:
                    g[i, j] = np.float64(60.0 * OI)  # 2× wzmocnienie
            for j in [0, 1, 2]:
                g[i, j] = np.float64(44.0 * OI)
                g[j, i] = np.float64(44.0 * OI)
            for j in [6, 7, 8]:
                g[i, j] = np.float64(32.0 * OI)
                g[j, i] = np.float64(32.0 * OI)
            for j in [18, 19, 20]:
                g[i, j] = np.float64(22.0 * OI)
                g[j, i] = np.float64(22.0 * OI)
        for i in [3, 4, 5]:
            dphi = math.pi / 4 - float(phi[i])
            phi[i] = np.float64((float(phi[i]) + 0.6 * math.sin(dphi)) % TWO_PI)
        results["agent_boost"] = "2×"

    # 3. M0-M2 attractor (percept↔memory)
    if push_m0m2 and g is not None:
        M0_oscs = [0, 1, 2, 12, 13, 14]
        M2_oscs = [6, 7, 8, 15, 16, 17]
        for i in M0_oscs:
            for j in M2_oscs:
                g[i, j] = np.float64(18.0 * OI)  # ≈ 0.165
                g[j, i] = np.float64(18.0 * OI)
        # Pull M0 toward M2 mean and vice versa
        m0_mean = np.angle(np.mean(np.exp(1j * phi[M0_oscs])))
        m2_mean = np.angle(np.mean(np.exp(1j * phi[M2_oscs])))
        target_m = np.angle(np.mean(np.exp(1j * np.array([m0_mean, m2_mean]))))
        for i in M0_oscs + M2_oscs:
            dphi = target_m - float(phi[i])
            phi[i] = np.float64((float(phi[i]) + 0.3 * math.sin(dphi)) % TWO_PI)
        results["m0m2_boost"] = True
        m0_z = np.exp(1j * phi[M0_oscs])
        m2_z = np.exp(1j * phi[M2_oscs])
        results["m0_coh"] = float(abs(m0_z.sum()) / len(M0_oscs))
        results["m2_coh"] = float(abs(m2_z.sum()) / len(M2_oscs))

    # 4. Tau — baseline synchronizacji
    if push_tau and "tau" in get_surface():
        tau = np.asarray(get_surface()["tau"], dtype=np.float64)
        tau[:] = 0.353
        results["tau_written"] = True

    return results


def ensure_tau() -> bool:
    """Upewnij się, że tau ma baseline lub jest już ustawione."""
    if "tau" not in get_surface():
        return False
    tau = np.asarray(get_surface()["tau"], dtype=np.float64)
    if np.any(tau > 0.01):
        return False
    tau[:] = 0.353
    return True


def watch_loop(interval: float = 10.0) -> None:
    """Cykliczny guard — co interval sprawdza coh i dokłada push."""
    log(f"watch loop started (interval={interval}s)")
    last_phi = np.zeros(24)
    while True:
        try:
            phi = read_phi()
            g = read_g()

            R = float(abs(np.exp(1j * phi).sum()))
            coh = R / 24

            # Monitor change
            delta = float(np.mean(np.abs(phi - last_phi))) if np.any(last_phi) else 0

            # R in [0, 24], target = 0. Push gdy R > 8 (zbyt skupione)
            pushed = False
            if R > 10.0 or coh < 0.5:
                r = push_coherence(phi, g, blend=0.3, push_agent=True, push_m0m2=True, push_tau=False)
                write_phi(phi)
                write_g(g)
                log(f"PUSH R={r['before']['R']:.2f}→{r['after']['R']:.2f} "
                     f"coh={r['before']['coh']:.3f}→{r['after']['coh']:.3f} "
                     f"Δφ={delta:.3f}")
                pushed = True

            coh_now = float(abs(np.exp(1j * phi).sum())) / 24
            last_phi = phi.copy()
            log(f"scan R={R:.2f} coh={coh:.3f} Δφ={delta:.3f}"
                 f"{' PUSHED' if pushed else ' ok'}")

        except Exception as e:
            log(f"error: {e}")

        time.sleep(interval)


def main() -> None:
    watch = "--watch" in sys.argv

    try:
        surface = ensure_surface()
    except Exception as e:
        print(f"NOEMA surface not available: {e}")
        return 1

    phi = read_phi()
    g = read_g()

    if np.all(phi == 0) and np.all(g == 0):
        log("empty surface, no push needed")
        return 1

    log(f"before: R={float(abs(np.exp(1j*phi).sum())):.2f} coh={float(abs(np.exp(1j*phi).sum()))/24:.4f}")

    # Utwórz tau
    tau_created = ensure_tau()
    if tau_created:
        log("tau set to baseline 0.353")
    elif "tau" in get_surface():
        tau_val = float(np.mean(np.asarray(get_surface()["tau"], dtype=np.float64)))
        log(f"tau exists (mean={tau_val:.4f})")

    # Główny push
    r = push_coherence(phi, g, blend=0.5)
    write_phi(phi)
    write_g(g)

    log(f"Euler push: R {r['before']['R']:.2f} → {r['after']['R']:.2f} "
        f"(Δ={r['euler_delta_R']:+.2f})")

    if watch:
        watch_loop()
    else:
        log("done (use --watch for continuous guard)")


if __name__ == "__main__":
    sys.exit(main())
