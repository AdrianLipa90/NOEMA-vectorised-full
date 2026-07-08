#!/usr/bin/env python3
"""Linux Cards Daemon — mapuje cały system Linux na karty NOEMA.

Co robi:
1. Skanuje /proc (przez psutil) + /sys dla:
   - PROC: wszystkie procesy (200)
   - CPU: każdy rdzeń CPU (z /proc/stat)
   - DISK: urządzenia blokowe (z /proc/diskstats)
   - NET_IF: interfejsy sieciowe (z /proc/net/dev)
    - NET_CONN: aktywne połączenia (z /proc/net/tcp)
    - NET_FLOW: procesy z aktywnością sieciową (nethogs-like, przez /proc/[pid]/fd → socket)
    - MODULE: moduły jądra (z /proc/modules)
    - MOUNT: punkty montowania (z /proc/mounts + statvfs)
    - PCI_DEV: urządzenia PCI (z /sys/bus/pci/devices)
    - SENSOR: sensory sprzętowe (z /sys/class/hwmon)
    - SERVICE: usługi systemd (przez systemctl list-units)
2. Zapisuje dane na NOEMA surface: gravity[7], mean_phi, top_cpu, hardware summary
3. Integruje z PhaseNav hot: najbliższa karta → analog bus
4. Zapisuje karty do /dev/shm/ciel_noema/linux_cards/

Użycie:
    .venv/bin/python3 scripts/noema_linux_cards_daemon.py
    .venv/bin/python3 scripts/noema_linux_cards_daemon.py --once
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
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.linux_cards import LinuxCardIndex, CARDS_DIR
from ciel_geometry.noema_registry import registry
from ciel_geometry.noema_surface_mmap import N_OSCILLATORS

SURFACE = Path("/dev/shm/ciel_noema")
GRAVITY_FILE = SURFACE / "gravity"
PHI_FILE = SURFACE / "phi"

_INDEX: LinuxCardIndex | None = None
_running = True

def log(msg: str) -> None:
    ts = time.strftime("%H:%M:%S")
    print(f"[linux-cards] {ts} {msg}", flush=True)

def read_surface_phi() -> np.ndarray:
    try:
        raw = PHI_FILE.read_bytes()
        need = N_OSCILLATORS * 8
        if len(raw) >= need:
            return np.frombuffer(raw[:need], dtype=np.float64).copy()
    except (FileNotFoundError, OSError):
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_linux_cards_daemon.py:67 quiet except scope=read_surface_phi reason=pass")
        pass
    return np.zeros(N_OSCILLATORS, dtype=np.float64)

def write_gravity(val: float) -> None:
    """Zapisz linux_load do osobnego pliku (NOT gravity — avoid CIELingo collision)."""
    try:
        load_path = SURFACE / "linux_load"
        np.array([val], dtype=np.float64).tofile(load_path)
    except (FileNotFoundError, OSError):
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_linux_cards_daemon.py:76 quiet except scope=write_gravity reason=pass")
        pass

def write_cards_dir(idx: LinuxCardIndex) -> None:
    """Zapisz karty na surface i dodatkowe pliki."""
    idx.save_surface()

    # Najbliższe procesy do bieżącej fazy surface (PhaseNav bridge)
    phi_surface = read_surface_phi()
    nearby = idx.nearby(phi_surface, k=10)
    with open(CARDS_DIR / "nearby_surface.json", "w") as f:
        json.dump([{
            "pid": n.get("pid"), "name": n.get("name"),
            "type": n.get("type"), "cpu": n.get("cpu_percent"),
            "sim": round(n.get("sim", 0), 4),
        } for n in nearby], f, indent=2)

def _bridge_to_phasenav() -> None:
    """Wstrzyknij najbliższą kartę do analog bus (PhaseNav hot)."""
    if _INDEX is None:
        return
    phi_surface = read_surface_phi()
    nearby = _INDEX.nearby(phi_surface, k=5)
    if nearby:
        best = nearby[0]
        try:
            analog_dir = SURFACE / "analog"
            if analog_dir.exists():
                best_phi = np.asarray(best.get("phi", np.zeros(N_OSCILLATORS)), dtype=np.float64)
                best_phi.tofile(analog_dir / "phi_hot")
                with open(analog_dir / "hot_label", "w") as f:
                    label = f"{best.get('type','?')}:{best.get('name','?')}"
                    pid = best.get("pid")
                    if pid:
                        label += f" PID:{pid}"
                    f.write(label)
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_linux_cards_daemon.py:112 quiet except scope=_bridge_to_phasenav reason=pass")
            pass

def cycle() -> None:
    global _INDEX
    if _INDEX is None:
        _INDEX = LinuxCardIndex(max_procs=200, max_conns=50)

    n = _INDEX.update()
    stats = _INDEX.summary_stats()

    # Zapisz na surface
    by_type = stats.get("by_type", {})
    total_cpu = by_type.get("PROC", 0)
    write_gravity(min(stats.get("total_cpu", 0) / 50, 10.0))
    write_cards_dir(_INDEX)

    # Log podsumowania
    hw = {k: by_type.get(k, 0) for k in
          ("PROC", "CPU", "DISK", "NET_IF", "NET_CONN", "MODULE", "MOUNT", "PCI_DEV", "SENSOR")}
    log(f"{n} cards | "
        f"CPU cores:{hw.get('CPU',0)} "
        f"DISK:{hw.get('DISK',0)} "
        f"NET:{hw.get('NET_IF',0)} "
        f"conns:{hw.get('NET_CONN',0)} "
        f"mods:{hw.get('MODULE',0)} "
        f"mounts:{hw.get('MOUNT',0)} "
        f"PCI:{hw.get('PCI_DEV',0)} "
        f"sns:{hw.get('SENSOR',0)} "
        f"procs:{hw.get('PROC',0)} "
        f"top:{stats.get('max_cpu_name','?')}")

    _bridge_to_phasenav()

def signal_handler(sig, frame) -> None:
    global _running
    log(f"signal {sig}, exiting")
    _running = False

def main() -> None:
    global _INDEX

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    parser.add_argument("--interval", type=float, default=15.0, help="Seconds between cycles")
    args, _ = parser.parse_known_args()

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    _INDEX = LinuxCardIndex(max_procs=200, max_conns=50)
    n = _INDEX.update()
    log(f"start — {n} Linux cards [{', '.join(f'{t}={c}' for t, c in _INDEX.summary_stats().get('by_type',{}).items())}]")
    write_cards_dir(_INDEX)

    if args.once:
        stats = _INDEX.summary_stats()
        print(json.dumps(stats, indent=2))
        print("\n--- Top CPU ---")
        for t in _INDEX.top_cpu(10):
            print(f"  {t.get('pid',0):>7d}  {t.get('name','?'):<24s}  "
                  f"CPU:{t.get('cpu_percent',0):5.1f}%  "
                  f"MEM:{t.get('memory_percent',0):5.1f}%")
        print(f"\n--- Hardware ---")
        hw = {k: len(_INDEX.by_type(k)) for k in
              ("CPU", "DISK", "NET_IF", "NET_CONN", "MODULE", "MOUNT", "PCI_DEV", "SENSOR")}
        for k, v in hw.items():
            print(f"  {k}: {v}")
        return

    hb_count = 0
    reg_token = registry.register("linux-cards")

    while _running:
        hb_count += 1
        if hb_count % 30 == 0:
            try:
                registry.heartbeat(reg_token)
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_linux_cards_daemon.py:191 quiet except scope=main reason=pass")
                pass

        try:
            cycle()
        except Exception as e:
            log(f"error: {e}")
            import traceback
            traceback.print_exc()

        # Single long sleep zamiast 20×0.25s — redukuje wakeupy z 80 do 1 na cykl
        if _running:
            time.sleep(args.interval)

    log("stopped")

if __name__ == "__main__":
    main()
