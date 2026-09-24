"""NOEMA analog bus — pseudo-analog shared memory for dual-node PhaseNav.

Architecture:
  Two PhaseNav nodes (hot/cold) write independent phi vectors to mmap.
  A blender reads both, weights by temperature, and injects into surface.

Files under /dev/shm/ciel_noema/analog/:
  phi_hot     float64[36]  — hot node phase (fast, wide exploration)
  phi_cold    float64[36]  — cold node phase (slow, focused)
  temp        float64[1]   — blend temperature (1.0=hot dominant, 0.0=cold)
  coupling    float64[1296] — 36x36 influence cold→hot (for future use)
  resonance   float64[1]   — coherence fed back to hot node
  tick        uint64[1]    — bus tick (written by blender)

Usage:
    from ciel_geometry.analog_bus import ensure_bus, open_bus, blend_phi
    bus = ensure_bus()  # creates mmaps, returns dict of np.ndarray
    bus["phi_hot"][:] = new_phi  # hot node writes
    blended = blend_phi(bus, temp=0.7)
"""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np

ANALOG_ROOT = Path("/dev/shm/ciel_noema/analog")
N_OSCILLATORS = 36

FIELDS: dict[str, tuple[tuple[int, ...], type]] = {
    "phi_hot": ((N_OSCILLATORS,), np.float64),
    "phi_cold": ((N_OSCILLATORS,), np.float64),
    "temp": ((1,), np.float64),
    "coupling": ((N_OSCILLATORS, N_OSCILLATORS), np.float64),
    "resonance": ((1,), np.float64),
    "tick": ((1,), np.uint64),
}


def _ensure_dir() -> None:
    ANALOG_ROOT.mkdir(parents=True, exist_ok=True)


def _create_mmap(path: Path, shape: tuple[int, ...], dtype: type) -> np.ndarray:
    arr = np.memmap(path, dtype=dtype, mode="w+", shape=shape)
    arr.fill(0.0)
    return arr


def _open_mmap(path: Path, shape: tuple[int, ...], dtype: type) -> np.ndarray:
    return np.memmap(path, dtype=dtype, mode="r+", shape=shape)


def ensure_bus() -> dict[str, np.ndarray]:
    _ensure_dir()
    bus = {}
    for name, (shape, dtype) in FIELDS.items():
        path = ANALOG_ROOT / name
        if not path.exists():
            bus[name] = _create_mmap(path, shape, dtype)
        else:
            bus[name] = _open_mmap(path, shape, dtype)
    return bus


def open_bus() -> dict[str, np.ndarray]:
    bus = {}
    for name, (shape, dtype) in FIELDS.items():
        path = ANALOG_ROOT / name
        bus[name] = _open_mmap(path, shape, dtype)
    return bus


def blend_phi(
    bus: dict[str, np.ndarray],
    temp: float | None = None,
) -> np.ndarray:
    phi_hot = np.asarray(bus["phi_hot"], dtype=np.float64)
    phi_cold = np.asarray(bus["phi_cold"], dtype=np.float64)
    if temp is None:
        temp = float(bus["temp"][0])
    temp_clamped = max(0.0, min(1.0, temp))
    if temp_clamped < 1e-9:
        return phi_cold.copy()
    if 1.0 - temp_clamped < 1e-9:
        return phi_hot.copy()
    blended = temp_clamped * phi_hot + (1.0 - temp_clamped) * phi_cold
    return blended % (2 * np.pi)
