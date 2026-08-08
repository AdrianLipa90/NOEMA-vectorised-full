#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import struct
import sys
import time

import numpy as np

N = 36
BYTES = N * 8


def atomic_write(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    with tmp.open("wb") as fh:
        fh.write(raw)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


def save_npy(path: Path, value: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    with tmp.open("wb") as fh:
        np.save(fh, np.asarray(value, dtype=np.float64))
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


def valid_state(value: np.ndarray) -> bool:
    return value.shape == (N,) and bool(np.all(np.isfinite(value)))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--surface-root", default="/dev/shm/ciel_noema")
    ap.add_argument("--persistent-file", required=True)
    ap.add_argument("--geometry-root")
    ap.add_argument("--interval", type=float, default=0.2)
    args = ap.parse_args()

    if args.geometry_root:
        sys.path.insert(0, args.geometry_root)

    persistent = Path(args.persistent_file)
    root = Path(args.surface_root)
    root.mkdir(parents=True, exist_ok=True)
    source = "PERSISTENT_AUX_SELF"

    if not persistent.is_file():
        from ciel_geometry import aux_self

        state = np.asarray(aux_self.ensure_aux(), dtype=np.float64).reshape(-1)
        if not valid_state(state):
            raise RuntimeError("native aux_self returned invalid state")
        save_npy(persistent, state)
        source = "NATIVE_AUX_SELF_INITIALIZED"

    seq = 0
    while True:
        try:
            state = np.asarray(np.load(persistent, allow_pickle=False), dtype=np.float64).reshape(-1)
            if not valid_state(state):
                raise RuntimeError("persistent AUX state invalid")
            raw = struct.pack("<36d", *map(float, state))
            atomic_write(root / "aux_phi", raw)
            status = {
                "schema": "noema.aux-stream-status/v2",
                "status": "ACTIVE",
                "pid": os.getpid(),
                "heartbeat_ns": time.time_ns(),
                "seq": seq,
                "dim": N,
                "bytes": BYTES,
                "persistent_file": str(persistent),
                "surface_file": str(root / "aux_phi"),
                "state_sha256": hashlib.sha256(raw).hexdigest(),
                "source": source,
                "interval_s": args.interval,
            }
            atomic_write(
                root / "aux_stream_status.json",
                (json.dumps(status, indent=2, sort_keys=True) + "\n").encode(),
            )
            seq += 1
        except Exception as exc:
            status = {
                "schema": "noema.aux-stream-status/v2",
                "status": "BLOCKED",
                "pid": os.getpid(),
                "heartbeat_ns": time.time_ns(),
                "seq": seq,
                "error": f"{type(exc).__name__}:{exc}",
            }
            atomic_write(
                root / "aux_stream_status.json",
                (json.dumps(status, indent=2, sort_keys=True) + "\n").encode(),
            )
        time.sleep(args.interval)


if __name__ == "__main__":
    raise SystemExit(main())
