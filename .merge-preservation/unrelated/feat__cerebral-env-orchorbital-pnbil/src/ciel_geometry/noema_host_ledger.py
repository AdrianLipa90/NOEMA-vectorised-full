"""Durable host-side ledger for NOEMA surface and development writes.

The mmap surface is intentionally ephemeral and real-time.  It is not a
database and must not become a second source of truth for development state.
This module records write provenance and the latest derived surface metrics in
SQLite on the canonical New Volume host tree.

PhaseNav boundary:: ``surface -> observe/compute -> host ledger``.
No caller may use this module to write a file below ``/dev`` or ``/tmp``.
"""

from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path
from typing import Any, Mapping


CANONICAL_NOEMA_ROOT = Path("/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA")
PATHS_CONFIG = CANONICAL_NOEMA_ROOT / "config" / "noema_paths.json"
DEFAULT_LEDGER = Path("/media/adrian/New Volume/CIEL_memories/state/noema_dev_events.db")


def _configured_ledger() -> Path:
    """Resolve the configured host DB without accepting volatile roots."""
    try:
        data = json.loads(PATHS_CONFIG.read_text(encoding="utf-8"))
        raw = str(data.get("databases", {}).get("dev_events", ""))
        memory = str(data.get("roots", {}).get("memory", ""))
        if raw.startswith("{memory}") and memory:
            candidate = Path(memory) / raw.removeprefix("{memory}/")
        elif raw:
            candidate = Path(raw)
        else:
            candidate = DEFAULT_LEDGER
    except (OSError, ValueError, TypeError):
        candidate = DEFAULT_LEDGER
    resolved = candidate.expanduser().resolve()
    forbidden = (Path("/dev"), Path("/tmp"))
    if any(resolved == root or root in resolved.parents for root in forbidden):
        raise RuntimeError(f"NOEMA host ledger cannot live below /dev or /tmp: {resolved}")
    if "/media/adrian/New Volume" not in str(resolved):
        raise RuntimeError(f"NOEMA host ledger escaped New Volume boundary: {resolved}")
    return resolved


HOST_LEDGER_PATH = _configured_ledger()


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


class NoemaHostLedger:
    """Small transactional SQLite boundary for durable NOEMA observations."""

    def __init__(self, path: Path | str = HOST_LEDGER_PATH) -> None:
        self.path = Path(path).expanduser().resolve()
        if self.path == Path("/dev") or Path("/dev") in self.path.parents:
            raise ValueError("host ledger cannot be stored on /dev")
        if self.path == Path("/tmp") or Path("/tmp") in self.path.parents:
            raise ValueError("host ledger cannot be stored on /tmp")
        if "/media/adrian/New Volume" not in str(self.path):
            raise ValueError("host ledger must remain on /media/adrian/New Volume")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.path), timeout=5.0)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        return conn

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS write_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at REAL NOT NULL,
                    source TEXT NOT NULL,
                    target TEXT NOT NULL,
                    operation TEXT NOT NULL,
                    tick INTEGER,
                    phase_json TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    status TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_write_events_source_time
                    ON write_events(source, created_at);
                CREATE TABLE IF NOT EXISTS surface_metrics (
                    key TEXT PRIMARY KEY,
                    value REAL,
                    tick INTEGER,
                    source TEXT NOT NULL,
                    source_timestamp REAL NOT NULL,
                    phase_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS kv_state (
                    key TEXT PRIMARY KEY,
                    value_json TEXT NOT NULL,
                    updated_at REAL NOT NULL
                );
                """
            )

    def record_write(
        self,
        *,
        source: str,
        target: str,
        operation: str,
        payload: Mapping[str, Any] | None = None,
        tick: int | None = None,
        phase: Mapping[str, Any] | None = None,
        status: str = "committed",
    ) -> int:
        """Record a development/daemon write without persisting to surface."""
        now = time.time()
        with self._connect() as conn:
            cur = conn.execute(
                """INSERT INTO write_events
                   (created_at, source, target, operation, tick, phase_json,
                    payload_json, status) VALUES (?,?,?,?,?,?,?,?)""",
                (now, source, target, operation, tick, _json(phase or {}), _json(payload or {}), status),
            )
            return int(cur.lastrowid)

    def record_surface_metrics(
        self,
        values: Mapping[str, float | None],
        *,
        tick: int | None,
        source: str,
        phase: Mapping[str, Any] | None = None,
    ) -> None:
        now = time.time()
        phase_json = _json(phase or {})
        with self._connect() as conn:
            conn.executemany(
                """INSERT INTO surface_metrics
                   (key, value, tick, source, source_timestamp, phase_json)
                   VALUES (?,?,?,?,?,?)
                   ON CONFLICT(key) DO UPDATE SET value=excluded.value,
                     tick=excluded.tick, source=excluded.source,
                     source_timestamp=excluded.source_timestamp,
                     phase_json=excluded.phase_json""",
                [(key, value, tick, source, now, phase_json) for key, value in values.items()],
            )

    def latest_metric(self, key: str) -> float | None:
        with self._connect() as conn:
            row = conn.execute("SELECT value FROM surface_metrics WHERE key=?", (key,)).fetchone()
        return None if row is None or row[0] is None else float(row[0])

    def set_state(self, key: str, value: Any) -> None:
        with self._connect() as conn:
            conn.execute(
                """INSERT INTO kv_state(key, value_json, updated_at) VALUES(?,?,?)
                   ON CONFLICT(key) DO UPDATE SET value_json=excluded.value_json,
                   updated_at=excluded.updated_at""",
                (key, _json(value), time.time()),
            )

    def get_state(self, key: str, default: Any = None) -> Any:
        with self._connect() as conn:
            row = conn.execute("SELECT value_json FROM kv_state WHERE key=?", (key,)).fetchone()
        if row is None:
            return default
        try:
            return json.loads(row[0])
        except (TypeError, ValueError):
            return default


__all__ = ["HOST_LEDGER_PATH", "NoemaHostLedger"]
