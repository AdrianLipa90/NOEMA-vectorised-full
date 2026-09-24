"""CIEL Unified Daemon Base — shared skeleton for all NOEMA daemons.

Eliminates 29× copy-paste of: binding check, ROOT/sys.path, logging,
signal handling, PID file, surface mmap, registry heartbeat, main loop,
tick counter, shutdown cleanup.

Usage:
    from ciel_geometry.daemon_base import CielDaemon

    class MyDaemon(CielDaemon):
        NAME = "kuramoto"
        INTERVAL = 0.1  # seconds

        def tick(self):
            ...  # your logic here

    if __name__ == "__main__":
        MyDaemon().run()

Autorzy: Adrian Lipa & CIEL (2026)
"""
from __future__ import annotations

import json
import logging
import os
import signal
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

# ── ROOT / sys.path ──────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent.parent
SRC = str(ROOT / "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

# ── CIEL ORBITAL BINDING check ───────────────────────────────────
_BINDING_PATH = Path("/dev/shm/ciel_noema/ciel_binding_status")
_log = logging.getLogger(__name__)

def _check_binding(daemon_name: str) -> None:
    try:
        if not (_BINDING_PATH.exists() and _BINDING_PATH.read_text().strip() == "ACTIVE"):
            import warnings
            warnings.warn(f"CIEL ORBITAL BINDING: not ACTIVE on daemon {daemon_name}")
    except Exception as exc:
        _log.debug("binding check skipped: %s", exc)

# ── Base class ────────────────────────────────────────────────────
class CielDaemon:
    """Base for all NOEMA daemons. Subclass and override NAME, INTERVAL, tick()."""

    NAME: str = "unnamed"
    INTERVAL: float = 1.0          # seconds between ticks
    PID_DIR: Path = Path("/tmp")
    SURFACE_ROOT: Path = Path("/dev/shm/ciel_noema")
    HEARTBEAT_INTERVAL: float = 30.0
    REGISTER: bool = True          # set False to skip registry

    def __init__(self) -> None:
        _check_binding(self.NAME)

        self._running = True
        self._tick_count = 0
        self._start_time = time.time()
        self._token: str | None = None
        self._registry: Any = None
        self._surface: dict[str, Any] = {}

        # logging
        logging.basicConfig(
            level=logging.INFO,
            format=f"[{self.NAME}] %(asctime)s %(message)s",
            datefmt="%H:%M:%S",
        )
        self.log = logging.getLogger(f"noema.{self.NAME}")

        # signal handlers
        signal.signal(signal.SIGTERM, self._handle_sigterm)
        signal.signal(signal.SIGINT, self._handle_sigterm)
        try:
            signal.signal(signal.SIGUSR1, self._handle_sigusr1)
        except (AttributeError, OSError):
            pass  # SIGUSR1 not available on all platforms

    # ── Signals ───────────────────────────────────────────────────
    def _handle_sigterm(self, signum: int, frame: Any) -> None:
        self.log.info("SIGTERM received, shutting down")
        self._running = False

    def _handle_sigusr1(self, signum: int, frame: Any) -> None:
        self.log.info("SIGUSR1 — status dump")
        self._dump_status()

    def _dump_status(self) -> None:
        elapsed = time.time() - self._start_time
        self.log.info(
            "tick=%d elapsed=%.0fs surface_keys=%s",
            self._tick_count, elapsed, list(self._surface.keys()),
        )

    # ── PID file ──────────────────────────────────────────────────
    @property
    def pid_path(self) -> Path:
        return self.PID_DIR / f"ciel_{self.NAME}.pid"

    def _write_pid(self) -> None:
        self.pid_path.write_text(str(os.getpid()))
        self.log.info("PID %d → %s", os.getpid(), self.pid_path)

    def _remove_pid(self) -> None:
        try:
            self.pid_path.unlink(missing_ok=True)
        except Exception as exc:
            self.log.debug("pid unlink skipped: %s", exc)

    # ── Registry ──────────────────────────────────────────────────
    def _setup_registry(self) -> None:
        if not self.REGISTER:
            return
        try:
            from ciel_geometry.noema_registry import registry
            self._registry = registry
            self._token = self._registry.register(
                self.NAME,
                surface_claims=["tick"],
            )
            self.log.info("registered as %s", self._token)
        except Exception as e:
            self.log.debug("registry unavailable: %s", e)
            self._registry = None

    def _heartbeat(self) -> None:
        if self._registry and self._token:
            try:
                self._registry.heartbeat(self._token)
            except Exception as exc:
                self.log.debug("heartbeat skipped: %s", exc)

    def _unregister(self) -> None:
        if self._registry and self._token:
            try:
                self._registry.unregister(self._token)
            except Exception as exc:
                self.log.debug("unregister skipped: %s", exc)

    # ── Surface ───────────────────────────────────────────────────
    def _open_surface(self) -> None:
        try:
            from ciel_geometry.noema_surface_mmap import open_surface, ensure_surface
            ensure_surface()
            self._surface = open_surface()
            self.log.info("surface opened, keys=%s", list(self._surface.keys()))
        except Exception as e:
            self.log.debug("surface unavailable: %s", e)
            self._surface = {}

    def _read_phi(self) -> np.ndarray | None:
        phi = self._surface.get("phi")
        if phi is not None:
            return np.asarray(phi, dtype=np.float64)
        return None

    def _write_phi(self, phi: np.ndarray) -> None:
        if "phi" in self._surface:
            self._surface["phi"][:36] = phi[:36]

    def _read_tick(self) -> int:
        t = self._surface.get("tick")
        if t is None:
            raise RuntimeError("NOEMA surface tick is unavailable")
        values = np.asarray(t)
        if values.size != 1:
            raise RuntimeError(
                f"NOEMA surface tick violates scalar contract: shape={values.shape}"
            )
        return int(values.reshape(-1)[0])

    def _write_scalar(self, key: str, value: float) -> None:
        if key in self._surface:
            self._surface[key] = value

    # ── Lifecycle (override these) ────────────────────────────────
    def setup(self) -> None:
        """Called once before main loop. Override for init logic."""
        self._open_surface()
        self._setup_registry()
        self._write_pid()

    def tick(self) -> None:
        """Called every INTERVAL seconds. Override with your logic."""
        raise NotImplementedError

    def shutdown(self) -> None:
        """Called on exit. Override for cleanup logic."""
        self._unregister()
        self._remove_pid()

    # ── Main loop ─────────────────────────────────────────────────
    def run(self) -> None:
        self.log.info("starting (interval=%.3fs)", self.INTERVAL)
        self.setup()
        last_heartbeat = time.time()

        try:
            while self._running:
                loop_start = time.time()
                try:
                    self.tick()
                    self._tick_count += 1
                except Exception as e:
                    if self._running:
                        self.log.debug("tick error: %s", e)
                        time.sleep(min(self.INTERVAL * 2, 5.0))

                # heartbeat
                now = time.time()
                if now - last_heartbeat >= self.HEARTBEAT_INTERVAL:
                    self._heartbeat()
                    last_heartbeat = now

                # sleep remainder
                elapsed = time.time() - loop_start
                sleep_time = max(0, self.INTERVAL - elapsed)
                if sleep_time > 0 and self._running:
                    time.sleep(sleep_time)
        finally:
            self.log.info(
                "stopping after %d ticks (%.0fs)",
                self._tick_count, time.time() - self._start_time,
            )
            self.shutdown()
