#!/usr/bin/env python3
"""NOEMA Watchdog — trzyma wszystkie daemony przy życiu.

Jeśli któryś padnie, restartuje go. Sprawdza co 30s.
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

# CIEL ORBITAL BINDING — daemon bound
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on daemon " + __name__)


import os
import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

DAEMONS: list[dict] = [
    {
        "name": "kuramoto",
        "cmd": ["python3", "-u", str(ROOT / "scripts/ciel_noema_kuramoto_daemon.py"),
                "--interval", "0.1", "--dt", "0.05"],
        "log": "/dev/shm/ciel_noema/kuramoto_daemon.log",
    },
    {
        "name": "resonance",
        "cmd": ["python3", "-u", str(ROOT / "scripts/ciel_noema_resonance_bridge.py")],
        "log": "/dev/shm/ciel_noema/resonance_bridge.log",
    },
    {
        "name": "neutrino",
        "cmd": ["python3", "-u", str(ROOT / "scripts/ciel_noema_neutrino_daemon.py"),
                "--interval", "1.0"],
        "log": "/dev/shm/ciel_noema/neutrino_daemon.log",
    },
    {
        "name": "sync",
        "cmd": ["python3", "-u", str(ROOT / "scripts/ciel_noema_cielingo_sync.py")],
        "log": "/dev/shm/ciel_noema/cielingo_sync.log",
    },
    {
        "name": "nonlocal",
        "cmd": ["python3", "-u", str(ROOT / "scripts/ciel_noema_nonlocal_proxy.py"),
                "--interval", "1.0"],
        "log": "/dev/shm/ciel_noema/nonlocal_proxy.log",
    },
    {
        "name": "linux_sensor",
        "cmd": ["python3", "-u", str(ROOT / "scripts/ciel_noema_linux_sensor_daemon.py")],
        "log": "/dev/shm/ciel_noema/linux_sensor_daemon.log",
    },
    {
        "name": "phasenav",
        "cmd": ["python3", "-u", str(ROOT / "scripts/ciel_noema_phasenav_daemon.py"),
                "--interval", "5.0"],
        "log": "/dev/shm/ciel_noema/phasenav_daemon.log",
    },
    {
        "name": "ebpf",
        "cmd": ["python3", "-u", str(ROOT / "scripts/ebpf_noema_daemon.py"),
                "--interval", "1.0"],
        "log": "/dev/shm/ciel_noema/ebpf_sensor.log",
        "sudo": True,
    },
]


class Watchdog:
    def __init__(self, check_interval: float = 30.0):
        self.interval = check_interval
        self.processes: dict[str, subprocess.Popen] = {}
        self.running = False

    def _start(self, d: dict) -> subprocess.Popen | None:
        name = d["name"]
        log_path = d["log"]
        cmd = d["cmd"]
        needs_sudo = d.get("sudo", False)

        try:
            with open(log_path, "a") as logf:
                logf.write(f"\n--- watchdog restart at {time.ctime()} ---\n")
                if needs_sudo:
                    sudo_cmd = ["sudo", "-S", "-p", ""] + cmd
                    proc = subprocess.Popen(
                        sudo_cmd,
                        stdin=subprocess.PIPE,
                        stdout=logf,
                        stderr=logf,
                        preexec_fn=os.setpgrp,
                    )
                    proc.stdin.write(b"M4y0n3z11\n")
                    proc.stdin.flush()
                else:
                    proc = subprocess.Popen(
                        cmd,
                        stdout=logf,
                        stderr=logf,
                        preexec_fn=os.setpgrp,
                    )
                self.processes[name] = proc
                print(f"[watchdog] {name} started (PID {proc.pid})", flush=True)
                return proc
        except Exception as e:
            print(f"[watchdog] {name} start failed: {e}", flush=True)
            return None

    def check(self):
        for d in DAEMONS:
            name = d["name"]
            proc = self.processes.get(name)
            if proc is None or proc.poll() is not None:
                if proc is not None:
                    print(f"[watchdog] {name} died (rc={proc.returncode}), restarting...", flush=True)
                del self.processes[name]
                self._start(d)

    def start_all(self):
        print(f"[watchdog] starting all {len(DAEMONS)} daemons...", flush=True)
        for d in DAEMONS:
            self._start(d)
            time.sleep(1.0)  # stagger starts

    def stop_all(self):
        for name, proc in self.processes.items():
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                print(f"[watchdog] {name} stopped", flush=True)
            except (ProcessLookupError, PermissionError):
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_watchdog.py:135 quiet except scope=Watchdog.stop_all reason=pass")
                raise
                pass

    def run(self):
        self.start_all()
        self.running = True
        print(f"[watchdog] running (check every {self.interval}s)", flush=True)

        def _handler(signum, frame):
            print(f"\n[watchdog] shutting down...", flush=True)
            self.running = False

        signal.signal(signal.SIGINT, _handler)
        signal.signal(signal.SIGTERM, _handler)

        while self.running:
            time.sleep(self.interval)
            self.check()

        self.stop_all()
        print("[watchdog] done", flush=True)


if __name__ == "__main__":
    w = Watchdog(check_interval=float(sys.argv[1]) if len(sys.argv) > 1 else 30.0)
    w.run()
