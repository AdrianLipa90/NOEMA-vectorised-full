#!/usr/bin/env python3
"""Watch the live NOEMA surface and optional phase-memory matches."""

from __future__ import annotations
# CIEL ORBITAL BINDING — daemon bound
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on daemon " + __name__)


import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry import DEFAULT_SURFACE_ROOT, open_surface, query_phase_memory
from ciel_geometry.resonance_bridge import DEFAULT_IMAGINAL_SURFACE_ROOT, resonance_snapshot


def snapshot(surface_root: Path, query: str | None, top_k: int, imaginal_root: Path | None = None) -> dict[str, object]:
    surface = open_surface(surface_root)
    phi = np.asarray(surface["phi"], dtype=np.float64)
    omega = np.asarray(surface["omega"], dtype=np.float64)
    flavor = np.asarray(surface["flavor"], dtype=np.float64)
    payload: dict[str, object] = {
        "tick": int(surface["tick"][0]),
        "phi_mean": float(np.mean(phi)),
        "phi_std": float(np.std(phi)),
        "omega_mean": float(np.mean(omega)),
        "R_global": float(np.mean(np.asarray(surface["R_geom"], dtype=np.float64))),
        "psi_global": float(np.mean(np.asarray(surface["psi_geom"], dtype=np.float64))),
        "flavor": [float(x) for x in flavor.tolist()],
    }
    if query:
        payload["matches"] = [row.__dict__ for row in query_phase_memory(query, top_k=top_k, surface_root=surface_root)]
    if imaginal_root is not None and imaginal_root.exists():
        payload["dual_surface"] = resonance_snapshot(real_root=surface_root, imaginal_root=imaginal_root)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Watch live NOEMA phase surface")
    parser.add_argument("--surface-root", type=Path, default=DEFAULT_SURFACE_ROOT)
    parser.add_argument("--query", type=str, default=None, help="optional phase-memory query")
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--imaginal-root", type=Path, default=DEFAULT_IMAGINAL_SURFACE_ROOT)
    parser.add_argument("--no-imaginal", action="store_true", help="disable dual-surface resonance snapshot")
    parser.add_argument("--watch", action="store_true", help="refresh continuously")
    parser.add_argument("--interval", type=float, default=1.0)
    args = parser.parse_args()

    while True:
        imaginal_root = None if args.no_imaginal else args.imaginal_root
        print(json.dumps(snapshot(args.surface_root, args.query, args.top_k, imaginal_root), ensure_ascii=False, indent=2))
        if not args.watch:
            return 0
        time.sleep(max(args.interval, 0.1))


if __name__ == "__main__":
    raise SystemExit(main())
