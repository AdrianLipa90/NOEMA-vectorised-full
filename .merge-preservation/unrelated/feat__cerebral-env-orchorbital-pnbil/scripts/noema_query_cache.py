#!/usr/bin/env python3
"""NOEMA Query Cache — SQLite database of search queries, results, and PhaseNav metrics.

Usage:
    .venv/bin/python3 scripts/noema_query_cache.py --log "quantum gravity" gamma=0.95
    .venv/bin/python3 scripts/noema_query_cache.py --recent 20
    .venv/bin/python3 scripts/noema_query_cache.py --stats
"""
from __future__ import annotations

import json
import os
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_geometry.paths import P

PHASE_DATA = Path(os.environ.get("NOEMA_PHASE_DATA", Path(P.PHASE_DATA)))
DB_PATH = PHASE_DATA / "QUERY_CACHE" / "query_history.db"


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS queries (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            ts          TEXT NOT NULL,
            query       TEXT NOT NULL,
            top_result  TEXT,
            gamma       REAL,
            elapsed_ms  REAL,
            n_results   INTEGER,
            enhance     TEXT
        );
        CREATE TABLE IF NOT EXISTS search_results (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            query_id    INTEGER NOT NULL REFERENCES queries(id),
            rank        INTEGER NOT NULL,
            path        TEXT NOT NULL,
            gamma       REAL NOT NULL,
            size        INTEGER
        );
        CREATE TABLE IF NOT EXISTS surface_snapshots (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            ts          TEXT NOT NULL,
            tick        INTEGER NOT NULL,
            phi_mean    REAL,
            R           REAL,
            euler       REAL,
            gamma       REAL,
            unruh       REAL,
            mass        REAL,
            closure     REAL,
            holonomy_mean_A REAL,
            holonomy_closure REAL
        );
        CREATE INDEX IF NOT EXISTS idx_queries_ts ON queries(ts);
        CREATE INDEX IF NOT EXISTS idx_results_query ON search_results(query_id);
        CREATE INDEX IF NOT EXISTS idx_snapshots_tick ON surface_snapshots(tick);
    """)
    return conn


def log_query(query: str, gamma: float = 0.0, elapsed_ms: float = 0.0,
              n_results: int = 0, top_result: str = "", enhance: str = "") -> int:
    conn = _connect()
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        "INSERT INTO queries (ts, query, top_result, gamma, elapsed_ms, n_results, enhance) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (now, query[:500], top_result[:200], gamma, elapsed_ms, n_results, enhance),
    )
    qid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.commit()
    conn.close()
    return qid


def log_surface_snapshot(tick: int, phi_mean: float, R: float, euler: float,
                         gamma: float, unruh: float, mass: float, closure: float,
                         hol_mean_A: float = 0, hol_closure: float = 0) -> None:
    conn = _connect()
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        "INSERT INTO surface_snapshots "
        "(ts, tick, phi_mean, R, euler, gamma, unruh, mass, closure, holonomy_mean_A, holonomy_closure) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (now, tick, phi_mean, R, euler, gamma, unruh, mass, closure, hol_mean_A, hol_closure),
    )
    conn.commit()
    conn.close()


def recent_queries(n: int = 10) -> list[dict]:
    conn = _connect()
    rows = conn.execute(
        "SELECT * FROM queries ORDER BY id DESC LIMIT ?", (n,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def stats() -> dict:
    conn = _connect()
    total_q = conn.execute("SELECT COUNT(*) FROM queries").fetchone()[0]
    total_s = conn.execute("SELECT COUNT(*) FROM surface_snapshots").fetchone()[0]
    avg_gamma = conn.execute("SELECT AVG(gamma) FROM queries WHERE gamma IS NOT NULL").fetchone()[0]
    recent_tick = conn.execute("SELECT MAX(tick) FROM surface_snapshots").fetchone()[0]
    conn.close()
    return {
        "queries": total_q,
        "snapshots": total_s,
        "avg_gamma": round(avg_gamma or 0, 4),
        "last_tick": recent_tick or 0,
        "db_size": DB_PATH.stat().st_size if DB_PATH.exists() else 0,
    }


if __name__ == "__main__":
    if "--log" in sys.argv:
        idx = sys.argv.index("--log")
        query = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else ""
        gamma = float(sys.argv[sys.argv.index("--log") + 2]) if len(sys.argv) > idx + 2 else 0.0
        qid = log_query(query, gamma=gamma)
        print(json.dumps({"query_id": qid}))
    elif "--recent" in sys.argv:
        n = int(sys.argv[sys.argv.index("--recent") + 1]) if "--recent" in sys.argv and len(sys.argv) > sys.argv.index("--recent") + 1 else 10
        print(json.dumps(recent_queries(n), indent=2, default=str))
    elif "--stats" in sys.argv:
        print(json.dumps(stats(), indent=2))
    elif "--snapshot" in sys.argv:
        from ciel_geometry.noema_surface_mmap import ensure_surface
        import numpy as np
        s = ensure_surface()
        phi = np.asarray(s["phi"])
        g = np.asarray(s["gravity"])
        h = np.asarray(s["holonomy"]) if "holonomy" in s else np.zeros(7)
        z = np.exp(1j * phi)
        log_surface_snapshot(
            tick=int(s["tick"][0]),
            phi_mean=float(np.mean(phi)),
            R=float(np.abs(z.mean())),
            euler=float(np.abs(z.sum())),
            gamma=float(g[1]),
            unruh=float(g[3]),
            mass=float(g[2]),
            closure=1 - float(np.asarray(s["flavor"])[3]),
            hol_mean_A=float(h[0]),
            hol_closure=float(h[2]),
        )
        print(json.dumps({"status": "ok"}))
    else:
        print(__doc__)
