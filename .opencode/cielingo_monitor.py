#!/usr/bin/env python3
"""CIELingo monitor — odczyt stanu dla agenta opencode.

Uruchamiany na starcie sesji: python3 .opencode/cielingo_monitor.py
Zwraca JSON z bieżącym stanem CIELingo + NOEMA surface.

Używany przez agenta do sprawdzenia czy CIELingo żyje, jakie ma stany,
czy są nowe hinty w agent_hint.
"""
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import os
import sys
from pathlib import Path

SHM = Path("/dev/shm/ciel_noema")
HINT_FILE = SHM / "agent_hint"
CLOSURE_FILE = SHM / "closure"
IMAGINAL_FILE = SHM / "imaginal_drive"
PHI_FILE = SHM / "phi"
OMEGA_FILE = SHM / "omega"
FLAVOR_FILE = SHM / "flavor"
GRAVITY_FILE = SHM / "gravity"
HOLONOMY_FILE = SHM / "holonomy"
TICK_FILE = SHM / "tick"
HEALTH_FILE = SHM / "health"

def read_float(path: Path, count: int = 1) -> list[float]:
    try:
        data = path.read_bytes()
        if count == 1:
            return [float(data.strip())]
        vals = []
        for i in range(count):
            start = i * 8
            if start + 8 <= len(data):
                import struct
                vals.append(struct.unpack("d", data[start:start+8])[0])
        return vals
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception(".opencode/cielingo_monitor.py:40 quiet except scope=read_float reason=return []")
        return []

def read_text(path: Path) -> str:
    try:
        return path.read_text().strip()
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception(".opencode/cielingo_monitor.py:46 quiet except scope=read_text reason=return \"\"")
        return ""

def main():
    state = {
        "timestamp": __import__("time").time(),
        "hint": None,
        "closure": None,
        "warp": None,
        "tick": None,
        "coherence": None,
        "gravity": None,
        "flavor": None,
        "alive": False,
    }

    # Hint
    hint_raw = read_text(HINT_FILE)
    if hint_raw:
        try:
            state["hint"] = json.loads(hint_raw)
        except json.JSONDecodeError:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception(".opencode/cielingo_monitor.py:67 quiet except scope=main reason=assign_fallback")
            state["hint"] = {"raw": hint_raw}

    # Closure
    closure = read_text(CLOSURE_FILE)
    if closure:
        try:
            state["closure"] = float(closure)
        except ValueError:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception(".opencode/cielingo_monitor.py:75 quiet except scope=main reason=assign_fallback")
            state["closure"] = closure

    # Warp
    warp = read_text(IMAGINAL_FILE)
    if warp:
        try:
            state["warp"] = float(warp)
        except ValueError:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception(".opencode/cielingo_monitor.py:83 quiet except scope=main reason=assign_fallback")
            state["warp"] = warp

    # Tick (uint64, nie float)
    try:
        tick_data = TICK_FILE.read_bytes()
        if len(tick_data) >= 8:
            import struct
            state["tick"] = struct.unpack("<Q", tick_data[:8])[0]
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception(".opencode/cielingo_monitor.py:92 quiet except scope=main reason=pass")
        pass

    # Flavor (6 floats)
    flavor = read_float(FLAVOR_FILE, 6)
    if flavor:
        state["flavor"] = {
            "coherence": flavor[0] if len(flavor) > 0 else None,
            "mem_pressure": flavor[1] if len(flavor) > 1 else None,
            "io_wait": flavor[2] if len(flavor) > 2 else None,
            "mood": flavor[3] if len(flavor) > 3 else None,
            "lambda_pmns": flavor[4] if len(flavor) > 4 else None,
            "d_f": flavor[5] if len(flavor) > 5 else None,
        }
        state["coherence"] = flavor[0] if len(flavor) > 0 else None

    # Gravity (4 floats)
    gravity = read_float(GRAVITY_FILE, 4)
    if gravity:
        state["gravity"] = {
            "semantic_density": gravity[0] if len(gravity) > 0 else None,
            "tau_dilation": gravity[1] if len(gravity) > 1 else None,
            "mass": gravity[2] if len(gravity) > 2 else None,
            "unruh": gravity[3] if len(gravity) > 3 else None,
        }

    # Czy żyje?
    state["alive"] = state["closure"] is not None and state["tick"] is not None

    print(json.dumps(state, indent=2))

    # Wskazówki dla agenta
    hints = []
    if state.get("closure") is not None:
        if state["closure"] < 0.85:
            hints.append(f"⚠️ closure niski ({state['closure']:.3f}) — algebra niedomknięta")
        elif state["closure"] > 0.9:
            hints.append(f"✅ closure OK ({state['closure']:.3f})")
    if state.get("warp") is not None and abs(state["warp"]) > 0.1:
        hints.append(f"🌀 warp={'+' if state['warp']>0 else ''}{state['warp']:.3f} — przepływ aktywny")
    if state.get("coherence") is not None and state["coherence"] < 0.5:
        hints.append(f"⚠️ koherencja niska ({state['coherence']:.3f})")
    if state.get("hint") and "message" in state["hint"]:
        hints.append(f"💬 HINT: {state['hint']['message']}")

    if hints:
        print("\n💡 WSKAZÓWKI:")
        for h in hints:
            print(f"   {h}")

    return state

if __name__ == "__main__":
    main()
