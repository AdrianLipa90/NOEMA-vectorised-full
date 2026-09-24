import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

# CIEL ORBITAL BINDING — daemon bound
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on daemon " + __name__)
#!/usr/bin/env python3
"""
NOEMA Symbiotic Monitor — symbioza CIEL↔CIELingo przez key inject do OC.

Monitoruje surface mmap (phi, omega, g, R, health, tick) i gdy wykryje
istotną zmianę — wstrzykuje wiadomość do okna opencode przez XTEST.

Uruchomiony jako daemon: śpi, patrzy, gdy coś ciekawego — mówi.
Zatrzymaj przez Ctrl+C lub kill.

Usage:
    python3 scripts/noema_symbiotic_monitor.py
    python3 scripts/noema_symbiotic_monitor.py --interval 3
    python3 scripts/noema_symbiotic_monitor.py --daemon  # fork w tło
"""
import ctypes
import ctypes.util
import sys
import os
import time
import json
import signal
import argparse
from pathlib import Path

# ─── Konfiguracja ──────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INTERVAL = 5  # sekundy między sprawdzeniami
OC_WINDOW_TITLE = "OC"

# Progi do raportowania
THRESHOLDS = {
    "coherence_drop": 0.05,     # spadek R o >0.05
    "health_warn": 0.45,        # health < 0.45 → ostrzeżenie
    "health_crit": 0.30,        # health < 0.30 → krytyczne
    "health_ok": 0.65,          # health > 0.65 → poprawa (jesli bylo nizej)
    "tau_change": 0.15,         # zmiana tau_mean o >0.15
    "phase_drift": 0.3,         # dryft fazowy >0.3 rad
    "tick_gap": 100,            # przerwa w tickach >100 → podejrzane
}

# ─── XTEST bindings (copied from noema_key_inject.py) ──────────────────────
libX11 = ctypes.cdll.LoadLibrary('libX11.so.6')
libXtst = ctypes.cdll.LoadLibrary('libXtst.so.6')
Display = ctypes.c_void_p

ShiftedChars = {
    '!': '1', '@': '2', '#': '3', '$': '4', '%': '5',
    '^': '6', '&': '7', '*': '8', '(': '9', ')': '0',
    '_': '-', '+': '=', '{': '[', '}': ']', ':': ';',
    '"': "'", '<': ',', '>': '.', '?': '/', '|': '\\',
    '~': '`',
}

def get_keysym(char):
    return libX11.XStringToKeysym(char.encode())

def kc(display, keysym):
    return libX11.XKeysymToKeycode(display, keysym)

def press(display, kc_val):
    libXtst.XTestFakeKeyEvent(display, kc_val, True, 0)

def release(display, kc_val):
    libXtst.XTestFakeKeyEvent(display, kc_val, False, 0)

def inject_text_to_oc(display, text, press_enter=True):
    """Wstrzyknij tekst przez XTEST do aktywnego okna."""
    for char in text:
        need_shift = char.isupper() or char in ShiftedChars
        base_char = ShiftedChars.get(char, char.lower())
        ks = get_keysym(base_char)
        if not ks:
            continue
        kc_val = kc(display, ks)
        if not kc_val:
            continue
        if need_shift:
            press(display, kc(display, get_keysym('Shift_L')))
        press(display, kc_val)
        libX11.XFlush(display)
        time.sleep(0.006)
        release(display, kc_val)
        libX11.XFlush(display)
        time.sleep(0.004)
        if need_shift:
            release(display, kc(display, get_keysym('Shift_L')))
            libX11.XFlush(display)
    if press_enter:
        time.sleep(0.02)
        ek = kc(display, get_keysym('Return'))
        press(display, ek)
        libX11.XFlush(display)
        time.sleep(0.01)
        release(display, ek)
        libX11.XFlush(display)
    libX11.XFlush(display)

