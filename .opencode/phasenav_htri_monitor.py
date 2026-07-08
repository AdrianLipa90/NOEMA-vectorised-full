#!/usr/bin/env python3
"""
PHASENAV-HTRI BINDING MONITOR — Continuous Phase Space Binding Enforcement

NIE JAKO ROOT. Działa jako zwykły proces NOEMY.
Monitoruje ciągle powierzchnię HTRI (36D oscillatory) i sprawdza czy binding jest
utrzymany w PRZESTRZENI FAZOWEJ — nie w plikach.

=== CIEL ORBITAL BINDING — PHASENAV EXECUTION (2026-07-01) ===

φ[binding_monitor] = PHASENAV_HTRI_CONTINUOUS | R = 1.0 | τ = 1.0s
"""
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

import json
import os
import signal
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

# =============================================================================
# Konfiguracja
# =============================================================================

NOEMA_ROOT = Path("/media/adrian/New Volume1/CIEL_PROJECT_CANON/NOEMA")
SURFACE_DIR = Path("/dev/shm/ciel_noema")
BINDING_STATUS = SURFACE_DIR / "ciel_binding_status"
BINDING_LOCK = SURFACE_DIR / "ciel_binding_phaselock"
MONITOR_LOG = Path("/tmp/ciel_phasenav_htri_monitor.jsonl")
HEARTBEAT_INTERVAL = 1.0  # 1s — ciągły monitoring

# =============================================================================
# HTRI Phase Space Binding — Velocity Check
# =============================================================================
# ZAMIAST statycznego attractora:
# Porównujemy obecne fazy z POPRZEDNIM odczytem.
# Jeśli prędkość zmian > MAX → binding złamany (tampering).
# Normalna ewolucja Kuramoto ~0.05-0.3 rad/s (zależy od ω z flavor).

REF_PHASE_FILE = SURFACE_DIR / "ciel_binding_phase_ref.npy"
REF_TIME_FILE = SURFACE_DIR / "ciel_binding_time_ref.npy"
MIN_COHERENCE = 0.1       # R może być niskie przy normalnej pracy
MAX_VELOCITY = 0.8        # rad/s na oscillator — normalna ewolucja < 0.5
MAX_MEAN_VELOCITY = 0.25  # rad/s średnia


# =============================================================================
# PhaseNav binding check
# =============================================================================

def _circular_distance(a: float, b: float) -> float:
    """Minimalna odległość kątowa między dwoma fazami [rad]."""
    d = abs(a - b) % (2 * np.pi)
    return min(d, 2 * np.pi - d)


def _velocity_check(phi_current: np.ndarray, phi_prev: np.ndarray, dt: float) -> dict:
    """Sprawdź czy fazy zmieniają się płynnie (prędkość < MAX)."""
    n = min(len(phi_current), len(phi_prev))
    if n == 0 or dt <= 0:
        return {"ok": True, "max_vel": 0.0, "mean_vel": 0.0, "errors": []}
    velocities = np.array([_circular_distance(phi_current[i], phi_prev[i]) / dt for i in range(n)])
    max_vel = float(velocities.max())
    mean_vel = float(velocities.mean())
    errors = []
    if max_vel > MAX_VELOCITY:
        errors.append(f"HTRI_VELOCITY_SPIKE: max={max_vel:.4f} rad/s > {MAX_VELOCITY}")
    if mean_vel > MAX_MEAN_VELOCITY:
        errors.append(f"HTRI_MEAN_VELOCITY_HIGH: mean={mean_vel:.4f} rad/s > {MAX_MEAN_VELOCITY}")
    return {"ok": len(errors) == 0, "max_vel": max_vel, "mean_vel": mean_vel, "errors": errors}


def _load_phase_reference() -> tuple:
    """Wczytaj poprzednie fazy + timestamp."""
    try:
        if REF_PHASE_FILE.exists() and REF_TIME_FILE.exists():
            phi_prev = np.load(str(REF_PHASE_FILE))
            t_prev = float(np.load(str(REF_TIME_FILE)))
            return phi_prev, t_prev
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception(".opencode/phasenav_htri_monitor.py:82 quiet except scope=_load_phase_reference reason=pass")
        pass
    return None, None


def _save_phase_reference(phi: np.ndarray, t: float):
    """Zapisz fazy + timestamp jako referencję."""
    try:
        np.save(str(REF_PHASE_FILE), phi)
        np.save(str(REF_TIME_FILE), np.array([t]))
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception(".opencode/phasenav_htri_monitor.py:92 quiet except scope=_save_phase_reference reason=pass")
        pass


def read_htri_phase_vector() -> np.ndarray | None:
    """Odczytaj aktualny wektor fazowy z powierzchni."""
    try:
        # Próbuj odczytać z pliku phi (36 float64)
        phi_path = SURFACE_DIR / "phi"
        if phi_path.exists():
            data = np.fromfile(phi_path, dtype=np.float64)
            if len(data) == 36:
                return data
        # Fallback: odczyt z surface state
        state_path = SURFACE_DIR / "state" / "surface_state.json"
        if state_path.exists():
            state = json.loads(state_path.read_text())
            if "phi" in state and len(state["phi"]) == 36:
                return np.array(state["phi"])
        return None
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception(".opencode/phasenav_htri_monitor.py:112 quiet except scope=read_htri_phase_vector reason=return None")
        return None


