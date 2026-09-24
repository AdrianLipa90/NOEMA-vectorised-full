# CIEL Server Hub — Snapshot Cache
# Warstwa cache'owania kosztownych odczytów (mmap, SQLite, systemd)
# Odświeżanie w tle na osobnych interwałach
# Autor: Adrian Lipa & CIEL
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

# ─── Konfiguracja snapshotów ──────────────────────────────────────────────

SNAPSHOT_DIR = Path("/dev/shm/ciel_noema")


@dataclass
class SnapshotDef:
    """Definicja snapshotu: co, jak często, jak odświeżać."""
    key: str
    interval_s: float
    fetcher: Callable[[], Any]
    last_fetch: float = 0.0
    cached: Any = None
    error: str | None = None


class SnapshotCache:
    """Cache warstwa — odświeża snapshoty w tle na osobnych interwałach.
    
    Wzorzec:
        cache = SnapshotCache()
        cache.register("surface", fetcher=read_surface, interval=1.0)
        cache.register("daemons", fetcher=scan_daemons, interval=2.0)
        cache.start()
        data = cache.get("surface")
    """

    def __init__(self, auto_start: bool = False) -> None:
        self._snapshots: dict[str, SnapshotDef] = {}
        self._lock = threading.Lock()
        self._thread: threading.Thread | None = None
        self._running = False
        self._hub_snapshot_path = SNAPSHOT_DIR / "hub_snapshot.json"
        if auto_start:
            self.start()

    def register(self, key: str, fetcher: Callable[[], Any], interval: float = 5.0) -> None:
        """Rejestruje snapshot."""
        with self._lock:
            self._snapshots[key] = SnapshotDef(
                key=key,
                interval_s=interval,
                fetcher=fetcher,
            )

    def unregister(self, key: str) -> None:
        """Usuwa snapshot."""
        with self._lock:
            self._snapshots.pop(key, None)

    def get(self, key: str, default: Any = None) -> Any:
        """Zwraca cachowaną wartość snapshotu."""
        with self._lock:
            sd = self._snapshots.get(key)
            if sd is not None:
                return sd.cached if sd.error is None else default
        return default

    def get_all(self) -> dict[str, Any]:
        """Zwraca wszystkie snapshoty jako dict."""
        result: dict[str, Any] = {}
        with self._lock:
            for key, sd in self._snapshots.items():
                if sd.error is None:
                    result[key] = sd.cached
                else:
                    result[key] = {"error": sd.error}
        return result

    def _refresh_one(self, sd: SnapshotDef) -> None:
        """Odświeża pojedynczy snapshot."""
        try:
            data = sd.fetcher()
            with self._lock:
                sd.cached = data
                sd.error = None
                sd.last_fetch = time.time()
        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_hub/snapshot.py:91 quiet except scope=SnapshotCache._refresh_one reason=With")
            with self._lock:
                sd.error = str(e)

    def _refresh_all(self) -> None:
        """Odświeża wszystkie snapshoty, które są do odświeżenia."""
        now = time.time()
        for sd in list(self._snapshots.values()):
            if now - sd.last_fetch >= sd.interval_s:
                self._refresh_one(sd)

    def _save_hub_snapshot(self) -> None:
        """Zapisuje wszystkie snapshoty do pliku hub_snapshot.json."""
        try:
            data = self.get_all()
            data["_meta"] = {
                "ts": time.time(),
                "snapshots": len(self._snapshots),
            }
            self._hub_snapshot_path.write_text(json.dumps(data, ensure_ascii=False, default=str))
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_hub/snapshot.py:111 quiet except scope=SnapshotCache._save_hub_snapshot reason=pass")
            pass

    def _loop(self) -> None:
        """Główna pętla odświeżania."""
        while self._running:
            try:
                self._refresh_all()
                self._save_hub_snapshot()
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_hub/snapshot.py:120 quiet except scope=SnapshotCache._loop reason=pass")
                pass
            time.sleep(1.0)

    def start(self) -> None:
        """Uruchamia pętlę snapshotów w tle."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Zatrzymuje pętlę snapshotów."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=3.0)

    def status(self) -> dict:
        """Zwraca status cache."""
        with self._lock:
            return {
                "snapshots": len(self._snapshots),
                "keys": list(self._snapshots.keys()),
                "running": self._running,
            }


# ─── Globalna instancja ──────────────────────────────────────────────────
cache = SnapshotCache()
