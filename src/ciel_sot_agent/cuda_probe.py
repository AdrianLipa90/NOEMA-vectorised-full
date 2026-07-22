"""Central CUDA/CuPy host probe for NOEMA/CIEL runtime."""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import importlib.util
import shutil
from typing import Any


def probe_cuda() -> dict[str, Any]:
    nvcc = shutil.which("nvcc")
    nvidia_smi = shutil.which("nvidia-smi")
    cupy_spec = importlib.util.find_spec("cupy")

    cuda_runtime_ok = False
    cupy_import_ok = False
    device_count = 0
    reason = []

    if not nvcc:
        reason.append("nvcc_missing")
    if not nvidia_smi:
        reason.append("nvidia_smi_missing")
    if cupy_spec is None:
        reason.append("cupy_missing")

    if cupy_spec is not None:
        try:
            import cupy as cp  # type: ignore

            cupy_import_ok = True
            try:
                device_count = int(cp.cuda.runtime.getDeviceCount())
                cuda_runtime_ok = device_count > 0
                if not cuda_runtime_ok:
                    reason.append("cuda_runtime_no_devices")
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_sot_agent/cuda_probe.py:37 quiet except scope=probe_cuda reason=Expr")
                reason.append("cuda_runtime_unavailable")
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_sot_agent/cuda_probe.py:39 quiet except scope=probe_cuda reason=Expr")
            reason.append("cupy_import_failed")

    cuda_available = bool(nvcc and nvidia_smi and cupy_import_ok and cuda_runtime_ok)
    return {
        "cuda_available": cuda_available,
        "nvcc": nvcc,
        "nvidia_smi": nvidia_smi,
        "cupy_installed": cupy_spec is not None,
        "cupy_import_ok": cupy_import_ok,
        "cuda_runtime_ok": cuda_runtime_ok,
        "device_count": device_count,
        "reason": reason or ["ok"],
    }


__all__ = ["probe_cuda"]
