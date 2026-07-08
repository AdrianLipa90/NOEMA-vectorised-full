"""PhaseNav Linux Bridge — eBPF Kuramoto → NOEMA 36D sensor_raw + cgroup.

Uruchamiany jako daemon (sudo):
    python3 phasenav_linux_bridge.py

Cykl (1 Hz):
    1. Czyta BPF mapy (per-PID phase)
    2. Oblicza global R, Ψ
    3. Zapisuje 36D sensor_raw (float64) na powierzchnię NOEMA
    4. Moduluje cgroup cpu.weight na podstawie R
"""
from __future__ import annotations
import math
import os
import signal
import struct
import sys
import time
from pathlib import Path

NOEMA_SURFACE = Path(os.environ.get("NOEMA_SURFACE", "/dev/shm/ciel_noema"))
NOEMA_SURFACE.mkdir(parents=True, exist_ok=True)

# Inicjalizuj brakujące pliki startowe dla NOEMA surface
_SURFACE_INIT_DIRS = ["registry", "daemon_registry", "analog", "phasenav", "htri", "browser", "linux_cards", "daemon_logs"]
for _d in _SURFACE_INIT_DIRS:
    _dp = NOEMA_SURFACE / _d
    try:
        _dp.mkdir(parents=True, exist_ok=True)
    except OSError:
        pass

_SURFACE_INIT_FILES: dict[str, str] = {
    "ciel_binding_status": "ACTIVE",
    "tick": "0",
    "sandbox_adrian": "1.0",
    "sandbox_cpu": "0.5",
    "sandbox_mem": "0.5",
    "sandbox_mood": "0.8",
    "sandbox_R": "0.9",
    "sandbox_tau": "1.0",
    "closure": "0",
}
for _name, _content in _SURFACE_INIT_FILES.items():
    _p = NOEMA_SURFACE / _name
    if not _p.exists():
        try:
            _p.write_text(_content)
        except OSError:
            pass

CGROUP_ROOT = Path("/sys/fs/cgroup")
CGROUP_UI = CGROUP_ROOT / "ui.slice"
CGROUP_SYSTEM = CGROUP_ROOT / "system.slice"

BASE_WEIGHT = 100
ALPHA = 0.5
BETA = 4.0
HYSTERESIS_S = 2.0


class PhaseNavLinuxBridge:
    def __init__(self) -> None:
        self._last_cgroup_write: float = 0.0
        self._running = False

    def write_sensor_raw(self, vec_36d: list[float]) -> None:
        buf = bytearray(288)
        for i, val in enumerate(vec_36d[:36]):
            struct.pack_into("d", buf, i * 8, val)
        p = NOEMA_SURFACE / "sensor_raw"
        try:
            p.write_bytes(buf)
            p.chmod(0o666)
        except OSError:
            pass

    def modulate_cgroup(self, R: float) -> None:
        now = time.monotonic()
        if now - self._last_cgroup_write < HYSTERESIS_S:
            return
        self._last_cgroup_write = now
        modulation = 1.0 + ALPHA * math.tanh((0.5 - R) * BETA)
        new_weight = max(1, min(10000, int(BASE_WEIGHT * modulation)))
        for cg_path in [CGROUP_SYSTEM, CGROUP_UI]:
            weight_file = cg_path / "cpu.weight"
            if weight_file.exists():
                try:
                    weight_file.write_text(str(new_weight))
                except (OSError, PermissionError):
                    pass

    def run(self) -> None:
        try:
            from apocalypos.ebpf.phasenav_sched import PhaseNavSched
        except ImportError:
            sys.path.insert(0, str(Path(__file__).parent.parent))
            from ebpf.phasenav_sched import PhaseNavSched

        self._running = True
        sched = PhaseNavSched()
        print("[pnv_linux_bridge] BPF loaded, starting 1 Hz cycle",
              file=sys.stderr, flush=True)

        signal.signal(signal.SIGINT, lambda *_: setattr(self, "_running", False))
        signal.signal(signal.SIGTERM, lambda *_: setattr(self, "_running", False))

        while self._running:
            try:
                op = sched.compute_order_parameters()
                vec = sched.to_36d()
                self.write_sensor_raw(vec)
                self.modulate_cgroup(op["R"])
                cls = "SYNC" if op["R"] > 0.7 else "MIXED" if op["R"] > 0.4 else "SCATTERED"
                print(
                    f"[pnv_linux_bridge] R={op['R']:.3f} Ψ={op['Psi']:.3f}"
                    f" N={op['N']} {cls}",
                    file=sys.stderr, flush=True,
                )
            except Exception as e:
                print(f"[pnv_linux_bridge] error: {e}", file=sys.stderr, flush=True)
            time.sleep(1.0)

        sched.cleanup()
        print("[pnv_linux_bridge] stopped", file=sys.stderr, flush=True)


def main() -> int:
    PhaseNavLinuxBridge().run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
