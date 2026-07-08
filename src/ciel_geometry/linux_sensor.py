"""NOEMA Linux Sensor — mapuje system operacyjny na powierzchnię 3-6-9.

Sensor NIE zastępuje Kuramoto — zasila powierzchnię REALNYMI danymi
z /proc i /sys, na których Kuramoto wykonuje ewolucję.
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import os
from pathlib import Path
from typing import Any

import numpy as np

from .noema_surface_mmap import (
    N_OSCILLATORS, N_FLAVORS, DEFAULT_SURFACE_ROOT, flush_surface,
)

# ── Oscillator map: system_d → φ index ────────────────────────────────────

SYSTEM_OSC_MAP: dict[str, int] = {
    "cpu_user":      0, "cpu_nice":     1, "cpu_system":    2, "cpu_iowait":   3,
    "cpu_irq":       4, "cpu_softirq":  5, "cpu_steal":     6, "cpu_guest":    7,
    "mem_total":     8, "mem_free":     9, "mem_available":10, "mem_cache":    11,
    "mem_buffers":  12, "swap_total":  13, "swap_free":    14, "swap_cached":  15,
    "load_1":       16, "load_5":      17, "load_15":      18, "procs_run":    19,
    "procs_block":  20, "ctxt_per_sec": 21, "forks_per_sec":22, "entropy":      23,
    # Nowe kanały 24-35 dla 36D
    "io_rchar":     24, "io_wchar":    25, "io_read_bytes":26, "io_write_bytes":27,
    "num_fds":      28, "num_threads": 29, "cpu_temp":     30, "gpu_temp":     31,
    "battery_pct":  32, "wifi_signal": 33, "disk_busy":    34, "net_dropped":  35,
}

_SYSTEM_KEYS = list(SYSTEM_OSC_MAP.keys())
_SYSTEM_IDXS = np.array(list(SYSTEM_OSC_MAP.values()), dtype=np.intp)

# ── Flavor map ─────────────────────────────────────────────────────────────

FLAVOR_MAP: dict[str, int] = {
    "cpu_coherence": 0, "mem_pressure": 1, "io_wait": 2,
    "load_mood":     3, "entropy_open": 4, "sys_mode": 5,
}

# ── proc paths ─────────────────────────────────────────────────────────────

_PROC_STAT = Path("/proc/stat")
_PROC_MEMINFO = Path("/proc/meminfo")
_PROC_LOADAVG = Path("/proc/loadavg")
_PROC_ENTROPY = Path("/proc/sys/kernel/random/entropy_avail")
_PROC_NET = Path("/proc/net/dev")
_OWN_IO = Path("/proc/self/io")
_TWO_PI = 2.0 * np.pi

# ── Precomputed operator matrix (33×36) ────────────────────────────────────
# Built once at import; used by process_phasenav for vectorized matching.

_OP_MATRIX: np.ndarray | None = None
_OP_IDS: list[str] = []


def _ensure_op_matrix() -> tuple[np.ndarray, list[str]]:
    global _OP_MATRIX, _OP_IDS
    if _OP_MATRIX is not None:
        return _OP_MATRIX, _OP_IDS
    from .phasenav.operator_algebra import ALL_OPERATOR_IDS, operator_signature
    _OP_IDS = list(ALL_OPERATOR_IDS)
    rows = []
    for oid in _OP_IDS:
        v = np.asarray(operator_signature(oid), dtype=np.float64)
        rows.append(v)
    _OP_MATRIX = np.array(rows, dtype=np.float64)  # (33, 36)
    return _OP_MATRIX, _OP_IDS


# ── Stat helpers (I/O bound, minimal vectorization possible) ────────────────

def _stat_read(path: Path) -> str:
    try:
        return path.read_text()
    except OSError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_sensor.py:79 quiet except scope=_stat_read reason=return \"\"")
        return ""


def _read_cpu_phi() -> np.ndarray:
    """Read /proc/stat → phi[0:8] (CPU oscillators) as numpy array."""
    phi = np.zeros(8, dtype=np.float64)
    text = _stat_read(_PROC_STAT)
    if not text:
        return phi
    for line in text.splitlines():
        if line.startswith("cpu "):
            parts = line.split()
            idx_map = (1, 2, 3, 5, 6, 7, 8, 9)
            for i, idx in enumerate(idx_map):
                if idx < len(parts):
                    phi[i] = min(float(parts[idx]) / 100.0, 1.0) * _TWO_PI
        elif line.startswith("procs_running "):
            phi[-5] = min(float(line.split()[1]) / 64.0, 1.0) * _TWO_PI
        elif line.startswith("procs_blocked "):
            phi[-4] = min(float(line.split()[1]) / 64.0, 1.0) * _TWO_PI
        elif line.startswith("ctxt "):
            phi[-3] = min(float(line.split()[1]) / 5e6, 1.0) * _TWO_PI
        elif line.startswith("processes "):
            phi[-2] = min(float(line.split()[1]) / 5e4, 1.0) * _TWO_PI
    return phi


def _read_mem_phi() -> np.ndarray:
    """Read /proc/meminfo → phi[8:16] (MEM oscillators)."""
    phi = np.zeros(8, dtype=np.float64)
    text = _stat_read(_PROC_MEMINFO)
    if not text:
        return phi
    vals = {}
    for line in text.splitlines():
        parts = line.split(":")
        if len(parts) != 2:
            continue
        k = parts[0].strip().lower()
        try:
            v = float(parts[1].strip().split()[0]) / 1_000_000  # kB → GB
        except (ValueError, IndexError):
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_sensor.py:121 quiet except scope=_read_mem_phi reason=continue")
            continue
        v = min(v / 16.0, 1.0)
        vals[k] = v
    for i_k, k in enumerate(("memtotal", "memfree", "memavailable", "cached",
                              "buffers", "swaptotal", "swapfree", "swapcached")):
        phi[i_k] = vals.get(k, 0.0) * _TWO_PI
    return phi


def _read_io_phi() -> np.ndarray:
    """Read /proc/self/io → phi[24:28] (IO oscillators)."""
    phi = np.zeros(4, dtype=np.float64)
    text = _stat_read(_OWN_IO)
    if text:
        for line in text.splitlines():
            parts = line.split(":")
            if len(parts) != 2:
                continue
            k = parts[0].strip()
            try:
                v = float(parts[1].strip())
            except (ValueError, IndexError):
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_sensor.py:143 quiet except scope=_read_io_phi reason=continue")
                continue
            if k == "rchar":
                phi[0] = min(v / 1e9, 1.0) * _TWO_PI       # io_rchar
            elif k == "wchar":
                phi[1] = min(v / 1e9, 1.0) * _TWO_PI       # io_wchar
            elif k == "read_bytes":
                phi[2] = min(v / 1e9, 1.0) * _TWO_PI       # io_read_bytes
            elif k == "write_bytes":
                phi[3] = min(v / 1e9, 1.0) * _TWO_PI       # io_write_bytes
    return phi


def _read_load_phi() -> np.ndarray:
    """Read loadavg + entropy + IO → phi[16:28] (LOAD + IO oscillators, 12 elements)."""
    phi = np.zeros(12, dtype=np.float64)
    text = _stat_read(_PROC_LOADAVG)
    if text:
        parts = text.strip().split()
        if len(parts) >= 3:
            phi[0] = min(float(parts[0]) / 8.0, 1.0) * _TWO_PI  # load_1
            phi[1] = min(float(parts[1]) / 8.0, 1.0) * _TWO_PI  # load_5
            phi[2] = min(float(parts[2]) / 8.0, 1.0) * _TWO_PI  # load_15
    try:
        phi[7] = min(_read_float(_PROC_ENTROPY) / 4096.0, 1.0) * _TWO_PI
    except OSError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_sensor.py:168 quiet except scope=_read_load_phi reason=pass")
        pass
    # IO metrics at indices 8-11 (phi[24:28] on the surface)
    io_phi = _read_io_phi()
    phi[8:12] = io_phi
    return phi


def _read_float(path: Path, default: float = 0.0) -> float:
    try:
        return float(path.read_text().strip().split()[0])
    except (OSError, ValueError, IndexError):
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_sensor.py:179 quiet except scope=_read_float reason=return default")
        return default


class LinuxSensorSnapshot:
    def __init__(self) -> None:
        self.raw: dict[str, float] = {}
        self.phi: np.ndarray = np.zeros(N_OSCILLATORS, dtype=np.float64)
        self.omega: np.ndarray = np.full(N_OSCILLATORS, 1.0, dtype=np.float64)
        self.flavor: np.ndarray = np.zeros(N_FLAVORS, dtype=np.float64)
        self.thinking_delta: float = 0.0
        self.tick: int = 0


class LinuxSensor:
    """Czyta /proc i /sys, mapuje na powierzchnię NOEMA."""

    def __init__(self, smoothing: float = 0.3) -> None:
        self.smoothing = smoothing
        self._prev_phi: np.ndarray | None = None
        self._prev_raw_arr: np.ndarray = np.zeros(36, dtype=np.float64)
        self._has_prev = False
        self._prev_tick: int = 0
        self._ema_phi: np.ndarray = np.zeros(N_OSCILLATORS, dtype=np.float64)

    def snapshot(self) -> LinuxSensorSnapshot:
        snap = LinuxSensorSnapshot()

        cpu_phi = _read_cpu_phi()
        mem_phi = _read_mem_phi()
        load_phi = _read_load_phi()

        snap.phi[0:8] = cpu_phi
        snap.phi[8:16] = mem_phi
        snap.phi[16:28] = load_phi

        raw_parts = np.concatenate([
            cpu_phi / _TWO_PI, mem_phi / _TWO_PI, load_phi / _TWO_PI
        ])
        # Pad to 36 (indices 28-35 = extra sensors, zero by default)
        raw_arr = np.zeros(36, dtype=np.float64)
        raw_arr[:len(raw_parts)] = raw_parts
        raw_arr = np.clip(raw_arr, 0.0, 1.0)
        snap.raw = {k: float(raw_arr[i]) for i, k in enumerate(_SYSTEM_KEYS)}

        # ── Flavor (Linux Sensor pisze tylko slot 1 — mem_pressure) ─────
        avail = raw_arr[10] if len(raw_arr) > 10 else 1.0
        total = raw_arr[8] if len(raw_arr) > 8 else 1.0
        snap.flavor[1] = 1.0 - min(avail / max(total, 1e-9), 1.0)

        # ── Omega (first derivative) ───────────────────────────────────
        if self._has_prev:
            dphi = snap.phi - self._prev_phi
            snap.omega = np.clip(np.abs(dphi) * 100.0, 0.1, 100.0)
        else:
            snap.omega[:] = 1.0

        # ── Thinking delta (vectorized) ─────────────────────────────────
        if self._has_prev:
            denom = np.maximum(self._prev_raw_arr, 1e-9)
            deltas = np.abs(raw_arr - self._prev_raw_arr) / denom
            snap.thinking_delta = min(float(np.mean(deltas)), 1.0)

        # ── EMA smoothing ───────────────────────────────────────────────
        if self._has_prev:
            self._ema_phi = self.smoothing * snap.phi + (1.0 - self.smoothing) * self._ema_phi
            snap.phi = self._ema_phi.copy()

        self._prev_phi = snap.phi.copy()
        self._prev_raw_arr = raw_arr.copy()
        self._has_prev = True
        self._prev_tick += 1
        snap.tick = self._prev_tick

        return snap

    def write_surface(self, surface: dict[str, np.memmap], snap: LinuxSensorSnapshot) -> None:
        # Sensor writes RAW data to dedicated mmap — NOT to surface["phi"].
        # Kuramoto daemon blends sensor_raw into phi with AGENT/M2 protection.
        if "sensor_raw" in surface:
            surface["sensor_raw"][...] = snap.phi
        else:
            # Fallback (legacy): if no sensor_raw, write directly for compat
            surface["phi"][...] = snap.phi
        surface["omega"][...] = snap.omega
        surface["flavor"][1] = snap.flavor[1]  # tylko mem_pressure
        surface["tick"][0] = snap.tick
        surface["Z_geom"][...] = np.cos(snap.phi)
        z = np.mean(np.exp(1j * snap.phi))
        surface["R_geom"][0] = float(abs(z))
        surface["psi_geom"][0] = float(np.angle(z))
        flush_surface(surface)

    def process_phasenav(self, snap: LinuxSensorSnapshot) -> dict[str, Any]:
        """Vectorized PhaseNav: one matrix multiply vs ALL 33 operators."""
        op_matrix, op_ids = _ensure_op_matrix()

        # Harmonic imprint
        H = {f"R_{h}": round(float(abs(np.mean(np.exp(1j * h * snap.phi)))), 6)
             for h in (1, 3, 6, 9)}

        # Vectorized cosine similarity: state_vec vs all operators
        # 18 sin + 18 cos = 36 elements (matching 36D operator signatures)
        state_vec = np.concatenate([np.sin(snap.phi[:18]), np.cos(snap.phi[:18])])
        sv_norm = np.linalg.norm(state_vec) + 1e-12
        state_vec_n = state_vec / sv_norm
        op_norms = np.linalg.norm(op_matrix, axis=1) + 1e-12
        cos_sims = (op_matrix @ state_vec_n) / op_norms
        best_idx = int(np.argmax(cos_sims))
        best_op = op_ids[best_idx]

        fp = "".join("H" if H[f"R_{h}"] > 0.5 else "L" for h in (1, 3, 6, 9))

        return {
            "operator": best_op,
            "cos_similarity": round(float(cos_sims[best_idx]), 4),
            "harmonic_fingerprint": fp,
            "R": H,
            "thinking_delta": round(snap.thinking_delta, 6),
            "flavor": [round(float(f), 4) for f in snap.flavor],
            "tick": snap.tick,
        }


def top_processes(n: int = 10) -> list[dict[str, Any]]:
    """Top N procesów według CPU z PhaseNav, batch-mode."""
    from .phasenav.enrichment import phasenav_enrich

    procs: list[dict[str, Any]] = []
    try:
        for entry in os.scandir("/proc"):
            if not entry.name.isdigit():
                continue
            pid = entry.name
            try:
                stat_text = Path(f"/proc/{pid}/stat").read_text()
                comm = stat_text.split("(")[1].split(")")[0] if "(" in stat_text else "?"
                stat_parts = stat_text.split(")")[-1].split()
                state = stat_parts[0] if stat_parts else "?"
                utime = float(stat_parts[11]) if len(stat_parts) > 12 else 0.0
                stime = float(stat_parts[12]) if len(stat_parts) > 13 else 0.0
                rss = _read_rss(pid)
                procs.append({
                    "pid": pid, "comm": comm, "state": state,
                    "cpu_sec": utime + stime, "rss_kb": rss,
                })
            except (OSError, ValueError, IndexError):
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_sensor.py:325 quiet except scope=top_processes reason=continue")
                continue
    except OSError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_sensor.py:327 quiet except scope=top_processes reason=pass")
        pass

    procs.sort(key=lambda p: -p["cpu_sec"])
    top = procs[:n]

    # Batch PhaseNav: all top processes in one go
    for p in top:
        p["phasenav"] = phasenav_enrich(f"pid:{p['pid']}", p["comm"])

    return top


def _read_rss(pid: str) -> float:
    try:
        for line in Path(f"/proc/{pid}/status").read_text().splitlines():
            if line.startswith("VmRSS:"):
                parts = line.split()
                return float(parts[1]) if len(parts) > 1 else 0.0
    except OSError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/linux_sensor.py:346 quiet except scope=_read_rss reason=pass")
        pass
    return 0.0
