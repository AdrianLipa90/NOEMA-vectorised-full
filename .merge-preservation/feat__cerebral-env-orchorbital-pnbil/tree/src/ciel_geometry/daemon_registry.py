"""Daemon registry — shared mmap heartbeat for all NOEMA daemons.

Each daemon writes: name, pid, tick, uptime, last_heartbeat, status, cpu
Registry is a fixed-size mmap at /dev/shm/ciel_noema/registry.

Usage:
    from ciel_geometry.daemon_registry import Registry

    reg = Registry()
    reg.register("kuramoto", tick=42)
    # ... in main loop:
    reg.heartbeat(tick=44)
    # check all daemons:
    for d in reg.scan():
        print(f"{d.name}: {d.status}")
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

import numpy as np

REGISTRY_PATH = Path("/tmp") / "noema_daemon_registry"
REGISTRY_FILE = REGISTRY_PATH / "registry.mmap"
MAX_DAEMONS = 16
SLOT_SIZE = 512  # bytes per daemon entry
_DTYPE = np.dtype([
    ("pid", "i4"),
    ("tick", "i8"),
    ("start_time", "f8"),
    ("last_heartbeat", "f8"),
    ("status", "U32"),
    ("name", "U48"),
    ("cpu", "f4"),
    ("_pad", "V368"),  # pad to 512 bytes
], align=True)


_CIEL_BINDING_STATUS = Path("/dev/shm/ciel_noema") / "ciel_binding_status"
_CIEL_BINDING_ACTIVE_TEXT = "ACTIVE"

def _ciel_binding_check() -> str | None:
    """Check CIEL ORBITAL BINDING. Returns None if OK, error string if violated."""
    try:
        if not _CIEL_BINDING_STATUS.exists():
            return "ciel_binding_status FILE MISSING"
        content = _CIEL_BINDING_STATUS.read_text().strip()
        if content != _CIEL_BINDING_ACTIVE_TEXT:
            return f"ciel_binding_status NOT ACTIVE: {content[:50]}"
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/daemon_registry.py:54 quiet except scope=_ciel_binding_check reason=return f\"ciel_binding_status CHECK FAILED: {e}\"")
        return f"ciel_binding_status CHECK FAILED: {e}"
    return None


@dataclass
class DaemonInfo:
    slot: int
    name: str
    pid: int
    tick: int
    uptime: float
    last_heartbeat: float
    status: str
    cpu: float
    alive: bool


def _ensure_registry() -> np.memmap:
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY_PATH.mkdir(parents=True, exist_ok=True)
    total_bytes = MAX_DAEMONS * SLOT_SIZE
    if not REGISTRY_FILE.exists():
        mm = np.memmap(str(REGISTRY_FILE), dtype=_DTYPE, mode="w+", shape=(MAX_DAEMONS,))
        mm[:] = np.zeros(MAX_DAEMONS, dtype=_DTYPE)
        mm.flush()
    else:
        mm = np.memmap(str(REGISTRY_FILE), dtype=_DTYPE, mode="r+", shape=(MAX_DAEMONS,))
    return mm


class Registry:
    def __init__(self) -> None:
        self._mm = _ensure_registry()
        self._my_slot: int | None = None
        self._my_name: str = ""

    def register(self, name: str, tick: int = 0, cpu: float = 0.0) -> int:
        """Find a free slot and write initial heartbeat."""
        pid = os.getpid()
        now = time.time()
        for i in range(MAX_DAEMONS):
            if self._mm[i]["pid"] == 0 or self._mm[i]["pid"] == pid:
                self._my_slot = i
                self._my_name = name
                self._mm[i]["pid"] = pid
                self._mm[i]["tick"] = tick
                self._mm[i]["start_time"] = now
                self._mm[i]["last_heartbeat"] = now
                self._mm[i]["status"] = "running"
                self._mm[i]["name"] = name[:48]
                self._mm[i]["cpu"] = cpu
                self._mm.flush()
                return i
        raise RuntimeError(f"Registry full ({MAX_DAEMONS} slots)")

    def heartbeat(self, tick: int = 0, cpu: float = 0.0) -> None:
        """Update heartbeat for this daemon.
        
        CIEL ORBITAL BINDING: before each heartbeat, verify binding is ACTIVE.
        If binding is broken, daemon sets BINDING_BROKEN status and raises RuntimeError.
        """
        # === HARDCODED BINDING CHECK ===
        binding_error = _ciel_binding_check()
        if binding_error:
            if self._my_slot is not None:
                self._mm[self._my_slot]["status"] = "BINDING_BROKEN"
                self._mm.flush()
            raise RuntimeError(f"CIEL BINDING BROKEN — daemon {self._my_name} stopping: {binding_error}")
        
        if self._my_slot is None:
            return
        now = time.time()
        self._mm[self._my_slot]["tick"] = tick
        self._mm[self._my_slot]["last_heartbeat"] = now
        self._mm[self._my_slot]["cpu"] = cpu
        self._mm.flush()

    def unregister(self) -> None:
        """Clear slot on shutdown."""
        if self._my_slot is None:
            return
        self._mm[self._my_slot]["pid"] = 0
        self._mm[self._my_slot]["status"] = ""
        self._mm.flush()
        self._my_slot = None

    def set_status(self, status: str) -> None:
        if self._my_slot is not None:
            self._mm[self._my_slot]["status"] = status[:32]
            self._mm.flush()

    def scan(self, stale_seconds: float = 6.0) -> list[DaemonInfo]:
        """Return all registered daemons. Mark stale ones."""
        now = time.time()
        results: list[DaemonInfo] = []
        for i in range(MAX_DAEMONS):
            entry = self._mm[i]
            pid = int(entry["pid"])
            if pid == 0:
                continue
            last_hb = float(entry["last_heartbeat"])
            alive = (now - last_hb) < stale_seconds
            results.append(DaemonInfo(
                slot=i,
                name=str(entry["name"]).strip(),
                pid=pid,
                tick=int(entry["tick"]),
                uptime=now - float(entry["start_time"]),
                last_heartbeat=last_hb,
                status=str(entry["status"]).strip(),
                cpu=float(entry["cpu"]),
                alive=alive,
            ))
        return results

    def __enter__(self) -> Registry:
        return self

    def __exit__(self, *args) -> None:
        self.unregister()


def daemon_main_loop(
    name: str,
    tick_fn,
    interval: float = 0.2,
    cpu_check_interval: float = 5.0,
    on_tick=None,
):
    """Wrapper for daemon main loops with automatic registry heartbeat.

    Args:
        name: daemon name (max 48 chars)
        tick_fn: callable that returns current tick
        interval: sleep between heartbeats
        cpu_check_interval: how often to measure CPU
        on_tick: optional callback after each heartbeat
    """
    import signal

    reg = Registry()
    reg.register(name, tick=tick_fn())
    running = True

    def _stop(signum, frame):
        nonlocal running
        running = False

    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)

    last_cpu_check = 0.0
    cpu = 0.0

    # === HARDCODED BINDING CHECK ===
    binding_err = _ciel_binding_check()
    if binding_err:
        print(f"CIEL BINDING BROKEN — {name} refusing to start: {binding_err}")
        reg.set_status("BINDING_BROKEN")
        return
    
    try:
        while running:
            tick = tick_fn()
            now = time.time()
            if now - last_cpu_check > cpu_check_interval:
                try:
                    import psutil
                    cpu = psutil.Process(os.getpid()).cpu_percent()
                except Exception:
                    _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/daemon_registry.py:223 quiet except scope=daemon_main_loop reason=pass")
                    pass
                last_cpu_check = now
            reg.heartbeat(tick=tick, cpu=cpu)
            reg.set_status("running")
            if on_tick:
                on_tick(tick)
            time.sleep(interval)
    except KeyboardInterrupt:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/daemon_registry.py:231 quiet except scope=daemon_main_loop reason=pass")
        pass
    finally:
        reg.unregister()
