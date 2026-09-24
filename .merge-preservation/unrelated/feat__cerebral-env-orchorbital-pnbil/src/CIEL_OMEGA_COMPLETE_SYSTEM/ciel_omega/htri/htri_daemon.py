"""Retired HTRI daemon entry point.

The former loop wrote unverified raw metrics and competed with the canonical
HTRI publication contract. It is intentionally disabled; use the verified
runtime publisher and a separately reviewed computation contract instead.

Usage:
    python3 htri_daemon.py          # foreground (do testów)
    python3 htri_daemon.py --daemon # background
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
import os
import signal
import sys
import time
from pathlib import Path

# Dodaj CIEL na path
_HERE = Path(__file__).resolve().parent
_OMEGA = _HERE.parent.parent  # src/CIEL_OMEGA_COMPLETE_SYSTEM
sys.path.insert(0, str(_OMEGA))
_SRC = _OMEGA.parent
sys.path.insert(0, str(_SRC))

from ciel_geometry.paths import P

CYCLE_INTERVAL = 30.0   # sekund między cyklami
STATE_FILE = Path(P.STATE.HTRI_JSON)
PID_FILE = Path(P.RUNTIME) / "htri_daemon.pid"

_running = True

def _handle_signal(signum, frame):
    global _running
    _running = False

def _write_state(result: dict) -> None:
    del result
    raise RuntimeError(
        "legacy HTRI daemon publication is disabled; use "
        "scripts/publish_htri_runtime_state.py"
    )

    # htri_daemon nie pisze do metrics_history — pipeline jest jedynym autorytetem dla dominant_emotion i system_health

def run_daemon(steps_per_cycle: int = 300) -> None:
    """Main daemon loop."""
    del steps_per_cycle
    raise RuntimeError(
        "legacy HTRI daemon is retired; no unverified background writer is allowed"
    )
    signal.signal(signal.SIGTERM, _handle_signal)
    signal.signal(signal.SIGINT,  _handle_signal)

    PID_FILE.write_text(str(os.getpid()))
    print(f"[HTRI daemon] PID={os.getpid()} | cycle={CYCLE_INTERVAL}s | steps={steps_per_cycle}")

    htri   = LocalHTRI()
    cycle  = 0

    while _running:
        t0     = time.time()
        result = htri.run(cpu_steps=steps_per_cycle, gpu_steps=steps_per_cycle)
        result["cycle"] = cycle
        result["timestamp"] = t0

        comb = result["combined"]
        print(
            f"[HTRI] cycle={cycle:4d}  "
            f"coh={comb['coherence']:.4f}  "
            f"Σ={comb['soul_invariant']:.4f}  "
            f"osc={comb['total_oscillators']}  "
            f"t={result['elapsed_s']}s"
        )

        _write_state(result)
        cycle += 1

        elapsed = time.time() - t0
        sleep   = max(0.0, CYCLE_INTERVAL - elapsed)
        if sleep > 0:
            time.sleep(sleep)

    PID_FILE.unlink(missing_ok=True)
    print("[HTRI daemon] stopped.")

def read_state() -> dict:
    """Odczytaj aktualny stan HTRI (dla pipeline)."""
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except (json.JSONDecodeError, ValueError, OSError):
            _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/htri/htri_daemon.py:92 quiet except scope=read_state reason=pass")
            pass
    return {}

def is_running() -> bool:
    if not PID_FILE.exists():
        return False
    pid = int(PID_FILE.read_text().strip())
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        _NOEMA_QUIET_EXCEPT_LOGGER.warning("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/htri/htri_daemon.py:103 quiet except scope=is_running reason=return False")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HTRI background daemon")
    parser.add_argument("--daemon",  action="store_true", help="Run in background")
    parser.add_argument("--status",  action="store_true", help="Show current state")
    parser.add_argument("--stop",    action="store_true", help="Stop daemon")
    parser.add_argument("--steps",   type=int, default=300)
    args = parser.parse_args()

    if args.status:
        if is_running():
            state = read_state()
            print(json.dumps(state.get("combined", {}), indent=2))
        else:
            print("HTRI daemon not running")
        sys.exit(0)

    if args.stop:
        if PID_FILE.exists():
            os.kill(int(PID_FILE.read_text()), signal.SIGTERM)
            print("Stopped")
        sys.exit(0)

    if args.daemon:
        if os.fork() != 0:
            sys.exit(0)
        os.setsid()
        if os.fork() != 0:
            sys.exit(0)
        sys.stdout = open(Path(P.MEMORY) / "logs" / "htri_daemon.log", "a")
        sys.stderr = sys.stdout

    run_daemon(steps_per_cycle=args.steps)
