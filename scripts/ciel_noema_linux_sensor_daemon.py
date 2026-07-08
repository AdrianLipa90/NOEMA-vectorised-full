#!/usr/bin/env python3
"""NOEMA Linux Sensor Daemon — mapuje system na powierzchnię /dev/shm/ciel_noema.

Usage:
    sudo python scripts/ciel_noema_linux_sensor_daemon.py
    # bez sudo: niektóre /proc odczyty pominięte, ale działa

Zapisuje na powierzchnię:
    phi[0..23]   → wymiary systemowe (CPU, mem, IO, net, procs)
    omega[0..23] → prędkość zmian (1. pochodna)
    flavor[0..5] → zagregowane metryki (cpu_coherence, mem_pressure, io_wait, mood, entropy, mode)
    tick         → licznik snapshotów

Raportuje:
    - fingerprint operacyjny systemu (PhaseNav)
    - top 10 procesów z operator fingerprint
    - thinking trigger δΦ z I/O i load spike
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

# CIEL ORBITAL BINDING — daemon bound
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on daemon " + __name__)


import signal
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.linux_sensor import LinuxSensor, top_processes
from ciel_geometry.noema_registry import registry
from ciel_geometry.noema_surface_mmap import ensure_surface, DEFAULT_SURFACE_ROOT

INTERVAL_S = 1.0  # 1 Hz — zgodne z daemonem Kuramoto

class LinuxSensorDaemon:
    def __init__(self, root: Path = DEFAULT_SURFACE_ROOT) -> None:
        self.root = root
        self.sensor = LinuxSensor()
        self.surface = ensure_surface(root)
        self.running = False
        self._prev_fingerprint: str = ""
        self._reg_token = registry.register("sensor")
        print(f"[LinuxSensor] registered token={self._reg_token[:8]}...")

    def run(self) -> None:
        self.running = True
        print(f"[LinuxSensor] start — {self.root}")
        print(f"[LinuxSensor] interval: {INTERVAL_S}s")

        hb_counter = 0
        while self.running:
            t0 = time.perf_counter_ns()

            try:
                snap = self.sensor.snapshot()
                self.sensor.write_surface(self.surface, snap)
                hb_counter += 1
                if hb_counter % 10 == 0:
                    registry.heartbeat(self._reg_token)

                # PhaseNav fingerprint co 5 cykli
                if snap.tick % 5 == 0:
                    pn = self.sensor.process_phasenav(snap)
                    fp = pn["harmonic_fingerprint"]
                    op = pn["operator"]
                    td = pn["thinking_delta"]
                    fl = pn["flavor"]

                    # Zmiana fingerprintu? Raport
                    if fp != self._prev_fingerprint:
                        print(f"  [{snap.tick}] φ:{fp} ∥ {op} ∥ δΦ:{td:.4f} ∥ F:{fl}")
                        self._prev_fingerprint = fp

                    # Top procesy co 30 cykli
                    if snap.tick % 30 == 0:
                        top = top_processes(5)
                        if top:
                            print(f"  ── top 5 procesów ──")
                            for p in top:
                                pn_pid = p["phasenav"]
                                print(f"    PID {p['pid']:>6} {p['comm'][:24]:<24} "
                                      f"CPU:{p['cpu_sec']:.1f}s "
                                      f"→ {pn_pid['operator_id']} ({pn_pid['harmonic_fingerprint']})")

            except Exception as exc:
                print(f"[LinuxSensor] błąd: {exc}", file=sys.stderr)

            # Interval: 1 Hz (lub catch-up jeśli opóźnienie)
            elapsed = (time.perf_counter_ns() - t0) / 1e9
            remaining = INTERVAL_S - elapsed
            if remaining > 0:
                # Czekaj przerwanie przy SIGINT/SIGTERM
                try:
                    time.sleep(remaining)
                except KeyboardInterrupt:
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_noema_linux_sensor_daemon.py:102 quiet except scope=LinuxSensorDaemon.run reason=break")
                    break

    def stop(self) -> None:
        self.running = False
        registry.unregister(self._reg_token)
        print("[LinuxSensor] unregistered from NOEMA registry")

def main():
    import argparse
    ap = argparse.ArgumentParser(description="NOEMA Linux Sensor Daemon")
    ap.add_argument("--root", type=str, default=str(DEFAULT_SURFACE_ROOT))
    args = ap.parse_args()

    root = Path(args.root)
    if not (root / "phi").exists():
        print(f"[LinuxSensor] powierzchnia nie istnieje: {root}")
        print(f"[LinuxSensor] utwórz przez scripts/ciel_noema_kuramoto_daemon.py")
        sys.exit(1)

    daemon = LinuxSensorDaemon(root)

    def _handler(signum, frame):
        print(f"\n[LinuxSensor] sygnał {signum} — zamykam")
        daemon.stop()

    signal.signal(signal.SIGINT, _handler)
    signal.signal(signal.SIGTERM, _handler)

    try:
        daemon.run()
    except KeyboardInterrupt:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_noema_linux_sensor_daemon.py:133 quiet except scope=main reason=Expr")
        daemon.stop()

    print("[LinuxSensor] koniec")

if __name__ == "__main__":
    main()
