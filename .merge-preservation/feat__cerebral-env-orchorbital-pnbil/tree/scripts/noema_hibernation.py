#!/usr/bin/env python3
"""NOEMA Surface Hibernacja — zapis/odczyt stanu powierzchni na dysk.

Zapisuje co 5 minut do katalogu hibernacji wyliczonego z HOME.
Przy starcie ładuje ostatni zapisany stan.
Przeżywa reboot.
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import os
import pickle
import signal
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import numpy as np
from ciel_geometry.noema_surface_mmap import (
    open_surface, N_OSCILLATORS, N_FLAVORS, DEFAULT_SURFACE_ROOT,
)

HIBER_DIR = Path(os.environ.get("HOME", "/tmp")) / ".noema_hibernation"
SAVE_INTERVAL = 300  # 5 min


def save(surface: dict) -> None:
    HIBER_DIR.mkdir(parents=True, exist_ok=True)
    state = {
        "phi": np.asarray(surface["phi"]).copy(),
        "omega": np.asarray(surface["omega"]).copy(),
        "g": np.asarray(surface["g"]).copy(),
        "flavor": np.asarray(surface["flavor"]).copy(),
        "tick": int(np.asarray(surface["tick"]).copy()[0]),
        "timestamp": time.time(),
    }
    path = HIBER_DIR / "surface_state.pkl"
    tmp = path.with_suffix(".pkl.tmp")
    with open(tmp, "wb") as f:
        pickle.dump(state, f)
    tmp.rename(path)  # atomic
    return state


def load() -> dict | None:
    path = HIBER_DIR / "surface_state.pkl"
    if not path.exists():
        return None
    try:
        with open(path, "rb") as f:
            state = pickle.load(f)
        age = time.time() - state.get("timestamp", 0)
        if age > 86400 * 7:  # older than a week — stale
            return None
        return state
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_hibernation.py:58 quiet except scope=load reason=return None")
        raise
        return None


def restore(surface: dict) -> bool:
    state = load()
    if state is None:
        return False
    surface["phi"][...] = state["phi"]
    surface["omega"][...] = state["omega"]
    surface["g"][...] = state["g"]
    surface["flavor"][...] = state["flavor"]
    surface["tick"][0] = state["tick"]
    from ciel_geometry.noema_surface_mmap import flush_surface
    flush_surface(surface)
    return True


def main():
    surface = open_surface(DEFAULT_SURFACE_ROOT)
    restored = restore(surface)
    if restored:
        print(f"[hiber] przywrócono stan z tick={surface['tick'][0]}")
    else:
        print("[hiber] brak zapisanego stanu — start fresh")

    running = True
    def _handler(signum, frame):
        nonlocal running; running = False
    signal.signal(signal.SIGINT, _handler)
    signal.signal(signal.SIGTERM, _handler)

    last_save = 0
    while running:
        now = time.time()
        if now - last_save >= SAVE_INTERVAL:
            s = save(surface)
            print(f"[hiber] saved tick={s['tick']}", flush=True)
            last_save = now
        try:
            time.sleep(10)
        except KeyboardInterrupt:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_hibernation.py:99 quiet except scope=main reason=break")
            raise
            break

    # Final save on exit
    s = save(surface)
    print(f"[hiber] final save tick={s['tick']}", flush=True)


if __name__ == "__main__":
    main()
