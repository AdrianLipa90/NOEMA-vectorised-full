#!/usr/bin/env python3
"""NOEMA agent-health bridge — writes gravity[5] (agent_ok) from a live
poll of the agent backend's /health endpoint.

gravity[5] (agent_ok) was permanently stuck at 0.0: its only writer,
noema_cielingo_daemon.py, has never had a systemd unit deployed (found
2026-07-09 while investigating why the memory-pressure gravity vector
looked unhealthy). Rather than deploy that whole undertested script,
this is a small, single-purpose bridge doing exactly the one thing that
was missing: poll http://localhost:18520/health and write the boolean
result into the surface, the same way scar_feedback.py expects to read it.

Usage:
    python3 scripts/noema_agent_health_bridge.py [--interval 5]
"""
from __future__ import annotations

import argparse
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

AGENT_HEALTH_URL = "http://localhost:18520/health"


def _check_health() -> bool:
    try:
        resp = urllib.request.urlopen(AGENT_HEALTH_URL, timeout=3)
        return resp.status == 200
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--interval", type=float, default=5.0)
    args = ap.parse_args()

    import numpy as np
    from ciel_geometry.noema_surface_mmap import ensure_surface, flush_surface
    from ciel_geometry.noema_registry import registry

    surface = ensure_surface()
    reg_token = registry.register("agent-health-bridge")

    print(f"[agent-health-bridge] polling {AGENT_HEALTH_URL} every {args.interval}s")

    cycle = 0
    while True:
        cycle += 1
        if cycle % 10 == 0:
            registry.heartbeat(reg_token)

        ok = _check_health()
        gravity = np.asarray(surface["gravity"], dtype=np.float64)
        gravity[5] = 1.0 if ok else 0.0
        flush_surface(surface)

        if cycle % 20 == 1:
            print(f"[agent-health-bridge] agent_ok={1.0 if ok else 0.0}")

        time.sleep(args.interval)


if __name__ == "__main__":
    main()
