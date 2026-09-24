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
        """Write only the bridge-owned vector to an initialized surface.

        The bridge runs as root for eBPF access but must not create NOEMA's
        control-plane files.  In particular, ``tick`` is a uint64 mmap field
        owned by the user-level Kuramoto runtime, never a textual bootstrap
        sentinel.
        """
        buf = bytearray(288)
        for i, val in enumerate(vec_36d[:36]):
            struct.pack_into("d", buf, i * 8, val)
        p = NOEMA_SURFACE / "sensor_raw"
        if not NOEMA_SURFACE.is_dir():
            raise RuntimeError(f"NOEMA surface is unavailable: {NOEMA_SURFACE}")
        if not p.is_file():
            raise RuntimeError(f"sensor_raw is not initialized by the surface owner: {p}")
        if p.stat().st_size != len(buf):
            raise RuntimeError(
                f"sensor_raw has {p.stat().st_size} bytes; expected {len(buf)}"
            )
        with p.open("r+b") as handle:
            handle.write(buf)
            handle.flush()
            os.fsync(handle.fileno())

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
                # One BPF map read per cycle, reused for both calls —
                # was 3 full map iterations/cycle (op + to_36d's internal
                # op + to_36d's own read_pid_phases), measured live as a
                # sustained ~26% CPU floor for a nominally 1Hz sensor.
                pids = sched.read_pid_phases()
                op = sched.compute_order_parameters(pids)
                vec = sched.to_36d(pids)
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
