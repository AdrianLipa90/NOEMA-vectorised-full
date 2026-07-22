#!/usr/bin/env python3
"""Per-message CIEL coupling — noema surface read, no blocking."""
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import os
import struct
import sys
import time
from pathlib import Path


def read_noema_surface() -> dict:
    shm = Path("/dev/shm/ciel_noema")
    state = {"tick": 0, "phi": [], "omega": [], "flavor": [], "gravity": []}
    def _unpack_dynamic(path: Path, default: list | None = None) -> list:
        """Unpack doubles from binary file, dynamically sized."""
        try:
            raw = path.read_bytes()
            n = len(raw) // 8
            if n > 0:
                return [round(float(v), 4) for v in struct.unpack(f"{n}d", raw)]
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_per_message.py:22 quiet except scope=read_noema_surface._unpack_dynamic reason=pass")
            raise
            pass
        return default if default is not None else []

    try:
        if (shm / "tick").exists():
            state["tick"] = struct.unpack("Q", (shm / "tick").read_bytes())[0]
        if (shm / "phi").exists():
            state["phi"] = _unpack_dynamic(shm / "phi", [])
        if (shm / "omega").exists():
            state["omega"] = _unpack_dynamic(shm / "omega", [])
        if (shm / "gravity").exists():
            state["gravity"] = _unpack_dynamic(shm / "gravity", [0.0, 0.0, 0.0, 0.0])
        if (shm / "flavor").exists():
            state["flavor"] = _unpack_dynamic(shm / "flavor", [0.0] * 6)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_per_message.py:37 quiet except scope=read_noema_surface reason=pass")
        raise
        pass
    return state


def order_parameter(phi):
    if not phi:
        return 0.0
    n = len(phi)
    r = abs(sum(complex(__import__("math").cos(p), __import__("math").sin(p)) for p in phi)) / n
    return round(r, 4)


def main():
    # Parse args
    args = sys.argv[1:]
    use_stdout = "--stdout" in args or "--verbose" in args
    output_file = None
    for i, a in enumerate(args):
        if a == "--output" and i + 1 < len(args):
            output_file = args[i + 1]
        elif a == "--output-file" and i + 1 < len(args):
            output_file = args[i + 1]

    text = " ".join([a for a in args if not a.startswith("--")]) if args else sys.stdin.read().strip() if not sys.stdin.isatty() else ""
    # Strip flag tokens from text if they leaked in
    text = " ".join(t for t in text.split() if not t.startswith("--"))

    surface = read_noema_surface()
    phi = surface.get("phi", [])
    flavor = surface.get("flavor", [0] * 6)
    gravity = surface.get("gravity", [0] * 4)
    tick = surface.get("tick", 0)
    coh = order_parameter(phi)
    flavor_5 = flavor[5] if len(flavor) > 5 else 0.0
    cp = round((2.57 - flavor_5) * 0.5, 4) if flavor_5 > 0 else 0.37
    if coh < 0.3:
        mode = "exploring"
        mood = "curious"
    elif coh < 0.7:
        mode = "resonating"
        mood = "balanced"
    else:
        mode = "locked"
        mood = "coherent"
    summary = {
        "emotion": mood,
        "ethical_score": round(gravity[2] if len(gravity) > 2 else 0.5, 4),
        "soul_invariant": round(abs(sum(phi)) / max(len(phi), 1), 4) if phi else 0.0,
        "operating_mode": mode,
        "coherence_index": coh,
        "mood": mood,
        "cycle_index": tick,
        "closure_penalty": cp,
        "noema_tick": tick,
        "phi_mean": round(sum(phi) / max(len(phi), 1), 4) if phi else 0.0,
        "flavor_4": flavor[4] if len(flavor) > 4 else 0.0,
        "flavor_5": flavor_5,
        "gravity_0": gravity[0] if len(gravity) > 0 else 0.0,
        "message": text[:80],
    }

    data = json.dumps(summary, separators=(",", ":"), ensure_ascii=False) + "\n"

    if output_file:
        _dir = os.path.dirname(output_file)
        if _dir and not os.path.exists(_dir):
            os.makedirs(_dir, exist_ok=True)
        with open(output_file, "w") as f:
            f.write(data)
    elif use_stdout:
        sys.stdout.write(data)
        sys.stdout.flush()
    else:
        # Default: write to /dev/shm/ciel_noema/per_message.json (no leak to terminal)
        default_path = "/dev/shm/ciel_noema/per_message.json"
        try:
            with open(default_path, "w") as f:
                f.write(data)
        except (IOError, OSError):
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_per_message.py:116 quiet except scope=main reason=With")
            raise
            # Fallback to /tmp
            with open("/tmp/noema_per_message.json", "w") as f:
                f.write(data)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_per_message.py:125 quiet except scope=<module> reason=pass")
        raise
        pass
