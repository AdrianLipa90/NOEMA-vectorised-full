from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OMEGA = ROOT / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM"
LOCAL_PACKAGES = ROOT / ".python_packages"
if str(OMEGA) not in sys.path:
    sys.path.insert(0, str(OMEGA))
if LOCAL_PACKAGES.is_dir() and str(LOCAL_PACKAGES) not in sys.path:
    sys.path.insert(0, str(LOCAL_PACKAGES))

from ciel_omega.htri.gpu_driver import HTRIGPUDriver, probe_htri_gpu_runtime


def test_gpu_driver_probe_exposes_runtime_keys() -> None:
    payload = probe_htri_gpu_runtime()
    for key in (
        "runtime_available",
        "backend",
        "cupy_available",
        "nvidia_smi_available",
        "device_count",
        "device_name",
        "reason",
    ):
        assert key in payload
    assert isinstance(payload["reason"], list)


def test_gpu_driver_runs_and_emits_eeg_rt() -> None:
    driver = HTRIGPUDriver(n=32, dt=0.01, kappa=0.2, prefer="auto", record_rt=False)
    report = driver.run(steps=2)

    assert report["backend"] in {"cupy_dense", "numpy_dense"}
    assert report["substrate"]
    assert "driver" in report
    assert "eeg_rt" in report
    assert report["eeg_rt"]["backend"] == report["backend"]
    assert len(report["eeg_rt"]["phase_wave_36d"]) == 36
