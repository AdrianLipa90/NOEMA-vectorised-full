#!/usr/bin/env python3
"""NOEMA Phase Archiver — capture surface state snapshots to persistent storage.

Reads the live NOEMA surface from /dev/shm/ciel_noema every N ticks and
archives to HDF5 on the phase data drive.

Usage:
    .venv/bin/python3 scripts/noema_phase_archiver.py          # daemon mode
    .venv/bin/python3 scripts/noema_phase_archiver.py --once   # single snapshot
    .venv/bin/python3 scripts/noema_phase_archiver.py --probe  # archive stats
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import logging
import os
import signal
import sys
import time
from pathlib import Path

import numpy as np

log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.noema_registry import registry
from ciel_geometry.noema_surface_mmap import ensure_surface, N_OSCILLATORS, N_GRAVITY, N_FLAVORS

PHASE_DATA = Path(os.environ.get(
    "NOEMA_PHASE_DATA",
    "/media/adrian/New Volume1/NOEMA_PHASE_DATA",
))

# ── Archive files ───────────────────────────────────────────────────

SURFACE_ARCHIVE = PHASE_DATA / "SURFACE_HISTORY" / "surface_archive.h5"
WAVE_ARCHIVE = PHASE_DATA / "WAVE_ARCHIVE" / "wave_snapshots.h5"
META_ARCHIVE = PHASE_DATA / "SURFACE_HISTORY" / "archive_meta.json"


def _ensure_h5():
    """Ensure HDF5 file exists with correct dataset schema."""
    try:
        import h5py
    except ImportError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_phase_archiver.py:48 quiet except scope=_ensure_h5 reason=return None")
        return None  # h5py not available — use NPZ fallback

    SURFACE_ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    if SURFACE_ARCHIVE.exists():
        f = h5py.File(str(SURFACE_ARCHIVE), "r+")
        # Check if datasets match current N_OSCILLATORS (24D→36D migration)
        if "phi" in f and f["phi"].shape[-1] != N_OSCILLATORS:
            log.warning("HDF5 shape mismatch: phi=%s != N=%d — recreating archive",
                        f["phi"].shape, N_OSCILLATORS)
            f.close()
            SURFACE_ARCHIVE.unlink()
            f = h5py.File(str(SURFACE_ARCHIVE), "w")
            _create_datasets(f)
        return f

    f = h5py.File(str(SURFACE_ARCHIVE), "w")
    _create_datasets(f)
    return f


def _create_datasets(f: "h5py.File") -> None:
    """Create HDF5 datasets with current N_OSCILLATORS / N_FLAVORS / N_GRAVITY."""
    import h5py
    dt = np.dtype(np.float64)
    f.create_dataset("phi", shape=(0, N_OSCILLATORS), maxshape=(None, N_OSCILLATORS), dtype=dt,
                     compression="gzip", compression_opts=4)
    f.create_dataset("omega", shape=(0, N_OSCILLATORS), maxshape=(None, N_OSCILLATORS), dtype=dt,
                     compression="gzip", compression_opts=4)
    f.create_dataset("gravity", shape=(0, N_GRAVITY), maxshape=(None, N_GRAVITY), dtype=dt,
                     compression="gzip", compression_opts=4)
    f.create_dataset("flavor", shape=(0, N_FLAVORS), maxshape=(None, N_FLAVORS), dtype=dt,
                     compression="gzip", compression_opts=4)
    f.create_dataset("R", shape=(0,), maxshape=(None,), dtype=dt)
    f.create_dataset("tick", shape=(0,), maxshape=(None,), dtype=np.uint64)
    f.create_dataset("timestamp", shape=(0,), maxshape=(None,), dtype=dt)
    f.create_dataset("mean_coupling", shape=(0,), maxshape=(None,), dtype=dt)
    f.create_dataset("euler_residual", shape=(0,), maxshape=(None,), dtype=dt)
    f.attrs["n_oscillators"] = N_OSCILLATORS
    f.attrs["created"] = time.time()
    f.attrs["description"] = "NOEMA surface state archive"


def _ensure_npz() -> dict:
    """NPZ fallback when h5py not available."""
    SURFACE_ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    npz_path = SURFACE_ARCHIVE.with_suffix(".npz")
    if npz_path.exists():
        data = dict(np.load(str(npz_path)))
    else:
        data = {
            "phi": np.zeros((0, N_OSCILLATORS)),
            "omega": np.zeros((0, N_OSCILLATORS)),
            "gravity": np.zeros((0, N_GRAVITY)),
            "flavor": np.zeros((0, N_FLAVORS)),
            "R": np.zeros(0),
            "tick": np.zeros(0, dtype=np.uint64),
            "timestamp": np.zeros(0),
        }
    return data, npz_path


def write_snapshot(surface, archive_h5=None, npz_data=None, npz_path=None) -> int:
    """Write one surface snapshot to archive. Returns total entries."""
    phi = np.asarray(surface["phi"], dtype=np.float64)
    omega = np.asarray(surface["omega"], dtype=np.float64)
    gravity = np.asarray(surface["gravity"], dtype=np.float64)
    flavor = np.asarray(surface["flavor"], dtype=np.float64)
    tick = int(np.asarray(surface["tick"], dtype=np.uint64)[0])
    g = np.asarray(surface["g"], dtype=np.float64)
    z = np.exp(1j * phi)
    R = float(np.abs(z.mean()))
    euler = float(np.abs(z.sum()))
    mean_coupling = float(np.mean(np.abs(g)))
    now = time.time()

    if archive_h5 is not None:
        for key, arr in [
            ("phi", phi[None]), ("omega", omega[None]), ("gravity", gravity[None]),
            ("flavor", flavor[None]), ("R", np.array([R])), ("tick", np.array([tick], dtype=np.uint64)),
            ("timestamp", np.array([now])), ("mean_coupling", np.array([mean_coupling])),
            ("euler_residual", np.array([euler])),
        ]:
            ds = archive_h5[key]
            ds.resize(ds.shape[0] + 1, axis=0)
            ds[-1:] = arr
        archive_h5.flush()
        return archive_h5["phi"].shape[0]
    else:
        for key, arr in [
            ("phi", phi[None]), ("omega", omega[None]), ("gravity", gravity[None]),
            ("flavor", flavor[None]), ("R", np.array([R])),
            ("tick", np.array([tick], dtype=np.uint64)),
            ("timestamp", np.array([now])),
        ]:
            npz_data[key] = np.concatenate([npz_data[key], arr])
        np.savez_compressed(str(npz_path), **npz_data)
        return npz_data["phi"].shape[0]


def snapshot_once() -> dict:
    """Single snapshot to archive."""
    surface = ensure_surface()
    h5 = _ensure_h5()
    if h5 is not None:
        total = write_snapshot(surface, archive_h5=h5)
        h5.close()
    else:
        data, path = _ensure_npz()
        total = write_snapshot(surface, npz_data=data, npz_path=path)
    return {"status": "ok", "entries": total, "format": "hdf5" if h5 else "npz"}


def run_daemon(interval_ticks: int = 50) -> None:
    """Archive surface state every N ticks."""
    h5 = _ensure_h5()
    npz_data = npz_path = None
    if h5 is None:
        npz_data, npz_path = _ensure_npz()

    surface = ensure_surface()
    last_tick = 0
    running = True

    def _stop(signum, frame):
        nonlocal running
        running = False

    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)

    print(f"[archiver] surface archive daemon — interval={interval_ticks} ticks", file=sys.stderr)

    total = 0
    hb_count = 0
    reg_token = registry.register("archiver")
    try:
        while running:
            hb_count += 1
            if hb_count % 30 == 0:
                try:
                    registry.heartbeat(reg_token)
                except Exception:
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_phase_archiver.py:190 quiet except scope=run_daemon reason=pass")
                    pass
            tick = int(np.asarray(surface["tick"], dtype=np.uint64)[0])
            if tick < last_tick:  # tick reset after kuramoto crash
                last_tick = 0
            if tick - last_tick >= interval_ticks:
                total = write_snapshot(surface, archive_h5=h5 if h5 else None,
                                       npz_data=npz_data, npz_path=npz_path)
                last_tick = tick
                print(f"[archiver] tick={tick} total={total}", file=sys.stderr)
                time.sleep(1)
            else:
                time.sleep(0.5)
    except KeyboardInterrupt:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_phase_archiver.py:203 quiet except scope=run_daemon reason=pass")
        pass
    finally:
        if h5:
            # Write metadata
            META_ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
            meta = {
                "n_entries": h5["phi"].shape[0],
                "n_oscillators": N_OSCILLATORS,
                "last_tick": last_tick,
                "formats": list(h5.keys()),
                "file_size": os.path.getsize(str(SURFACE_ARCHIVE)),
            }
            META_ARCHIVE.write_text(json.dumps(meta, indent=2))
            h5.close()
        print(f"[archiver] stopped — {total} snapshots archived", file=sys.stderr)


# ── CLI ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if "--once" in sys.argv:
        result = snapshot_once()
        print(json.dumps(result, indent=2))
    elif "--probe" in sys.argv:
        meta_path = META_ARCHIVE
        if meta_path.exists():
            print(meta_path.read_text())
        else:
            print('{"status": "no archive"}')
    else:
        run_daemon()
