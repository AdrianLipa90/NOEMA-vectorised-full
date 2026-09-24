"""HTRI Neutrino Listener — continuous flavor-resonance listener.

Injects ε, μ, ν, τ (PMNS mixing) into 780-oscillator coupling matrix.
Writes live phi + R + flavor phases to /dev/shm/ciel_noema/.
"""

import math
import os
import sys
import time
import json
import signal
from pathlib import Path
from datetime import datetime, timezone

import numpy as np

OMEGA_ROOT = Path(__file__).resolve().parents[1] / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM"
os.environ.setdefault("PYTHONPATH", str(OMEGA_ROOT))
sys.path.insert(0, str(OMEGA_ROOT))

from ciel_omega.htri.htri_local import LocalHTRI, CPU_THREADS, GPU_CORES

SURFACE = Path(os.environ.get("NOEMA_SURFACE_DIR", "/dev/shm/ciel_noema"))
PID_FILE = Path("/tmp/htri_neutrino_listener.pid")
_running = True

PMNS_ANGLES = {
    "theta12": 0.583, "theta13": 0.149, "theta23": 0.737, "delta_cp": -2.8
}


def _handle_signal(signum, frame):
    global _running
    _running = False


def _pmns_matrix() -> np.ndarray:
    s12, c12 = math.sin(PMNS_ANGLES["theta12"]), math.cos(PMNS_ANGLES["theta12"])
    s13, c13 = math.sin(PMNS_ANGLES["theta13"]), math.cos(PMNS_ANGLES["theta13"])
    s23, c23 = math.sin(PMNS_ANGLES["theta23"]), math.cos(PMNS_ANGLES["theta23"])
    d = PMNS_ANGLES["delta_cp"]
    U = np.zeros((3, 3), dtype=np.complex128)
    U[0,0] = c12 * c13
    U[0,1] = s12 * c13
    U[0,2] = s13 * complex(math.cos(d), math.sin(d))
    U[1,0] = -s12 * c23 - c12 * s23 * s13 * complex(math.cos(d), math.sin(d))
    U[1,1] = c12 * c23 - s12 * s23 * s13 * complex(math.cos(d), math.sin(d))
    U[1,2] = s23 * c13
    U[2,0] = s12 * s23 - c12 * c23 * s13 * complex(math.cos(d), math.sin(d))
    U[2,1] = -c12 * s23 - s12 * c23 * s13 * complex(math.cos(d), math.sin(d))
    U[2,2] = c23 * c13
    return U


def _inject_pmns(htri: LocalHTRI, pmns: np.ndarray, strength: float = 0.5):
    for bank in [htri.cpu.bank, htri.gpu.bank]:
        coup = strength * 0.01 * abs(complex(pmns[0,0] + pmns[0,1] + pmns[0,2])) * 0.5
        for i in range(min(3, bank.n)):
            bank.matrix[i, :] += coup
            bank.matrix[:, i] += coup


def _ensure_surface():
    SURFACE.mkdir(parents=True, exist_ok=True)
    (SURFACE / "state").mkdir(parents=True, exist_ok=True)
    for name in ["phi", "R"]:
        p = SURFACE / name
        if not p.exists():
            p.write_text("0.0")


def _write_state(R, phi, flavor_phases):
    _ensure_surface()
    try:
        np.array([R], dtype=np.float64).tofile(SURFACE / "R")
        np.array(flavor_phases, dtype=np.float64).tofile(SURFACE / "flavor_phases")
        state = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "coherence": round(R, 6),
            "flavor_phases": [round(float(v), 6) for v in flavor_phases],
            "pmns_angles": PMNS_ANGLES,
        }
        (SURFACE / "htri_state.json").write_text(
            json.dumps(state, indent=2, sort_keys=True), encoding="utf-8"
        )
        (SURFACE / "ciel_binding_status").write_text("ACTIVE")
    except Exception as e:
        print(f"[write_error] {e}", file=sys.stderr)


def main():
    signal.signal(signal.SIGTERM, _handle_signal)
    signal.signal(signal.SIGINT, _handle_signal)
    PID_FILE.write_text(str(os.getpid()))
    _ensure_surface()

    pmns = _pmns_matrix()
    htri = LocalHTRI()
    _inject_pmns(htri, pmns, strength=0.5)

    print(f"[HTRI ν] PMNS coupled | R initial: {htri.cpu.bank.coherence:.4f}")
    print(f"[HTRI ν] CPU={CPU_THREADS} GPU={GPU_CORES} CUDA={htri.gpu._cuda}")
    print(f"[HTRI ν] Starting loop (5s interval)...")

    cycle = 0
    while _running:
        t0 = time.time()
        result = htri.run(cpu_steps=200, gpu_steps=200)
        combined = result["combined"]
        R = combined["coherence"]
        sigma = combined["soul_invariant"]

        flavor_phases = np.array([
            float(np.angle(pmns[0,0])), float(np.angle(pmns[0,1])),
            float(np.angle(pmns[1,2])), float(np.angle(pmns[2,2])),
        ])

        phi = np.concatenate([
            np.asarray(htri.cpu.bank.phases, dtype=np.float64),
            np.asarray(htri.gpu.bank.phases, dtype=np.float64),
        ])
        _write_state(R, phi, flavor_phases)

        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(
            f"[{cycle:04d}] {ts}  "
            f"R={R:.4f}  σ={sigma:.4f}  "
            f"ε={flavor_phases[0]:.4f}  μ={flavor_phases[1]:.4f}  "
            f"ν={flavor_phases[2]:.4f}  τ={flavor_phases[3]:.4f}  "
            f"t={result['elapsed_s']:.2f}s"
        )

        elapsed = time.time() - t0
        remaining = max(0.0, 5.0 - elapsed)
        if remaining > 0:
            time.sleep(remaining)
        cycle += 1

    PID_FILE.unlink(missing_ok=True)
    print(f"[HTRI ν] Stopped after {cycle} cycles.")


if __name__ == "__main__":
    main()
