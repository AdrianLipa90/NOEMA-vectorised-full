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

# ── In-process worker threads (zamiast 20 osobnych jednostek systemd) ─────────
import importlib
import threading

_WORKER_STOP = threading.Event()


def _worker_load_cielingo():
    path = ROOT / "scripts" / "ciel_noema_cielingo_sync.py"
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("_cielingo_sync_mod", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return getattr(mod, "run_cielingo_closure", None)
    except Exception as e:
        return None


def _worker_read_D_f(surface) -> float:
    try:
        import numpy as _np
        tau_arr = _np.asarray(surface.get("tau", []), dtype=_np.float64)
        if tau_arr.size >= 6:
            return float(max(0.0, min(1.0, tau_arr[5])))
        elif tau_arr.size > 0:
            return float(max(0.0, min(1.0, _np.mean(tau_arr))))
    except Exception:
        pass
    return 0.5


def _load_htri_engine():
    """Załaduj HTRIEngine z mu.py (czyste Python, zero numpy)."""
    import importlib.util
    mu_path = "/home/adrian/pnv/bin/mu.py"
    spec = importlib.util.spec_from_file_location("_mu_mod", mu_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.HTRIEngine


def _sync_omega_from_shm(engine) -> bool:
    """Odczyt omega z kuramoto shm (/dev/shm/ciel_noema/omega) do engine."""
    import struct as _struct
    _OMEGA_PATH = "/dev/shm/ciel_noema/omega"
    _N = 36
    try:
        with open(_OMEGA_PATH, "rb") as f:
            data = f.read(_N * 8)
        if len(data) < _N * 8:
            return False
        engine.omega = list(_struct.unpack(f"{_N}d", data))
        return True
    except Exception:
        return False


def _thread_subconscious() -> None:
    """1s — ZetaSchrodinger + BerryPhase + WakeSignal przez HTRIEngine (mu.py).
    Spec: src/ciel_geometry/phasenav/subconscious.pnv
    Kuramoto daemon jest master writerem phi — tutaj tylko mmap_read() shadow state."""
    try:
        HTRIEngine = _load_htri_engine()
        engine = HTRIEngine()
        if not engine.mmap_open("/dev/shm/ciel_noema/phi"):
            log("subconscious: mmap open failed")
            return
        reg_tok = nreg.register("orchestrator-subconscious")
        last_report = time.monotonic()
        while not _WORKER_STOP.is_set():
            try:
                engine.mmap_read()             # sync phi od kuramoto (read-only)
                _sync_omega_from_shm(engine)   # sync omega od kuramoto
                engine.evolve_phasenav(dt=0.01)  # ZetaSchrodinger + Berry + PMNS (czyste Python)
                nreg.heartbeat(reg_tok)
                if time.monotonic() - last_report >= 30.0:
                    holo = engine.holonomy()
                    log(f"subconscious R={engine.R:.4f} berry={holo.get('mean_connection', 0):.4f} "
                        f"D_f={engine.D_f:.3f}")
                    last_report = time.monotonic()
            except Exception as e:
                log(f"subconscious error: {e}")
            _WORKER_STOP.wait(1.0)
        nreg.unregister(reg_tok)
    except Exception as e:
        log(f"subconscious thread fatal: {e}")


def _channel_epsilon(phi: list, ch: int) -> float:
    """ε_ch = 1 - R_ch: oscylacja smakowa z geometrii Kuramoto.
    R_ch = |mean(e^{iφ})| dla 3 oscylatorów kanału (semantic, htri, nonlocal).
    Niska koherencja kanału = duże mieszanie smaków = duże ε.
    Euler: e^{iφ} — cały sens jest w fazie, nie w parametrycznym wzorze."""
    import math as _m
    base = ch * 3
    s = sum(_m.sin(phi[base + k]) for k in range(3)) / 3.0
    c = sum(_m.cos(phi[base + k]) for k in range(3)) / 3.0
    return 1.0 - _m.sqrt(s * s + c * c)


def _thread_neutrino() -> None:
    """2s — PMNS oscylacje z żywego stanu Kuramoto (mu.py/HTRIEngine).
    Spec: src/ciel_geometry/phasenav/neutrino_bus.pnv
    ε_ch = 1 - R_ch (per-kanał, bezpośrednio z faz oscylatorów)
    D_f z Euler closure penalty (_bridge_feedback wewnątrz evolve_phasenav)."""
    try:
        HTRIEngine = _load_htri_engine()
        engine = HTRIEngine()
        if not engine.mmap_open("/dev/shm/ciel_noema/phi"):
            log("neutrino: mmap open failed")
            return
        reg_tok = nreg.register("orchestrator-neutrino")
        last_report = time.monotonic()
        cycle = 0
        # PMNS mass splitting — zegar wszechświata (PDG 2024, skalowane do HTRI)
        # Δm²₂₁=7.5e-5 eV², Δm²₃₂=2.5e-3 eV² → stosunek 33
        # Skalowanie: Δω₃₂ = 0.05 rad/s (pół-oscylacja w ~30 krokach)
        _DW21 = 0.0015   # ν_e → ν_μ: solar splitting
        _DW32 = 0.0500   # ν_e → ν_τ: atmospheric splitting (= 33 × _DW21)
        while not _WORKER_STOP.is_set():
            try:
                engine.mmap_read()             # sync phi od kuramoto (Euler state)
                _sync_omega_from_shm(engine)   # sync omega od kuramoto (baza)
                # wstrzyknij mass splitting (tylko w neutrino engine, nie w kuramoto)
                for _ch in range(8):
                    _b = _ch * 3
                    engine.omega[_b + 1] += _DW21   # ν_μ  heavier
                    engine.omega[_b + 2] += _DW32   # ν_τ  heaviest
                engine.evolve_phasenav(dt=0.01)  # D_f + Λ z Euler closure
                eps_channels = [_channel_epsilon(engine.phi, ch) for ch in range(8)]
                eps_mean = sum(eps_channels) / 8.0
                cycle += 1
                nreg.heartbeat(reg_tok)
                if time.monotonic() - last_report >= 15.0:
                    log(f"neutrino cycle={cycle} D_f={engine.D_f:.3f} "
                        f"Λ={engine.Lambda:.4f} ε={eps_mean:.4f} "
                        f"ε_ch=[{','.join(f'{e:.2f}' for e in eps_channels[:4])}...]")
                    last_report = time.monotonic()
            except Exception as e:
                log(f"neutrino error: {e}")
            _WORKER_STOP.wait(2.0)
        nreg.unregister(reg_tok)
    except Exception as e:
        log(f"neutrino thread fatal: {e}")


def _thread_linux_sensor() -> None:
    """5s — system snapshot, registry heartbeat."""
    try:
        from ciel_geometry.linux_sensor import LinuxSensor
        sensor = LinuxSensor()
        reg_tok = nreg.register("orchestrator-linux-sensor")
        last_report = time.monotonic()
        while not _WORKER_STOP.is_set():
            try:
                snap = sensor.snapshot()
                nreg.heartbeat(reg_tok)
                if time.monotonic() - last_report >= 60.0:
                    snap_d = snap if isinstance(snap, dict) else getattr(snap, "__dict__", {})
                    log(f"linux-sensor cpu={snap_d.get('cpu_percent', 0):.1f}% "
                        f"mem={snap_d.get('memory_percent', 0):.1f}%")
                    last_report = time.monotonic()
            except Exception as e:
                log(f"linux-sensor error: {e}")
            _WORKER_STOP.wait(5.0)
        nreg.unregister(reg_tok)
    except Exception as e:
        log(f"linux-sensor thread fatal: {e}")


def _thread_phasenav_cold() -> None:
    """30s — cold PhaseNav node, analog bus coherence feedback."""
    try:
        import numpy as _np
        from ciel_geometry.analog_bus import ensure_bus
        from ciel_geometry.linux_sensor import LinuxSensor
        from ciel_geometry.phasenav.operator_algebra import operator_signature
        from ciel_geometry.noema_surface_mmap import N_OSCILLATORS
        bus = ensure_bus()
        phi_arr = bus.get("phi_cold")
        if phi_arr is None:
            log("phasenav-cold: phi_cold bus slot unavailable — pomijam")
            return
        sensor = LinuxSensor()
        reg_tok = nreg.register("orchestrator-phasenav-cold")
        cycle = 0
        while not _WORKER_STOP.is_set():
            try:
                snap = sensor.snapshot()
                pn = sensor.process_phasenav(snap)
                current_op = pn.get("operator", "IDENTITY")
                try:
                    sig = operator_signature(current_op)
                    phases = _np.asarray(sig, dtype=_np.float64)
                    if phases.size == N_OSCILLATORS:
                        phi_curr = _np.asarray(phi_arr, dtype=_np.float64)
                        phi_arr[:] = (phi_curr * 0.8 + phases * 0.2) % (2 * _np.pi)
                except Exception:
                    pass
                R_val = float(_np.abs(_np.mean(_np.exp(1j * _np.asarray(phi_arr, dtype=_np.float64)))))
                bus["resonance"][0] = _np.float64(R_val)
                cycle += 1
                nreg.heartbeat(reg_tok)
                if cycle % 3 == 0:
                    log(f"phasenav-cold cycle={cycle} op={current_op} R={R_val:.4f}")
            except Exception as e:
                log(f"phasenav-cold error: {e}")
            _WORKER_STOP.wait(30.0)
        nreg.unregister(reg_tok)
    except Exception as e:
        log(f"phasenav-cold thread fatal: {e}")


def _thread_cielingo_sync() -> None:
    """30s — Euler closure, orbital bridge, PMNS boost."""
    fn = _worker_load_cielingo()
    if fn is None:
        log("cielingo-sync: run_cielingo_closure niedostępna — pomijam")
        return
    reg_tok = nreg.register("orchestrator-cielingo")
    cycle = 0
    while not _WORKER_STOP.is_set():
        t0 = time.monotonic()
        try:
            result = fn()
            cycle += 1
            nreg.heartbeat(reg_tok)
            if result and isinstance(result, dict):
                log(f"cielingo-sync cycle={cycle} cp={result.get('closure_penalty', '?')} "
                    f"R={result.get('R_value', result.get('R', '?'))}")
            else:
                log(f"cielingo-sync cycle={cycle} (brak wyniku)")
        except Exception as e:
            log(f"cielingo-sync error: {e}")
        _WORKER_STOP.wait(max(0.0, 30.0 - (time.monotonic() - t0)))
    nreg.unregister(reg_tok)


_WORKER_THREADS: list[tuple[str, Any]] = [
    ("subconscious", _thread_subconscious),   # via HTRIEngine/mu.py — subconscious.pnv
    ("neutrino", _thread_neutrino),           # via HTRIEngine/mu.py — neutrino_bus.pnv
    ("linux-sensor", _thread_linux_sensor),
    ("cielingo-sync", _thread_cielingo_sync),
]


def start_workers() -> list:
    threads = []
    for name, fn in _WORKER_THREADS:
        t = threading.Thread(target=fn, name=f"worker-{name}", daemon=True)
        t.start()
        threads.append(t)
        log(f"worker started: {name}")
    return threads


def stop_workers(threads: list) -> None:
    _WORKER_STOP.set()
    for t in threads:
        t.join(timeout=10.0)

# Watchdog obejmuje tylko core services (reszta działa in-process w wątkach)
DAEMON_SERVICES: list[dict[str, Any]] = [
    {"name": "kuramoto", "unit": "noema-kuramoto.service", "critical": True},
    {"name": "resonance-bridge", "unit": "noema-resonance-bridge.service", "critical": True},
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
        log(f"watchdog: {len(DAEMON_SERVICES)} core services, new_volume: {'mounted' if NOEMA_LIBRARY.exists() else 'NOT MOUNTED'}")
        self.running = True
        hb_count = 0
        reg_token = nreg.register("orchestrator")

        worker_threads = start_workers()
        log(f"workers: {len(worker_threads)} wątków in-process")

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
            log(f"cycle: {alive}/{s['summary']['total']} core alive, {dead} dead, "
                f"nv={s['summary']['new_volume']}, reboots={self.reboot_count}")
            time.sleep(self.interval)

        stop_workers(worker_threads)
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