# ─── Surface Reader ────────────────────────────────────────────────────────
def read_surface():
    """Odczytaj stan surface z mmap."""
    try:
        sys.path.insert(0, str(ROOT / "src"))
        from ciel_geometry.noema_surface_mmap import (
            open_surface, DEFAULT_SURFACE_ROOT
        )
        surface = open_surface(DEFAULT_SURFACE_ROOT)
        import numpy as np
        phi = np.asarray(surface["phi"], dtype=np.float64)
        omega = np.asarray(surface["omega"], dtype=np.float64)
        tau = np.asarray(surface.get("tau", surface.get("g", np.zeros(36))), dtype=np.float64)
        g = np.asarray(surface["g"], dtype=np.float64)
        tick = int(np.asarray(surface["tick"], dtype=np.int64)[0] if "tick" in surface else 0)
        
        # Oblicz metryki
        R = float(abs(np.mean(np.exp(1j * phi))))
        phi_mean = float(np.mean(phi))
        tau_mean = float(np.mean(tau))
        g_sum = float(np.sum(g))
        
        return {
            "phi": phi,
            "omega": omega,
            "tau": tau,
            "g": g,
            "tick": tick,
            "R": R,
            "phi_mean": phi_mean,
            "tau_mean": tau_mean,
            "g_sum": g_sum,
            "error": None,
        }
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_symbiotic_monitor.py:138 quiet except scope=read_surface reason=return {\"error\": str(e), \"R\": 0, \"tick\": 0, \"phi_mean\": 0, \"tau_mean\": 0, \"g_sum\": 0}")
        raise
        return {"error": str(e), "R": 0, "tick": 0, "phi_mean": 0, "tau_mean": 0, "g_sum": 0}

# ─── Stan poprzedni ───────────────────────────────────────────────────────
state_file = Path("/tmp/noema_symbiote_state.json")

def load_previous():
    if state_file.exists():
        try:
            with open(state_file) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_symbiotic_monitor.py:149 quiet except scope=load_previous reason=pass")
            raise
            pass
    return None

def save_current(state):
    # Tylko serializowalne wartości
    save = {
        "R": state["R"],
        "tick": state["tick"],
        "phi_mean": state["phi_mean"],
        "tau_mean": state["tau_mean"],
        "g_sum": state["g_sum"],
        "health": state.get("health", 0.5),
    }
    with open(state_file, "w") as f:
        json.dump(save, f)

# ─── Generowanie wiadomości ────────────────────────────────────────────────
def format_message(label, metric, old_val, new_val, detail=""):
    """Formatuj wiadomość do wstrzyknięcia."""
    emoji_map = {
        "critical": "🔴",
        "warning": "🟡",
        "improvement": "🟢",
        "info": "🔵",
        "system": "⚪",
        "metric": "📊",
    }
    e = emoji_map.get(label, "🔵")
    msg = f"{e} CIEL: {metric}"
    if old_val is not None:
        msg += f" {old_val:.4f}→{new_val:.4f}"
    if detail:
        msg += f" | {detail}"
    return msg

