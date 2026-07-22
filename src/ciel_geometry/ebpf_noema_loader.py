"""eBPF → NOEMA bridge: ładuje eBPF program, mapuje perf counters na 36φ.

Usage:
    sudo python3 -c "
    from ciel_geometry.ebpf_noema_loader import EBPFSensor
    sensor = EBPFSensor()
    sensor.start()
    while True:
        snap = sensor.read()
        print(snap)
        time.sleep(1)
    "
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import math
import time
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent
EBPF_C_SRC = ROOT / "src" / "ciel_geometry" / "ebpf_noema_sensor.c"

from .noema_surface_mmap import (
    N_OSCILLATORS, N_FLAVORS, DEFAULT_SURFACE_ROOT, flush_surface,
    FLAVOR_IO_PRESSURE, FLAVOR_MEM_PRESSURE, FLAVOR_ENTROPY, FLAVOR_COHERENCE, FLAVOR_MOOD,
)

_TWO_PI = 2.0 * math.pi

# Precomputed /proc/meminfo keys for MEM oscillators 8-15
_MEM_KEYS = ["MemTotal", "MemFree", "MemAvailable", "Cached",
             "Buffers", "SwapTotal", "SwapFree", "SwapCached"]


class EBPFSensor:
    """eBPF-based system sensor → 36 oscillator phases + 6 flavors."""

    def __init__(self) -> None:
        self._bpf = None
        self._running = False
        self._prev_counters: dict[str, float] = {}
        self._prev_rates: dict[str, float] = {}
        self._prev_phi: np.ndarray | None = None
        self._ema_phi: np.ndarray = np.zeros(N_OSCILLATORS, dtype=np.float64)
        self._tick = 0
        self._last_ts: float = 0.0

    def start(self, **bpf_kwargs: Any) -> None:
        from bcc import BPF
        if not EBPF_C_SRC.exists():
            raise FileNotFoundError(f"eBPF C source not found: {EBPF_C_SRC}")
        with open(EBPF_C_SRC) as f:
            bpf_text = f.read()
        self._bpf = BPF(text=bpf_text, **bpf_kwargs)
        self._bpf.attach_tracepoint(tp="sched:sched_switch",
                                     fn_name="trace_sched_switch")
        self._bpf.attach_tracepoint(tp="syscalls:sys_enter_openat",
                                     fn_name="trace_sys_enter_openat")
        self._bpf.attach_tracepoint(tp="irq:irq_handler_entry",
                                     fn_name="trace_irq_handler_entry")
        try:
            self._bpf.attach_tracepoint(tp="exceptions:page_fault_user",
                                         fn_name="trace_page_fault_user")
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/ebpf_noema_loader.py:67 quiet except scope=EBPFSensor.start reason=pass")
            pass  # may not exist on all kernels
        try:
            self._bpf.attach_tracepoint(tp="block:block_rq_complete",
                                         fn_name="trace_block_rq_complete")
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/ebpf_noema_loader.py:72 quiet except scope=EBPFSensor.start reason=pass")
            pass  # may not exist in containers
        # Warm up: read to get num_cpus
        items = list(self._bpf["cpu_util"].items())
        if items:
            self._num_cpus = len(items[0][1]) if hasattr(items[0][1], '__len__') else 1
        else:
            self._num_cpus = 8
        self._running = True

    def stop(self) -> None:
        if self._bpf:
            try:
                self._bpf.detach_tracepoint("sched:sched_switch")
                self._bpf.detach_tracepoint("syscalls:sys_enter_openat")
                self._bpf.detach_tracepoint("irq:irq_handler_entry")
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/ebpf_noema_loader.py:88 quiet except scope=EBPFSensor.stop reason=pass")
                pass
            self._bpf = None
        self._running = False

    def read_counters(self) -> dict[str, float]:
        c: dict[str, float] = {}
        if not self._bpf:
            return c

        # CPU util (PerCpuArray: key=core_idx, value=array[num_cpus])
        try:
            cpu_items = list(self._bpf["cpu_util"].items())
            c["cpu_total"] = 0.0
            for key, val_arr in cpu_items:
                core = key.value if hasattr(key, 'value') else int(key)
                total = sum(int(val_arr[i]) for i in range(self._num_cpus))
                c[f"cpu_core_{core}"] = float(total)
                c["cpu_total"] += float(total)
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/ebpf_noema_loader.py:107 quiet except scope=EBPFSensor.read_counters reason=pass")
            pass

        # Context switches (BPF_ARRAY)
        try:
            cs_val = self._bpf["ctx_switches"][0]
            c["ctx_switches"] = float(cs_val.value if hasattr(cs_val, 'value') else int(cs_val))
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/ebpf_noema_loader.py:114 quiet except scope=EBPFSensor.read_counters reason=assign_fallback")
            c["ctx_switches"] = 0.0

        # Syscall count
        try:
            sc_val = self._bpf["syscall_count"][0]
            c["syscall_openat"] = float(sc_val.value if hasattr(sc_val, 'value') else int(sc_val))
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/ebpf_noema_loader.py:121 quiet except scope=EBPFSensor.read_counters reason=assign_fallback")
            c["syscall_openat"] = 0.0

        # IRQ count
        try:
            irq_val = self._bpf["irq_count"][0]
            c["irq_total"] = float(irq_val.value if hasattr(irq_val, 'value') else int(irq_val))
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/ebpf_noema_loader.py:128 quiet except scope=EBPFSensor.read_counters reason=assign_fallback")
            c["irq_total"] = 0.0

        # Page faults (per-CPU sum)
        pf_total = 0.0
        try:
            pf_items = list(self._bpf["page_faults"].items())
            for key, val_arr in pf_items:
                total = sum(int(val_arr[i]) for i in range(self._num_cpus))
                pf_total += float(total)
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/ebpf_noema_loader.py:138 quiet except scope=EBPFSensor.read_counters reason=pass")
            pass
        c["page_faults"] = pf_total

        # Block I/O completions
        try:
            bio_val = self._bpf["block_io_count"][0]
            c["block_io"] = float(bio_val.value if hasattr(bio_val, 'value') else int(bio_val))
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/ebpf_noema_loader.py:146 quiet except scope=EBPFSensor.read_counters reason=assign_fallback")
            c["block_io"] = 0.0

        return c

    def _rates(self, raw: dict[str, float]) -> dict[str, float]:
        """Compute per-second rates from absolute counters using real elapsed time."""
        now = time.time()
        dt = now - self._last_ts if self._last_ts > 0 else 1.0
        self._last_ts = now
        rates: dict[str, float] = {}
        for k in ("ctx_switches", "syscall_openat", "irq_total",
                  "page_faults", "block_io", "cpu_total"):
            cur = raw.get(k, 0.0)
            prev = self._prev_counters.get(k, 0.0)
            rates[k] = max(0.0, cur - prev) / max(dt, 0.01)
        for core in range(8):
            cur = raw.get(f"cpu_core_{core}", 0.0)
            prev = self._prev_counters.get(f"cpu_core_{core}", 0.0)
            rates[f"cpu_core_{core}"] = max(0.0, cur - prev) / max(dt, 0.01)
        return rates

    def snapshot(self) -> dict[str, Any]:
        raw = self.read_counters()
        rates = self._rates(raw)
        phi = np.zeros(N_OSCILLATORS, dtype=np.float64)

        # CPU 0-7: per-core rate
        cpu_total_rate = rates.get("cpu_total", 1.0)
        for core in range(8):
            core_rate = rates.get(f"cpu_core_{core}", 0.0)
            frac = core_rate / max(cpu_total_rate / 8, 1.0)
            phi[core] = min(frac * 0.5, 1.0) * _TWO_PI

        # MEM 8-15: /proc/meminfo + page fault rate blend
        mem_phi = self._read_mem_fallback()
        pf_rate = rates.get("page_faults", 0.0)
        pf_frac = min(pf_rate / 5000.0, 1.0)
        mem_phi[0] = (mem_phi[0] + pf_frac * _TWO_PI) * 0.5
        mem_phi[1] = pf_frac * _TWO_PI
        phi[8:16] = mem_phi

        # LOAD 16-23: counter rates
        cs_rate = rates.get("ctx_switches", 0.0)
        sc_rate = rates.get("syscall_openat", 0.0)
        irq_rate = rates.get("irq_total", 0.0)
        pf_rate2 = rates.get("page_faults", 0.0)
        bio_rate = rates.get("block_io", 0.0)
        cpu_rate = rates.get("cpu_total", 0.0)

        phi[16] = min(cs_rate / 5000.0, 1.0) * _TWO_PI
        phi[17] = min(sc_rate / 2000.0, 1.0) * _TWO_PI
        phi[18] = min(irq_rate / 500.0, 1.0) * _TWO_PI
        phi[19] = min(pf_rate2 / 5000.0, 1.0) * _TWO_PI
        phi[20] = min(bio_rate / 1000.0, 1.0) * _TWO_PI
        phi[21] = min(cpu_rate / 5000.0, 1.0) * _TWO_PI

        # ── Flavor: rates-based, non-saturating ─────────────────────
        flavor = np.zeros(N_FLAVORS, dtype=np.float64)
        flavor[FLAVOR_MEM_PRESSURE] = min(pf_rate2 / 5000.0, 1.0)
        flavor[FLAVOR_IO_PRESSURE] = min(bio_rate / 1000.0, 1.0)
        flavor[FLAVOR_ENTROPY] = min(irq_rate / 500.0, 1.0)

        # ── Omega ────────────────────────────────────────────────────
        if self._prev_phi is not None:
            dphi = phi - self._prev_phi
            omega = np.clip(np.abs(dphi) * 100.0, 0.1, 100.0)
        else:
            omega = np.full(N_OSCILLATORS, 1.0, dtype=np.float64)

        # ── Thinking delta ───────────────────────────────────────────
        if self._prev_counters and self._prev_rates:
            deltas = []
            for k in ("ctx_switches", "syscall_openat", "irq_total", "page_faults", "block_io"):
                prev = self._prev_rates.get(k, 0.0)
                cur = rates.get(k, 0.0)
                denom = max(abs(cur), abs(prev), 1e-9)
                if denom > 1e-9:
                    deltas.append(abs(cur - prev) / denom)
            thinking_delta = min(float(np.mean(deltas)) if deltas else 0.0, 1.0)
        else:
            thinking_delta = 0.0

        # ── EMA smooth ───────────────────────────────────────────────
        if self._prev_phi is not None:
            self._ema_phi = 0.3 * phi + 0.7 * self._ema_phi
            phi = self._ema_phi.copy()

        self._prev_phi = phi.copy()
        self._prev_counters = raw
        self._prev_rates = rates
        self._tick += 1

        return {
            "phi": phi, "omega": omega, "flavor": flavor,
            "thinking_delta": thinking_delta, "tick": self._tick, "raw": raw,
        }

    def write_surface(self, surface: dict[str, np.memmap], snap: dict[str, Any]) -> None:
        surface["phi"][...] = snap["phi"]
        surface["omega"][...] = snap["omega"]
        # Only write flavor slots assigned to eBPF (1=mem, 2=io, 4=entropy)
        surface["flavor"][FLAVOR_MEM_PRESSURE] = snap["flavor"][FLAVOR_MEM_PRESSURE]
        surface["flavor"][FLAVOR_IO_PRESSURE] = snap["flavor"][FLAVOR_IO_PRESSURE]
        surface["flavor"][FLAVOR_ENTROPY] = snap["flavor"][FLAVOR_ENTROPY]
        surface["tick"][0] = snap["tick"]
        surface["Z_geom"][...] = np.cos(snap["phi"])
        z = np.mean(np.exp(1j * snap["phi"]))
        surface["R_geom"][0] = float(abs(z))
        surface["psi_geom"][0] = float(np.angle(z))
        flush_surface(surface)

    @staticmethod
    def _read_mem_fallback() -> np.ndarray:
        mem = np.zeros(8, dtype=np.float64)
        try:
            text = Path("/proc/meminfo").read_text()
            for i, k in enumerate(_MEM_KEYS):
                for line in text.splitlines():
                    if line.startswith(k):
                        v = float(line.split()[1]) / 1_000_000 / 16.0
                        mem[i] = min(v, 1.0) * _TWO_PI
                        break
        except OSError:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/ebpf_noema_loader.py:269 quiet except scope=EBPFSensor._read_mem_fallback reason=pass")
            pass
        return mem

    @staticmethod
    def _mem_pressure() -> float:
        try:
            text = Path("/proc/meminfo").read_text()
            avail, total = 1.0, 1.0
            for line in text.splitlines():
                if line.startswith("MemAvailable:"):
                    avail = float(line.split()[1]) / 1_000_000 / 16.0
                elif line.startswith("MemTotal:"):
                    total = float(line.split()[1]) / 1_000_000 / 16.0
            return 1.0 - min(avail / max(total, 1e-9), 1.0)
        except OSError:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/ebpf_noema_loader.py:284 quiet except scope=EBPFSensor._mem_pressure reason=return 0.5")
            return 0.5


def main_loop(interval: float = 1.0):
    import signal
    from .noema_surface_mmap import open_surface, DEFAULT_SURFACE_ROOT

    surface = open_surface(DEFAULT_SURFACE_ROOT)
    sensor = EBPFSensor()
    print(f"[eBPF] loading from {EBPF_C_SRC}")

    try:
        sensor.start()
    except Exception as e:
        print(f"[eBPF] failed: {e}")
        print("[eBPF] needs sudo: echo 'password' | sudo -S python3 ...")
        return

    print(f"[eBPF] running at {interval}s interval")
    running = True
    def _handler(signum, frame):
        nonlocal running; running = False
    signal.signal(signal.SIGINT, _handler)
    signal.signal(signal.SIGTERM, _handler)

    while running:
        t0 = time.perf_counter_ns()
        try:
            snap = sensor.snapshot()
            sensor.write_surface(surface, snap)
            if snap["tick"] % 5 == 0:
                R = float(np.abs(np.mean(np.exp(1j * snap["phi"]))))
                print(f"  [{snap['tick']}] φ_mean={float(np.mean(snap['phi'])):.3f} "
                      f"R={R:.4f} δΦ={snap['thinking_delta']:.4f} "
                      f"CS={snap['raw'].get('ctx_switches',0):.0f} "
                      f"F={[round(float(f),2) for f in snap['flavor']]}")
        except Exception as e:
            print(f"[eBPF] error: {e}", file=__import__('sys').stderr)
        elapsed = (time.perf_counter_ns() - t0) / 1e9
        remaining = interval - elapsed
        if remaining > 0:
            time.sleep(remaining)

    sensor.stop()
    print("[eBPF] stopped")


if __name__ == "__main__":
    import sys
    main_loop(interval=float(sys.argv[1]) if len(sys.argv) > 1 else 1.0)
