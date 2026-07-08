"""HTRI Local - dense matrix phase dynamics for local hardware.

This version replaces the scalar Kuramoto step with a fully vectorized dense
phase network: explicit coupling matrix, explicit pairwise potential, and a
winding-number accumulator for the topological memory trace.

The model remains classical. The matrices are phase-space bookkeeping, not
quantum operators.
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import math
import time
from dataclasses import dataclass, field
from typing import Any

import numpy as np

from .gpu_driver import HTRIGPUDriver
from .htri_matrix import DensePhaseNetwork, plo_frequencies

# ── Hardware constants ──────────────────────────────────────────────────────

CPU_THREADS = 12     # i7-8750H logical cores
GPU_CORES = 768      # GTX 1050 Ti CUDA cores
RAM_GB = 7.5
SCHUMANN_HZ = 7.83

# ── Frequency scaling ───────────────────────────────────────────────────────

_H200_BLOCKS = 14080   # reference scale (H200 spec)
_H200_SPREAD = 28.0    # Hz spread for 14080 blocks → 7.83 Hz beat


def plo_frequencies_local(n: int, f_base: float = 1.0,
                          target_beat_hz: float = SCHUMANN_HZ) -> np.ndarray:
    """Backward-compatible alias for the local frequency ladder."""
    _ = target_beat_hz  # diagnostic only
    spread = _H200_SPREAD * (n / _H200_BLOCKS)
    return np.array([f_base + (i / max(n, 1)) * spread for i in range(n)], dtype=np.float64)


def critical_kappa(n: int, margin: float = 1.5) -> float:
    """Kuramoto critical coupling K_c = 2*std(omegas), scaled by safety margin.

    Emergent — derived from the actual frequency distribution, not hardcoded.
    margin=1.5 puts the system solidly above the synchronization threshold.
    """
    omegas = plo_frequencies_local(n)
    return 2.0 * float(np.std(omegas)) * margin


# ── Dense phase network wrapper ─────────────────────────────────────────────

@dataclass
class OscillatorBank:
    n: int
    kappa: float = 0.1
    dt: float = 0.001
    topology: str = "all_to_all"
    field_strength: float = 0.0
    ring_nearest: int = 1
    ring_decay: float = 1.0
    grid_shape: tuple[int, int] | None = None

    phases: np.ndarray = field(init=False)
    omegas: np.ndarray = field(init=False)
    sigma: np.ndarray = field(init=False)
    coherence: float = field(init=False, default=0.0)
    potential: float = field(init=False, default=0.0)
    t: float = field(init=False, default=0.0)

    def __post_init__(self) -> None:
        self._network = DensePhaseNetwork(
            n=self.n,
            dt=self.dt,
            kappa=self.kappa,
            topology=self.topology,  # type: ignore[arg-type]
            field_strength=self.field_strength,
            ring_nearest=self.ring_nearest,
            ring_decay=self.ring_decay,
            grid_shape=self.grid_shape,
        )
        # Keep a stable, explicit state mirror for downstream callers.
        self.phases = self._network.phases
        self.omegas = self._network.omegas
        self.sigma = self._network.sigma

    def step(self) -> None:
        self._network.step()
        self._sync(self._network.snapshot())

    def run(self, steps: int) -> dict[str, Any]:
        snapshot = self._network.run(int(steps))
        self._sync(snapshot)
        return {
            "n_oscillators": self.n,
            "coherence": round(self.coherence, 6),
            "potential": round(self.potential, 6),
            "soul_invariant": round(float(np.mean(self.sigma)), 6),
            "sigma_max": round(float(np.max(np.abs(self.sigma))), 6),
            "beat_freq_est_hz": round(float(np.std(self.omegas) * self.n / 2), 4),
            "spectral_radius": round(float(snapshot["spectral_radius"]), 6),
            "field_norm": round(float(snapshot["field_norm"]), 6),
            "t": round(self.t, 4),
        }

    def _sync(self, snapshot: dict[str, Any]) -> None:
        self.phases = self._network.phases
        self.omegas = self._network.omegas
        self.sigma = self._network.sigma
        self.coherence = float(snapshot.get("coherence", self.coherence))
        self.potential = float(snapshot.get("potential", self.potential))
        self.t = float(snapshot.get("t", self.t))


# ── CPU HTRI (12 threads) ───────────────────────────────────────────────────

class CPUHtri:
    """12 PLO - one per logical thread of the i7-8750H."""

    def __init__(self):
        self.bank = OscillatorBank(n=CPU_THREADS, kappa=critical_kappa(CPU_THREADS), dt=0.001)

    def run(self, steps: int = 500) -> dict[str, Any]:
        m = self.bank.run(steps)
        m["substrate"] = "CPU_i7-8750H"
        return m


# ── GPU HTRI (768 cores) ────────────────────────────────────────────────────

class GPUHtri:
    """768 PLO mapped to the HTRI GPU driver layer."""

    def __init__(self):
        self.driver = HTRIGPUDriver(
            n=GPU_CORES,
            kappa=critical_kappa(GPU_CORES),
            dt=0.001,
            topology="all_to_all",
        )
        self.bank = self.driver.bank
        self._cuda = self.driver.runtime_available
        self.backend = self.driver.backend_name
        self.device_name = self.driver.device_name
        self.runtime = self.driver.runtime

    def run(self, steps: int = 500) -> dict[str, Any]:
        report = self.driver.run(steps)
        self._cuda = self.driver.runtime_available
        self.backend = self.driver.backend_name
        self.device_name = self.driver.device_name
        self.runtime = self.driver.runtime
        return report


# ── Unified Local HTRI ──────────────────────────────────────────────────────

class LocalHTRI:
    """Unified HTRI for the local system.

    CPU (12) + GPU (768) = 780 total oscillators.
    The combined result exposes coherence, potential, spectral radius, and the
    topological winding-number trace.
    """

    def __init__(self):
        self.cpu = CPUHtri()
        self.gpu = GPUHtri()

    def run(self, cpu_steps: int = 300, gpu_steps: int = 300) -> dict[str, Any]:
        t0 = time.time()

        cpu_m = self.cpu.run(cpu_steps)
        gpu_m = self.gpu.run(gpu_steps)

        ram_avail = _read_ram_available_gb()
        ram_phase = 2 * math.pi * (ram_avail / RAM_GB)

        # Disk I/O as M2/M3 phase channels
        disk_r, disk_w = _read_disk_throughput_mb()

        total_osc = CPU_THREADS + GPU_CORES
        w_cpu = CPU_THREADS / total_osc
        w_gpu = GPU_CORES / total_osc

        sigma_comb = w_cpu * cpu_m["soul_invariant"] + w_gpu * gpu_m["soul_invariant"]
        coh_comb = w_cpu * cpu_m["coherence"] + w_gpu * gpu_m["coherence"]
        pot_comb = w_cpu * cpu_m["potential"] + w_gpu * gpu_m["potential"]
        spec_comb = w_cpu * cpu_m["spectral_radius"] + w_gpu * gpu_m["spectral_radius"]

        return {
            "schema": "ciel/htri-local/v2.0-dense",
            "hardware": {
                "cpu": "Intel i7-8750H (12 threads)",
                "gpu": "GTX 1050 Ti (768 CUDA cores)",
                "ram_total_gb": RAM_GB,
                "ram_avail_gb": round(ram_avail, 2),
                "cuda_active": self.gpu._cuda,
                "gpu_backend": getattr(self.gpu, "backend", "unknown"),
                "gpu_device_name": getattr(self.gpu, "device_name", ""),
                "gpu_driver": getattr(self.gpu, "runtime", {}),
            },
            "cpu": cpu_m,
            "gpu": gpu_m,
            "ram_phase_rad": round(ram_phase, 4),
            "disk_read_mb_s": round(disk_r, 3),
            "disk_write_mb_s": round(disk_w, 3),
            "combined": {
                "soul_invariant": round(sigma_comb, 6),
                "coherence": round(coh_comb, 4),
                "potential": round(pot_comb, 6),
                "spectral_radius": round(spec_comb, 6),
                "beat_freq_target_hz": SCHUMANN_HZ,
                "total_oscillators": total_osc,
            },
            "elapsed_s": round(time.time() - t0, 3),
        }


def _read_ram_available_gb() -> float:
    try:
        with open("/proc/meminfo", encoding="utf-8") as fh:
            for line in fh:
                if line.startswith("MemAvailable"):
                    return int(line.split()[1]) / (1024 ** 2)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/htri/htri_local.py:260 quiet except scope=_read_ram_available_gb reason=pass")
        pass
    return 3.0


def _read_disk_throughput_mb(window: float = 0.1) -> tuple[float, float]:
    """Disk read/write throughput in MB/s over a short window."""

    def _sample() -> tuple[float, float]:
        r = w = 0.0
        try:
            with open("/proc/diskstats", encoding="utf-8") as fh:
                for line in fh:
                    parts = line.split()
                    if len(parts) >= 10:
                        dev = parts[2]
                        if dev.startswith(("sd", "nvme", "vd")) and not dev[-1].isdigit():
                            r += float(parts[5]) * 512
                            w += float(parts[9]) * 512
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/htri/htri_local.py:279 quiet except scope=_read_disk_throughput_mb._sample reason=pass")
            pass
        return r, w

    r0, w0 = _sample()
    time.sleep(window)
    r1, w1 = _sample()
    mb = 1024 * 1024
    return (r1 - r0) / window / mb, (w1 - w0) / window / mb


if __name__ == "__main__":
    import json

    print("Uruchamiam HTRI Local na i7-8750H + GTX 1050 Ti...")
    htri = LocalHTRI()
    result = htri.run(cpu_steps=200, gpu_steps=200)
    print(json.dumps(result, indent=2))
