"""HTRI GPU driver layer.

Owns runtime selection, backend execution, and EEG-style RT snapshots.
"""
from __future__ import annotations

import importlib.util
import json
import logging
import math
import shutil
import time
from pathlib import Path
from typing import Any, Literal

import numpy as np

from .htri_matrix import DensePhaseNetwork

log = logging.getLogger(__name__)

BackendName = Literal["cupy_dense", "numpy_dense"]
DEFAULT_SAMPLE_POINTS = 36
# Runtime observations are durable host evidence.  The volatile surface is
# intentionally read-only for this producer; root-owned surface subdirectories
# must never turn a real GPU observation into a quiet log-write failure.
RT_DIR = Path("/media/adrian/New Volume/CIEL_memories/logs/htri")
RT_LOG = RT_DIR / "gpu_driver_rt.jsonl"


def _slugify_device_name(name: str) -> str:
    slug = "".join(ch for ch in name if ch.isalnum())
    return slug or "Fallback"


def _sample_wave(values: np.ndarray, sample_points: int = DEFAULT_SAMPLE_POINTS) -> list[float]:
    if values.size == 0:
        return [0.5] * sample_points
    idx = np.linspace(0, values.size - 1, num=sample_points).astype(int)
    out: list[float] = []
    for i in idx:
        phase = float(values[i]) % (2.0 * math.pi)
        out.append(round(phase / (2.0 * math.pi), 6))
    return out


def _append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(payload, ensure_ascii=False) + "\n")
    except Exception:
        log.debug("gpu_driver.py:47 quiet except scope=_append_jsonl reason=rt_log_write_failed path=%s", path)


def _cupy_device_name(cp: Any) -> str:
    try:
        props = cp.cuda.runtime.getDeviceProperties(0)
        raw = props.get("name", "")
        if isinstance(raw, bytes):
            return raw.decode("utf-8", errors="ignore")
        return str(raw)
    except Exception:
        return ""


def probe_htri_gpu_runtime() -> dict[str, Any]:
    """Probe the HTRI GPU runtime without requiring nvcc."""
    nvidia_smi = shutil.which("nvidia-smi")
    cupy_spec = importlib.util.find_spec("cupy")

    reason: list[str] = []
    device_count = 0
    device_name = ""
    runtime_available = False
    backend: BackendName = "numpy_dense"

    if cupy_spec is None:
        reason.append("cupy_missing")
    else:
        try:
            import cupy as cp  # type: ignore

            device_count = int(cp.cuda.runtime.getDeviceCount())
            if device_count > 0:
                runtime_available = True
                backend = "cupy_dense"
                device_name = _cupy_device_name(cp)
            else:
                reason.append("no_cuda_devices")
        except Exception as exc:
            reason.append(f"cupy_runtime_error:{exc.__class__.__name__}")

    if not nvidia_smi:
        reason.append("nvidia_smi_missing")

    return {
        "runtime_available": runtime_available,
        "backend": backend,
        "cupy_available": cupy_spec is not None,
        "nvidia_smi_available": bool(nvidia_smi),
        "nvidia_smi": nvidia_smi,
        "device_count": device_count,
        "device_name": device_name,
        "reason": reason or ["ok"],
    }


