"""PhaseNav scheduler eBPF loader — Kuramoto per-PID phase tracking.

Usage:
    python3 phasenav_sched.py          # load + print stats once
    python3 phasenav_sched.py --loop   # continuous monitoring (sudo)
"""
from __future__ import annotations
import argparse
import math
import platform
import sys
import time
from pathlib import Path

from bcc import BPF

C_FILE = Path(__file__).parent / "phasenav_sched.c"
TWO_PI = 2.0 * math.pi
SCALE = 1_000_000


class PhaseNavSched:
    def __init__(self) -> None:
        with open(C_FILE) as f:
            bpf_text = f.read()
        self.bpf = BPF(text=bpf_text)
        self.bpf.attach_kprobe(
            event="finish_task_switch.isra.0",
            fn_name="trace_finish_task_switch",
        )
        self.pid_phase = self.bpf["pid_phase"]
        self.pid_runtime = self.bpf["pid_runtime"]

    def read_pid_phases(self) -> dict[int, dict]:
        result = {}
        for pid, v in self.pid_phase.items():
            pv = v.value if hasattr(v, "value") else v
            pid_val = pid.value if hasattr(pid, "value") else pid
            result[int(pid_val)] = {
                "phase": (pv % SCALE) / SCALE * TWO_PI,
                "phase_acc": pv,
            }
        for pid, v in self.pid_runtime.items():
            rv = v.value if hasattr(v, "value") else v
            pid_val = pid.value if hasattr(pid, "value") else pid
            if pid_val in result:
                result[pid_val]["runtime"] = int(rv)
        return result

    def compute_order_parameters(self) -> dict:
        pids = self.read_pid_phases()
        N = len(pids)
        if N == 0:
            return {"R": 0.0, "Psi": 0.0, "N": 0}

        re_sum = sum(math.cos(v["phase"]) for v in pids.values())
        im_sum = sum(math.sin(v["phase"]) for v in pids.values())
        re_mean = re_sum / N
        im_mean = im_sum / N
        R_global = math.sqrt(re_mean * re_mean + im_mean * im_mean)
        Psi_global = math.atan2(im_mean, re_mean)
        return {"R": R_global, "Psi": Psi_global, "N": N}

    def to_36d(self) -> list[float]:
        """Return 36D sensor_raw vector: [R_global, Ψ_global, per_id...]."""
        op = self.compute_order_parameters()
        vec = [op["R"], op["Psi"]]
        pids = self.read_pid_phases()
        items = sorted(
            pids.items(), key=lambda x: x[1].get("runtime", 0), reverse=True
        )
        n_entries = min(17, len(items))
        for pid, v in items[:n_entries]:
            vec.append(float(pid))
            vec.append(v["phase"])
        while len(vec) < 36:
            vec.append(0.0)
        return vec[:36]

    def cleanup(self) -> None:
        pass


def main() -> int:
    ap = argparse.ArgumentParser(description="PhaseNav scheduler eBPF loader")
    ap.add_argument("--loop", action="store_true")
    args = ap.parse_args()

    if not C_FILE.exists():
        print(f"eBPF C source not found: {C_FILE}", file=sys.stderr)
        return 1

    if not platform.uname().release.startswith("6."):
        print(f"Warning: kernel {platform.uname().release} may not fully support BPF")

    sched = PhaseNavSched()
    print(f"[phasenav_sched] BPF loaded OK")
    time.sleep(1)

    def print_stats() -> None:
        op = sched.compute_order_parameters()
        vec = sched.to_36d()
        print(f"Kuramoto: R={op['R']:.4f}  Ψ={op['Psi']:.4f}  N={op['N']}")
        print(f"36D[:6]: {vec[:6]}")

    if args.loop:
        try:
            while True:
                print_stats()
                time.sleep(2.0)
        except KeyboardInterrupt:
            print("\n[phasenav_sched] stopped")
    else:
        print_stats()

    sched.cleanup()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
