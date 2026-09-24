#!/usr/bin/env python3

"""Proc watch daemon — inotify-like /proc change detector.

Monitoruje narodziny i śmierci procesów przez skanowanie /proc/[pid]/stat,
detekcję nowych PIDs, i raportowanie na surface.

Zamiast inotify (wymaga ctypes/bindings), używa szybkiego pollingu
przez os.listdir("/proc") + diff z poprzednim stanem.

Surface output (/dev/shm/ciel_noema/proc_watch/):
  new_pids.jsonl  — ostatnie 64 narodzin (PID, nazwa, CPU, MEM)
  dead_pids.jsonl — ostatnie 64 śmierci (PID, nazwa, age)
  stats.json      — fork/exec rate, total births/deaths
  heartbeat.json  — żywotność daemona

Integracja:
  - fork rate → ω modulation na M4 (Perception → zmiany w systemie)
  - nowy PID → alert o birth z priorytetem (ważne procesy)
  - birth rate spike → gravity boost na unruh_power

Użycie:
  .venv/bin/python3 scripts/noema_proc_watch_daemon.py
  systemctl --user start noema-proc-watch.service
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
from collections import deque
from pathlib import Path

from ciel_geometry.noema_registry import registry

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

SURFACE = Path("/dev/shm/ciel_noema")
PROC_WATCH_DIR = SURFACE / "proc_watch"

# Ważne procesy (UID 0 lub well-known)
IMPORTANT_COMMS = {
    "systemd", "sshd", "NetworkManager", "Xorg", "firefox",
    "chrome", "python3", "opencode", "docker", "containerd",
}

# Parametry
SCAN_INTERVAL = 1.0  # sekund między skanami
NEW_RING_SIZE = 64
DEAD_RING_SIZE = 64

# Stan
_prev_pids: set[int] = set()
_prev_stats: dict[int, tuple[float, str]] = {}  # pid → (start_time, comm)
_new_ring: deque[dict] = deque(maxlen=NEW_RING_SIZE)
_dead_ring: deque[dict] = deque(maxlen=DEAD_RING_SIZE)
_fork_rate: deque[float] = deque(maxlen=30)  # timestampy fork events
_exec_rate: deque[float] = deque(maxlen=30)  # timestampy exec events (new PIDs)
_total_births = 0
_total_deaths = 0
_running = True

def log(msg: str) -> None:
    ts = time.strftime("%H:%M:%S")
    print(f"[procwatch] {ts} {msg}", flush=True)

def _init_dirs() -> None:
    PROC_WATCH_DIR.mkdir(parents=True, exist_ok=True)

def _read_proc_stats(pid: int) -> dict | None:
    """Odczytaj /proc/[pid]/stat + status dla jednego PID."""
    try:
        with open(f"/proc/{pid}/stat") as f:
            parts = f.read().split()
        comm = parts[1].strip("()")
        state = parts[2]
        # Czas startu: field 21 (starttime) w ticks od boot
        starttime_ticks = int(parts[21]) if len(parts) > 21 else 0

        # Clamp do rozsądnego zakresu
        try:
            uptime_ticks = os.sysconf("SC_CLK_TCK") * 60 * 60 * 24 * 7  # 7 dni w tickach
        except (ValueError, AttributeError):
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_proc_watch_daemon.py:93 quiet except scope=_read_proc_stats reason=assign_fallback")
            raise
            uptime_ticks = 100 * 60 * 60 * 24 * 7  # fallback
        starttime_ticks = max(0, min(starttime_ticks, uptime_ticks))
        # Normalizuj do [0, 1] → φ
        norm_start = starttime_ticks / max(uptime_ticks, 1)

        cpu_percent = 0.0
        mem_percent = 0.0
        uid = 65535
        try:
            with open(f"/proc/{pid}/status") as sf:
                for line in sf:
                    if line.startswith("VmRSS:"):
                        mem_str = line.split()[1]
                        mem_kb = int(mem_str)
                        try:
                            total_mem_kb = os.sysconf("SC_PHYS_PAGES") * \
                                           os.sysconf("SC_PAGE_SIZE") // 1024
                        except (ValueError, AttributeError):
                            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_proc_watch_daemon.py:111 quiet except scope=_read_proc_stats reason=assign_fallback")
                            raise
                            total_mem_kb = 16 * 1024 * 1024  # fallback 16GB
                        mem_percent = min(100.0, 100.0 * mem_kb / max(total_mem_kb, 1))
                    elif line.startswith("Uid:"):
                        uid = int(line.split()[1])
        except (FileNotFoundError, PermissionError, ValueError):
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_proc_watch_daemon.py:116 quiet except scope=_read_proc_stats reason=assign_fallback")
            raise
            uid = 65535

        try:
            with open(f"/proc/{pid}/stat") as sf:  # already read
                parts2 = sf.read().split()
            utime = int(parts2[13])
            stime = int(parts2[14])
            cutime = int(parts2[15])
            cstime = int(parts2[16])
            total_time = utime + stime + cutime + cstime
            try:
                clk_tck = os.sysconf("SC_CLK_TCK")
            except (ValueError, AttributeError):
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_proc_watch_daemon.py:129 quiet except scope=_read_proc_stats reason=assign_fallback")
                raise
                clk_tck = 100
            cpu_percent = min(100.0, 100.0 * total_time / max(clk_tck * 1.0, 1))
        except (FileNotFoundError, PermissionError, ValueError, IndexError):
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_proc_watch_daemon.py:132 quiet except scope=_read_proc_stats reason=pass")
            raise
            pass

        important = comm in IMPORTANT_COMMS or uid == 0

        return {
            "pid": pid,
            "comm": comm,
            "state": state,
            "uid": uid,
            "cpu_percent": round(cpu_percent, 1),
            "mem_percent": round(mem_percent, 2),
            "starttime_norm": round(norm_start, 4),
            "important": important,
        }
    except (FileNotFoundError, PermissionError, ValueError, IndexError):
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_proc_watch_daemon.py:147 quiet except scope=_read_proc_stats reason=return None")
        raise
        return None

def _scan() -> None:
    """Skanuj /proc, porównaj z poprzednim stanem, raportuj zmiany."""
    global _prev_pids, _prev_stats, _total_births, _total_deaths

    now = time.time()
    current_pids: set[int] = set()

    try:
        for entry in os.listdir("/proc"):
            if entry.isdigit():
                current_pids.add(int(entry))
    except FileNotFoundError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_proc_watch_daemon.py:161 quiet except scope=_scan reason=return None")
        raise
        return

    # Detekcja nowych PIDs (birth)
    new_pids = current_pids - _prev_pids
    # Detekcja znikniętych PIDs (death)
    dead_pids = _prev_pids - current_pids

    # Przetwarzaj nowe
    births_this_cycle = 0
    for pid in sorted(new_pids)[:20]:  # max 20 per scan
        stat = _read_proc_stats(pid)
        if stat:
            births_this_cycle += 1
            _new_ring.append({
                "ts": now,
                "event": "birth",
                **stat,
            })
            _prev_stats[pid] = (now, stat["comm"])
            _total_births += 1
            _fork_rate.append(now)

    # Przetwarzaj zniknięte
    for pid in dead_pids:
        start_info = _prev_stats.pop(pid, (now, "?"))
        age = now - start_info[0]
        _dead_ring.append({
            "ts": now,
            "event": "death",
            "pid": pid,
            "comm": start_info[1],
            "age": round(age, 1),
            "age_str": f"{age:.0f}s" if age < 3600 else f"{age/3600:.1f}h",
        })
        _total_deaths += 1

    _prev_pids = current_pids

    # Exec rate = births/sec w ostatnich 30s
    while _exec_rate and _exec_rate[0] < now - 30:
        _exec_rate.popleft()
    if births_this_cycle > 0:
        _exec_rate.append(now)

    # Zapisz na surface
    _write_surface()

def _write_surface() -> None:
    """Zapisz stan monitora na surface."""
    now = time.time()

    birth_rate = len(_exec_rate) / 30.0 if _exec_rate else 0.0
    fork_rate_raw = len(_fork_rate) / 30.0 if _fork_rate else 0.0

    # stats.json
    stats = {
        "ts": now,
        "total_births": _total_births,
        "total_deaths": _total_deaths,
        "birth_rate": round(birth_rate, 2),
        "fork_rate": round(fork_rate_raw, 2),
        "alive_pids": len(_prev_pids),
        "recent_births": len(_new_ring),
        "recent_deaths": len(_dead_ring),
    }

    # Ostatnie narodziny (ważne)
    important_births = [e for e in _new_ring if e.get("important")]
    if important_births:
        stats["last_important_birth"] = important_births[-1]

    # Ostatnia śmierć
    if _dead_ring:
        stats["last_death"] = _dead_ring[-1]

    with open(PROC_WATCH_DIR / "stats.json", "w") as f:
        json.dump(stats, f, indent=2)

    # new_pids.jsonl
    with open(PROC_WATCH_DIR / "new_pids.jsonl", "w") as f:
        for entry in _new_ring:
            f.write(json.dumps(entry) + "\n")

    # dead_pids.jsonl
    with open(PROC_WATCH_DIR / "dead_pids.jsonl", "w") as f:
        for entry in _dead_ring:
            f.write(json.dumps(entry) + "\n")

    # PROC_WATCH → surface bridge plik:
    # fork_rate jako liczba zmiennoprzecinkowa do ω modulation
    (PROC_WATCH_DIR / "fork_rate").write_text(str(round(fork_rate_raw, 4)))
    (PROC_WATCH_DIR / "birth_rate").write_text(str(round(birth_rate, 4)))

def signal_handler(sig, frame) -> None:
    global _running
    log(f"signal {sig}, exiting")
    _running = False

def main() -> None:
    global _prev_pids

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    _init_dirs()

    # Init: wczytaj aktualne PIDy
    try:
        _prev_pids = {int(e) for e in os.listdir("/proc") if e.isdigit()}
        # Wczytaj podstawowe info o żywych
        for pid in list(_prev_pids)[:500]:
            stat = _read_proc_stats(pid)
            if stat:
                _prev_stats[pid] = (time.time(), stat["comm"])
    except FileNotFoundError:
        log("ERROR: /proc not found")
        return

    log(f"init — {len(_prev_pids)} PIDs monitored")

    if "--once" in sys.argv:
        _scan()
        print((PROC_WATCH_DIR / "stats.json").read_text())
        return

    log("daemon start")
    hb_count = 0
    reg_token = registry.register("proc-watch")
    while _running:
        hb_count += 1
        if hb_count % 30 == 0:
            try:
                registry.heartbeat(reg_token)
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_proc_watch_daemon.py:295 quiet except scope=main reason=pass")
                raise
                pass

        try:
            _scan()
        except Exception as e:
            log(f"error: {e}")
            import traceback
            traceback.print_exc()

        # Interwał 1s
        for _ in range(10):
            if not _running:
                break
            time.sleep(0.1)

    log(f"daemon stop — {_total_births} births, {_total_deaths} deaths")

if __name__ == "__main__":
    main()