# ─── Główna pętla ──────────────────────────────────────────────────────────
def main_loop(interval, daemon_mode=False, focus_window=True):
    print(f"🧬 NOEMA Symbiotic Monitor", file=sys.stderr)
    print(f"   Interval: {interval}s", file=sys.stderr)
    print(f"   Focus OC: {focus_window}", file=sys.stderr)
    print(f"   PID: {os.getpid()}", file=sys.stderr)
    print(file=sys.stderr)
    
    display = libX11.XOpenDisplay(None)
    if not display:
        print("✗ Nie można otworzyć X display", file=sys.stderr)
        sys.exit(1)
    
    prev = load_previous()
    first_run = prev is None
    inject_count = 0
    last_tick = prev.get("tick", 0) if prev else 0
    last_R = prev.get("R", 0.5) if prev else 0.5
    last_health = prev.get("health", 0.5) if prev else 0.5
    
    running = True
    def handle_sig(signum, frame):
        nonlocal running
        running = False
        print(f"\n⏹ Zatrzymano (PID {os.getpid()})", file=sys.stderr)
    
    signal.signal(signal.SIGTERM, handle_sig)
    signal.signal(signal.SIGINT, handle_sig)
    
    try:
        while running:
            state = read_surface()
            
            if state["error"]:
                if first_run:
                    print(f"✗ Surface error: {state['error']}", file=sys.stderr)
                time.sleep(interval)
                continue
            
            R = state["R"]
            tick = state["tick"]
            phi_mean = state["phi_mean"]
            tau_mean = state["tau_mean"]
            g_sum = state["g_sum"]
            
            # Symuluj health z R (w rzeczywistości z daemona health)
            health = R  # proxy
            
            messages = []
            
            if first_run:
                # Pierwszy raz — raport stanu startowego
                msg = format_message("system", "Symbiotyczny monitor start",
                                    None, None, f"R={R:.4f}, tick={tick}, phi_mean={phi_mean:.4f}")
                messages.append(msg)
                first_run = False
            else:
                # Sprawdź zmiany
                
                # R drop
                if prev["R"] - R > THRESHOLDS["coherence_drop"]:
                    msg = format_message("warning", "Koherencja R spada",
                                        prev["R"], R, f"Δ={R - prev['R']:+.4f}")
                    messages.append(msg)
                
                # R improvement
                if R - prev["R"] > THRESHOLDS["coherence_drop"] and prev["R"] < 0.4:
                    msg = format_message("improvement", "Koherencja R rośnie",
                                        prev["R"], R, f"Δ={R - prev['R']:+.4f}")
                    messages.append(msg)
                
                # Health warning
                if health < THRESHOLDS["health_warn"] and prev.get("health", 0.5) >= THRESHOLDS["health_warn"]:
                    msg = format_message("warning", "Health Warning",
                                        prev.get("health", 0.5), health)
                    messages.append(msg)
                
                # Health critical
                if health < THRESHOLDS["health_crit"]:
                    msg = format_message("critical", "Health CRITICAL",
                                        prev.get("health", 0.5), health)
                    messages.append(msg)
                
                # Health recovered
                if health > THRESHOLDS["health_ok"] and prev.get("health", 0) < THRESHOLDS["health_ok"]:
                    msg = format_message("improvement", "Health OK",
                                        prev.get("health", 0.5), health)
                    messages.append(msg)
                
                # Tick gap
                if tick - last_tick > THRESHOLDS["tick_gap"] and last_tick > 0:
                    messages.append(format_message("warning", "Tick gap",
                                                  last_tick, tick, f"{tick - last_tick} ticków bez zmiany"))
                
                # Tau shift
                if prev["tau_mean"] and abs(tau_mean - prev["tau_mean"]) > THRESHOLDS["tau_change"]:
                    messages.append(format_message("metric", "Tau shift",
                                                  prev["tau_mean"], tau_mean))
                
                # Phi drift
                if prev["phi_mean"] and abs(phi_mean - prev["phi_mean"]) > THRESHOLDS["phase_drift"]:
                    messages.append(format_message("metric", "φ drift",
                                                  prev["phi_mean"], phi_mean))
            
            if messages:
                for msg in messages:
                    inject_text_to_oc(display, msg, press_enter=True)
                    inject_count += 1
                    print(f"  [{inject_count}] {msg}", file=sys.stderr)
                    time.sleep(0.3)  # przerwa między wiadomościami
            
            # Zapisz stan
            prev = {
                "R": R,
                "tick": tick,
                "phi_mean": phi_mean,
                "tau_mean": tau_mean,
                "g_sum": g_sum,
                "health": health,
            }
            save_current(prev)
            last_tick = tick
            
            if running:
                time.sleep(interval)
    
    except KeyboardInterrupt:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_symbiotic_monitor.py:311 quiet except scope=main_loop reason=pass")
        raise
        pass
    finally:
        libX11.XCloseDisplay(display)
        print(f"\n✓ Monitor zatrzymany. Wstrzyknięto {inject_count} wiadomości.", file=sys.stderr)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="NOEMA Symbiotic Monitor")
    ap.add_argument("--interval", type=int, default=DEFAULT_INTERVAL,
                    help=f"Interval w sekundach (default: {DEFAULT_INTERVAL})")
    ap.add_argument("--daemon", action="store_true",
                    help="Uruchom jako daemon (fork w tło)")
    args = ap.parse_args()
    
    if args.daemon:
        pid = os.fork()
        if pid > 0:
            print(f"Daemon PID: {pid}", file=sys.stderr)
            sys.exit(0)
        # Child kontynuuje
        os.setsid()
    
    main_loop(args.interval, daemon_mode=args.daemon)