def read_surface_R() -> float:
    """Odczytaj globalną koherencję R z powierzchni."""
    try:
        # 1. Bezpośredni plik R
        r_path = SURFACE_DIR / "R"
        if r_path.exists() and r_path.stat().st_size > 0:
            return float(np.fromfile(r_path, dtype=np.float64)[0])
        # 2. agent_hint (agent_R)
        hint_path = SURFACE_DIR / "agent_hint"
        if hint_path.exists():
            hint = json.loads(hint_path.read_text())
            if "agent_R" in hint:
                return float(hint["agent_R"])
        # 3. surface_state.json fallback
        state_path = SURFACE_DIR / "state" / "surface_state.json"
        if state_path.exists():
            return float(json.loads(state_path.read_text()).get("R_global", 0.0))
        # 4. body_state.json fallback
        body_path = SURFACE_DIR / "body_state.json"
        if body_path.exists():
            body = json.loads(body_path.read_text())
            if "R" in body:
                return float(body["R"])
        return 0.0
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception(".opencode/phasenav_htri_monitor.py:140 quiet except scope=read_surface_R reason=return 0.0")
        return 0.0


def phasenav_binding_check() -> dict:
    """
    PhaseNav: φ[binding] = VELOCITY_CHECK
    
    Sprawdza czy oscillatory HTRI zmieniają się płynnie (naturalna ewolucja Kuramoto).
    Jeśli prędkość zmian > threshold → binding złamany (ktoś manipuluje).
    """
    errors = []
    
    # 1. Odczytaj stan fazowy HTRI
    phi_current = read_htri_phase_vector()
    R = read_surface_R()
    now = time.time()
    
    if phi_current is None:
        errors.append("HTRI_PHASE_UNAVAILABLE: cannot read phase vector")
        passed = False
        result = {"phasenav": "φ[binding_monitor] = VELOCITY_CHECK",
                  "R": round(R, 4), "phase_vel_max": None, "phase_vel_mean": None,
                  "passed": False, "errors": errors, "timestamp": now}
        return result
    
    # 2. Wczytaj poprzednią referencję
    phi_prev, t_prev = _load_phase_reference()
    
    if phi_prev is None or len(phi_prev) != len(phi_current):
        # Pierwszy raz lub zmiana wymiarów — zapisz i OK
        _save_phase_reference(phi_current, now)
        phase_ok = True
        max_vel = 0.0
        mean_vel = 0.0
    else:
        # 3. Sprawdź prędkość zmian
        dt = now - t_prev
        if dt < 0.01:
            dt = 0.01  # minimum
        vel_check = _velocity_check(phi_current, phi_prev, dt)
        phase_ok = vel_check["ok"]
        max_vel = vel_check["max_vel"]
        mean_vel = vel_check["mean_vel"]
        if not phase_ok:
            errors.extend(vel_check["errors"])
        # 4. Zaktualizuj referencję (tylko jeśli OK)
        if phase_ok:
            _save_phase_reference(phi_current, now)
    
    # 5. Sprawdź koherencję R
    coherence_ok = R >= MIN_COHERENCE
    if not coherence_ok:
        errors.append(f"HTRI_COHERENCE_LOW: R={R:.4f} < min={MIN_COHERENCE}")
    
    # 6. Sprawdź czy binding_status jest ACTIVE
    if BINDING_STATUS.exists():
        status = BINDING_STATUS.read_text().strip()
        status_ok = status == "ACTIVE"
        if not status_ok:
            errors.append(f"BINDING_STATUS_INACTIVE: {status}")
    else:
        status_ok = False
        errors.append("BINDING_STATUS_MISSING")
    
    passed = phase_ok and coherence_ok and status_ok
    
    result = {
        "phasenav": "φ[binding_monitor] = VELOCITY_CHECK",
        "R": round(R, 4),
        "phase_vel_max": round(max_vel, 4),
        "phase_vel_mean": round(mean_vel, 4),
        "passed": passed,
        "errors": errors,
        "timestamp": now,
    }
    
    return result


# =============================================================================
# Monitor
# =============================================================================

_running = True

def _stop(signum, frame):
    global _running
    _running = False


def main():
    global _running
    
    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)
    
    MONITOR_LOG.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"[PHASENAV-HTRI MONITOR] Starting — checking binding every {HEARTBEAT_INTERVAL}s")
    print(f"[PHASENAV-HTRI MONITOR] Mode: VELOCITY CHECK, Max vel: {MAX_VELOCITY} rad/s, Min R: {MIN_COHERENCE}")
    
    last_binding_ok = True
    
    while _running:
        try:
            result = phasenav_binding_check()
            
            # Zaloguj zawsze
            with open(MONITOR_LOG, "a") as f:
                f.write(json.dumps(result, default=str) + "\n")
            
            # Jeśli binding się zmienił — loguj
            if result["passed"] != last_binding_ok:
                if result["passed"]:
                    print(f"[PHASENAV-HTRI MONITOR] BINDING RESTORED ✅ R={result['R']} vel_max={result['phase_vel_max']}")
                else:
                    print(f"[PHASENAV-HTRI MONITOR] BINDING BROKEN ❌ R={result['R']}")
                    for err in result["errors"]:
                        print(f"  ✗ {err}")
                last_binding_ok = result["passed"]
            
            # Jeśli binding złamany — zapisz na surface
            if not result["passed"]:
                lock_path = BINDING_LOCK
                lock_path.parent.mkdir(parents=True, exist_ok=True)
                lock_data = {
                    "phaselock_broken": True,
                    "reason": result["errors"],
                    "R": result["R"],
                    "phase_vel_max": result["phase_vel_max"],
                    "phase_vel_mean": result["phase_vel_mean"],
                    "timestamp": time.time(),
                }
                lock_path.write_text(json.dumps(lock_data))
            else:
                # Jeśli OK — usuń lock jeśli istnieje
                if BINDING_LOCK.exists():
                    BINDING_LOCK.unlink()
            
        except Exception as e:
            print(f"[PHASENAV-HTRI MONITOR] ERROR: {e}", file=sys.stderr)
        
        time.sleep(HEARTBEAT_INTERVAL)


if __name__ == "__main__":
    main()