class HTRIGPUDriver:
    """Select and run the HTRI GPU backend."""

    def __init__(
        self,
        n: int = 768,
        dt: float = 0.001,
        kappa: float = 0.1,
        topology: str = "all_to_all",
        field_strength: float = 0.0,
        field_phase: np.ndarray | None = None,
        ring_nearest: int = 1,
        ring_decay: float = 1.0,
        grid_shape: tuple[int, int] | None = None,
        prefer: str = "auto",
        rt_log_path: Path | None = None,
        record_rt: bool = True,
    ) -> None:
        self.network = DensePhaseNetwork(
            n=n,
            dt=dt,
            kappa=kappa,
            topology=topology,  # type: ignore[arg-type]
            field_strength=field_strength,
            field_phase=field_phase,
            ring_nearest=ring_nearest,
            ring_decay=ring_decay,
            grid_shape=grid_shape,
        )
        self.bank = self.network
        self.prefer = prefer
        self.record_rt = record_rt
        self.rt_log_path = Path(rt_log_path) if rt_log_path is not None else RT_LOG
        self.step_count = 0

        self.runtime = probe_htri_gpu_runtime()
        self.runtime_available = bool(self.runtime.get("runtime_available", False))
        self.backend_name: BackendName = "numpy_dense"
        self.device_name = str(self.runtime.get("device_name", "") or "cpu")

        self._cp: Any | None = None
        self._phases: Any | None = None
        self._sigma: Any | None = None
        self._omegas: Any | None = None
        self._matrix: Any | None = None
        self._field_phase: Any | None = None

        if self.prefer != "cpu" and self.runtime_available:
            try:
                import cupy as cp  # type: ignore

                self._cp = cp
                self.backend_name = "cupy_dense"
                self.device_name = self.device_name or _cupy_device_name(cp) or "cuda0"
                self._matrix = cp.asarray(self.network.matrix, dtype=cp.float32)
                self._phases = cp.asarray(self.network.phases, dtype=cp.float32)
                self._sigma = cp.asarray(self.network.sigma, dtype=cp.float32)
                self._omegas = cp.asarray(self.network.omegas, dtype=cp.float32)
                self._field_phase = cp.asarray(self.network.field_phase, dtype=cp.float32)
                self.runtime["reason"] = list(self.runtime.get("reason", [])) + ["cupy_backend_selected"]
            except Exception as exc:
                self.runtime["reason"] = list(self.runtime.get("reason", [])) + [
                    f"cupy_backend_error:{exc.__class__.__name__}"
                ]
                self.runtime_available = False
                self.backend_name = "numpy_dense"
                self.device_name = "cpu"
                self._cp = None

        self.runtime["selected_backend"] = self.backend_name
        self.runtime["prefer"] = self.prefer

    def _substrate_label(self) -> str:
        if self.backend_name == "cupy_dense":
            return f"HTRI_{_slugify_device_name(self.device_name)}_cupy_dense"
        if self.prefer == "cpu":
            return "HTRI_cpu_dense"
        return "HTRI_Fallback_numpy_dense"

    def _run_cupy(self, steps: int) -> dict[str, Any]:
        cp = self._cp
        assert cp is not None

        phases = self._phases
        sigma = self._sigma
        omegas = self._omegas
        matrix = self._matrix
        field_phase = self._field_phase
        assert phases is not None and sigma is not None and omegas is not None and matrix is not None and field_phase is not None

        dt = float(self.network.dt)
        n = max(1, self.network.n)

        for _ in range(steps):
            prev = phases.copy()
            diff = phases[:, None] - phases[None, :]
            coupling = cp.sum(matrix * cp.sin(diff), axis=1) / n
            field = self.network.field_strength * cp.sin(field_phase - phases)
            phases = (phases + dt * (omegas + coupling + field)) % (2.0 * math.pi)
            delta = cp.arctan2(cp.sin(phases - prev), cp.cos(phases - prev))
            sigma = sigma + delta / (2.0 * math.pi)

        self._phases = phases
        self._sigma = sigma
        self.network.phases = cp.asnumpy(phases)
        self.network.sigma = cp.asnumpy(sigma)
        self.network.t += steps * dt
        self.network.coherence = float(abs(cp.mean(cp.exp(1j * phases))))
        diff = phases[:, None] - phases[None, :]
        self.network.potential = float(0.5 * cp.sum(matrix * (1.0 - cp.cos(diff))).item() / n)
        return self.network.snapshot()

    def _build_eeg_rt(self, report: dict[str, Any]) -> dict[str, Any]:
        phases = np.asarray(self.network.phases, dtype=np.float64)
        sigma = np.asarray(self.network.sigma, dtype=np.float64)
        return {
            "schema": "HTRI_EEG_RT_V1",
            "ts": time.time(),
            "step_count": self.step_count,
            "backend": self.backend_name,
            "prefer": self.prefer,
            "runtime_available": self.runtime_available,
            "device_name": self.device_name,
            "device_count": int(self.runtime.get("device_count", 0) or 0),
            "coherence": float(report.get("coherence", 0.0) or 0.0),
            "potential": float(report.get("potential", 0.0) or 0.0),
            "spectral_radius": float(report.get("spectral_radius", 0.0) or 0.0),
            "phase_wave_36d": _sample_wave(phases),
            "sigma_wave_36d": _sample_wave(sigma),
            "source": "htri_gpu_driver",
        }

    def run(self, steps: int = 500) -> dict[str, Any]:
        t0 = time.time()
        steps = max(0, int(steps))

        if self.backend_name == "cupy_dense":
            report = self._run_cupy(steps)
        else:
            report = self.network.run(steps)

        self.step_count += steps
        report = dict(report)
        report["backend"] = self.backend_name
        report["driver"] = dict(self.runtime)
        report["runtime_available"] = self.runtime_available
        report["device_name"] = self.device_name
        report["substrate"] = self._substrate_label()
        report["steps"] = steps
        report["rt_elapsed_s"] = round(time.time() - t0, 3)
        report["eeg_rt"] = self._build_eeg_rt(report)

        if self.record_rt:
            _append_jsonl(self.rt_log_path, report["eeg_rt"])

        return report


__all__ = ["HTRIGPUDriver", "probe_htri_gpu_runtime"]
