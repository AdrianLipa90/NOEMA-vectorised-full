#!/usr/bin/env python3
"""Probe real host HTRI viability using existing CIEL tools."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
OMEGA = SRC / "CIEL_OMEGA_COMPLETE_SYSTEM"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(OMEGA) not in sys.path:
    sys.path.insert(0, str(OMEGA))

from ciel_sot_agent.htri_resource_gate import htri_profile_summary
from ciel_sot_agent.cuda_probe import probe_cuda
from ciel_omega.htri.gpu_driver import probe_htri_gpu_runtime
from noema_holonomic_doctor.doctor import DoctorConfig, run_doctor_cycle


def main() -> int:
    cuda = probe_cuda()
    gpu_driver = probe_htri_gpu_runtime()
    profile = htri_profile_summary()
    doctor = run_doctor_cycle(ROOT, DoctorConfig(write=False))
    payload = {
        "root": str(ROOT),
        "cuda": cuda,
        "gpu_driver": gpu_driver,
        "htri_profile": profile,
        "doctor": {
            "status": doctor.status,
            "j_doctor": doctor.j_doctor,
            "closure_error": doctor.euler_berry_closure_error,
            "epsilon_neutrino": doctor.epsilon_neutrino,
            "d_lambda": doctor.d_lambda,
            "finding_count": len(doctor.findings),
        },
        "verdict": (
            "gpu_driver_ready"
            if gpu_driver.get("runtime_available")
            else (
                "host_cuda_unavailable_use_cpu_or_imaginal_fallback"
                if not cuda.get("cuda_available")
                else "host_cuda_toolchain_detected"
            )
        ),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
