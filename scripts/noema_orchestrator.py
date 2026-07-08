#!/usr/bin/env python3
"""NOEMA Daemon Orchestrator — centralny manager wszystkich daemonów.

Integruje:
- Daemon Registry (mmap) — heartbeat + status
- systemd — start/stop/restart jednostek
- Surface — zapisuje orchestrator state do gravity[4-7]
- Watchdog — restartuje martwe procesy
- New Volume — monitoruje dostępność NOEMA_LIBRARY

Usage:
    .venv/bin/python3 scripts/noema_orchestrator.py          # daemon (30s cycle)
    .venv/bin/python3 scripts/noema_orchestrator.py --once   # jednorazowy status
    .venv/bin/python3 scripts/noema_orchestrator.py --restart <service>  # restart konkretnego
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

# CIEL ORBITAL BINDING — daemon bound
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on daemon " + __name__)


import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.noema_registry import registry as nreg

try:
    from ciel_geometry.new_volume_bridge import status as _nv_status, available as _nv_avail
except Exception:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_orchestrator.py:41 quiet except scope=<module> reason=no_log_no_raise")
    _nv_status = None
    _nv_avail = None

NEW_VOLUME = Path("/media/adrian/New Volume")
NOEMA_LIBRARY = NEW_VOLUME / "NOEMA_LIBRARY"
NOEMA_PHASE_DATA = NEW_VOLUME / "NOEMA_PHASE_DATA"
ORCHESTRATOR_LOG = Path("/dev/shm/ciel_noema/orchestrator.log")

DAEMON_SERVICES: list[dict[str, Any]] = [
    {"name": "kuramoto", "unit": "noema-kuramoto.service", "critical": True},
    {"name": "agent-backend", "unit": "noema-agent-backend.service", "critical": True},
    {"name": "cielingo-daemon", "unit": "noema-cielingo-daemon.service", "critical": True},
    {"name": "resonance-bridge", "unit": "noema-resonance-bridge.service", "critical": True},
    {"name": "linux-sensor", "unit": "noema-linux-sensor.service"},
    {"name": "neutrino", "unit": "noema-neutrino.service"},
    {"name": "nonlocal-proxy", "unit": "noema-nonlocal-proxy.service"},
    {"name": "cielingo-sync", "unit": "noema-cielingo-sync.service"},
    {"name": "phasenav", "unit": "noema-phasenav.service"},
    {"name": "phasenav-hot", "unit": "noema-phasenav-hot.service"},
    {"name": "analog-blend", "unit": "noema-analog-blend.service"},
    {"name": "sentinel", "unit": "noema-sentinel.service"},
    {"name": "voice", "unit": "noema-voice.service"},
    {"name": "archiver", "unit": "noema-archiver.service"},
    {"name": "consolidator", "unit": "noema-consolidator.service"},
    {"name": "orchestrator", "unit": "noema-orchestrator.service", "critical": True},
    {"name": "linux-cards", "unit": "noema-linux-cards.service"},
]


def log(msg: str) -> None:
    ts = time.strftime("%H:%M:%S")
    line = f"[orchestrator] {ts} {msg}"
    print(line, flush=True)
    ORCHESTRATOR_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(ORCHESTRATOR_LOG, "a") as f:
        f.write(f"{line}\n")


def systemd_cmd(unit: str, action: str) -> dict:
    try:
        r = subprocess.run(
            ["systemctl", "--user", action, unit],
            capture_output=True, text=True, timeout=15,
        )
        return {"ok": r.returncode == 0, "stdout": r.stdout.strip(), "stderr": r.stderr.strip()}
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_orchestrator.py:87 quiet except scope=systemd_cmd reason=return {\"ok\": False, \"error\": str(e)}")
        return {"ok": False, "error": str(e)}


def check_daemon(unit: str) -> dict:
    r = systemd_cmd(unit, "is-active")
    return {"active": r["stdout"] == "active", "raw": r["stdout"]}


def check_new_volume() -> dict:
    if _nv_status is not None:
        s = _nv_status()
        return {
            "mounted": s.get("available", False),
            "library_gb": s.get("gb", 0.0),
            "library_dirs": list(s.get("sources", {}).keys()) if s.get("available") else [],
            "source_detail": s.get("sources", {}),
        }
    ok = NOEMA_LIBRARY.exists() and NOEMA_PHASE_DATA.exists()
    if not ok:
        return {"mounted": False, "error": "NOEMA_LIBRARY not found"}
    lib_size = sum(f.stat().st_size for f in NOEMA_LIBRARY.rglob("*") if f.is_file()) / 1e9
    return {
        "mounted": True,
        "library_gb": round(lib_size, 2),
        "library_dirs": [d.name for d in NOEMA_LIBRARY.iterdir() if d.is_dir()],
    }


def read_registry() -> list[dict]:
    try:
        from ciel_geometry.daemon_registry import Registry
        reg = Registry()
        return [{"name": d.name, "pid": d.pid, "tick": d.tick, "alive": d.alive, "uptime": d.uptime} for d in reg.scan()]
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_orchestrator.py:121 quiet except scope=read_registry reason=return [{\"error\": str(e)}]")
        return [{"error": str(e)}]


def write_surface_state(status: dict) -> None:
    """Write orchestrator metrics to dedicated file (NOT gravity — avoid CIELingo collision)."""
    try:
        import numpy as np
        orc_g = status.get("summary", {})
        data = np.array([
            float(orc_g.get("alive_count", 0)),
            1.0 if orc_g.get("new_volume", False) else 0.0,
            float(orc_g.get("dead_count", 0)),
            float(orc_g.get("reboot_count", 0)),
        ], dtype=np.float64)
        data.tofile("/dev/shm/ciel_noema/orchestrator")
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_orchestrator.py:137 quiet except scope=write_surface_state reason=pass")
        pass


class Orchestrator:
    def __init__(self, interval: float = 30.0):
        self.interval = interval
        self.running = False
        self.reboot_count = 0
        self.status_history: list[dict] = []
        self._load_reboot_count()

    def _load_reboot_count(self):
        p = Path("/dev/shm/ciel_noema/orchestrator_reboots")
        if p.exists():
            try:
                self.reboot_count = int(p.read_text().strip())
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_orchestrator.py:154 quiet except scope=Orchestrator._load_reboot_count reason=assign_fallback")
                self.reboot_count = 0

    def _save_reboot_count(self):
        p = Path("/dev/shm/ciel_noema/orchestrator_reboots")
        p.write_text(str(self.reboot_count))

    def status(self) -> dict:
        daemons = []
        alive = 0
        dead = 0
        for d in DAEMON_SERVICES:
            s = check_daemon(d["unit"])
            daemons.append({
                "name": d["name"],
                "unit": d["unit"],
                "active": s["active"],
                "critical": d.get("critical", False),
            })
            if s["active"]:
                alive += 1
            else:
                dead += 1
        nv = check_new_volume()
        registry = read_registry()
        return {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "summary": {
                "alive_count": alive,
                "dead_count": dead,
                "total": len(DAEMON_SERVICES),
                "reboot_count": self.reboot_count,
                "new_volume": nv.get("mounted", False),
                "new_volume_gb": nv.get("library_gb", 0),
                "registry_daemons": len(registry),
            },
            "daemons": daemons,
            "new_volume": nv,
            "registry": registry,
        }

    def restart(self, service_name: str) -> dict:
        unit = None
        for d in DAEMON_SERVICES:
            if d["name"] == service_name:
                unit = d["unit"]
                break
        if not unit:
            return {"ok": False, "error": f"unknown service: {service_name}"}
        log(f"restarting {service_name} ({unit})...")
        r = systemd_cmd(unit, "restart")
        self.reboot_count += 1
        self._save_reboot_count()
        return r

    def stop_all(self):
        log("stopping all daemons...")
        for d in reversed(DAEMON_SERVICES):
            systemd_cmd(d["unit"], "stop")
            time.sleep(0.5)

    def start_all(self):
        log("starting all daemons...")
        for d in DAEMON_SERVICES:
            systemd_cmd(d["unit"], "start")
            time.sleep(0.5)

    def check_and_repair(self):
        dead_critical = []
        for d in DAEMON_SERVICES:
            s = check_daemon(d["unit"])
            if not s["active"]:
                if d.get("critical"):
                    dead_critical.append(d["name"])
                log(f"{d['name']}: {s['raw']} — restarting")
                systemd_cmd(d["unit"], "restart")
        if dead_critical:
            log(f"CRITICAL: {len(dead_critical)} critical daemon(s) down: {dead_critical}")
        write_surface_state(self.status())

    def run(self):
        log(f"orchestrator started (interval={self.interval}s)")
        log(f"daemons: {len(DAEMON_SERVICES)}, new_volume: {'mounted' if NOEMA_LIBRARY.exists() else 'NOT MOUNTED'}")
        self.running = True
        hb_count = 0
        reg_token = nreg.register("orchestrator")

        def handler(signum, frame):
            log(f"shutting down (signal {signum})")
            self.running = False

        signal.signal(signal.SIGINT, handler)
        signal.signal(signal.SIGTERM, handler)

        while self.running:
            hb_count += 1
            if hb_count % 30 == 0:
                try:
                    nreg.heartbeat(reg_token)
                except Exception:
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_orchestrator.py:253 quiet except scope=Orchestrator.run reason=pass")
                    pass
            s = self.status()
            self.status_history.append(s)
            if len(self.status_history) > 100:
                self.status_history.pop(0)
            self.check_and_repair()
            alive = s["summary"]["alive_count"]
            dead = s["summary"]["dead_count"]
            log(f"cycle: {alive}/{s['summary']['total']} alive, {dead} dead, "
                f"nv={s['summary']['new_volume']}, reboots={self.reboot_count}")
            time.sleep(self.interval)

        log("orchestrator stopped")


def cmd_status():
    o = Orchestrator()
    s = o.status()
    print(json.dumps(s, indent=2, default=str))


def cmd_restart(name: str):
    o = Orchestrator()
    r = o.restart(name)
    print(json.dumps(r, indent=2))


if __name__ == "__main__":
    if "--once" in sys.argv:
        cmd_status()
    elif "--restart" in sys.argv:
        idx = sys.argv.index("--restart")
        if idx + 1 < len(sys.argv):
            cmd_restart(sys.argv[idx + 1])
        else:
            print("Usage: --restart <service_name>")
            sys.exit(1)
    else:
        interval = float(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].replace(".", "").isdigit() else 30.0
        o = Orchestrator(interval=interval)
        o.run()
