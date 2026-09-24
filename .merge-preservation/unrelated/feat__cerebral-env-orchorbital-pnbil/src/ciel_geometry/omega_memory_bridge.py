"""
CIEL Omega Memory Bridge — łączy agenta z TSM ledgerem pamięci.

Używa bezpośrednio SQLite na memory_ledger.db (95 istniejących wpisów)
oraz PhaseMemory z CIELingo. Nie wymaga pełnego importu Omega.

API:
    store(memorise_id, content, D_associations="")
    retrieve(query, top_k=5) -> list[dict]
    recent(n=10) -> list[dict]
    stats() -> dict
    integrate_with_agent(state_db) -> None
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

# CIEL ORBITAL BINDING — hardcoded, immutable.
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on import of " + __name__)


import json
import math
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ── Ścieżki ──────────────────────────────────────────────────

_TSM_LEDGER = (
    Path(__file__).resolve().parent.parent
    / "CIEL_MEMORY_SYSTEM" / "TSM" / "ledger" / "memory_ledger.db"
)

_TSM_OMEGA = (
    Path(__file__).resolve().parent.parent
    / "CIEL_OMEGA_COMPLETE_SYSTEM" / "CIEL_MEMORY_SYSTEM" / "TSM" / "ledger" / "memory_ledger.db"
)

# Użyj tej która istnieje
if _TSM_OMEGA.exists() and _TSM_OMEGA.stat().st_size > _TSM_LEDGER.stat().st_size:
    _DB_PATH = _TSM_OMEGA
else:
    _DB_PATH = _TSM_LEDGER


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(str(_DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def _ensure_schema():
    """Upewnij się że tabela memories istnieje."""
    conn = _conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            memorise_id TEXT PRIMARY KEY,
            created_at TEXT,
            D_id TEXT,
            D_context TEXT,
            D_sense TEXT,
            D_associations TEXT,
            D_timestamp TEXT,
            D_meta TEXT,
            D_type TEXT,
            D_attr TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS memory_edges (
            src_id TEXT,
            dst_id TEXT,
            weight REAL,
            phase_diff REAL,
            co_activations INTEGER DEFAULT 0,
            last_activation TEXT,
            PRIMARY KEY (src_id, dst_id)
        )
    """)
    conn.commit()
    conn.close()


# ── Public API ─────────────────────────────────────────────────

def store(
    memorise_id: str,
    content: str,
    context: str = "",
    sense: str = "lingophysical",
    associations: str = "",
    meta: str = "",
    mem_type: str = "agent_log",
) -> bool:
    """Zapisz wpis do TSM ledger."""
    try:
        _ensure_schema()
        ts = datetime.now(timezone.utc).isoformat()
        conn = _conn()
        # D_context = główna treść wpisu
        d_ctx = (content[:512] + "…") if len(content) > 512 else content
        conn.execute("""
            INSERT OR REPLACE INTO memories
                (memorise_id, created_at, D_id, D_context, D_sense,
                 D_associations, D_timestamp, D_meta, D_type, D_attr)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (
            memorise_id[:64],
            ts,
            memorise_id[:64],
            d_ctx,
            sense[:64] if sense else "",
            (context[:256] if context else "") + " | " + (associations[:256] if associations else ""),
            ts,
            meta[:256] if meta else "",
            mem_type[:32],
            "",
        ))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[OmegaBridge] store error: {e}")
        return False


def retrieve(query: str, top_k: int = 5) -> list[dict]:
    """Proste wyszukiwanie po D_context (LIKE)."""
    try:
        conn = _conn()
        rows = conn.execute("""
            SELECT memorise_id, D_context, D_sense, D_associations,
                   D_type, D_timestamp, D_meta
            FROM memories
            WHERE D_context LIKE ? OR D_associations LIKE ?
            ORDER BY D_timestamp DESC
            LIMIT ?
        """, (f"%{query}%", f"%{query}%", top_k)).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception as e:
        print(f"[OmegaBridge] retrieve error: {e}")
        return []


def recent(n: int = 10) -> list[dict]:
    """Ostatnie N wpisów."""
    try:
        conn = _conn()
        rows = conn.execute("""
            SELECT memorise_id, D_context, D_sense, D_type, D_timestamp
            FROM memories
            ORDER BY D_timestamp DESC
            LIMIT ?
        """, (n,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/omega_memory_bridge.py:161 quiet except scope=recent reason=return []")
        return []


def store_exchange(
    user_msg: str,
    assistant_msg: str,
    session_id: str = "",
):
    """Zapisz wymianę użytkownik ↔ agent do TSM."""
    memorise_id = f"agent_{session_id}_{int(time.time())}" if session_id else f"agent_{int(time.time())}"
    content = f"USER: {user_msg[:300]}\nASSISTANT: {assistant_msg[:300]}"
    store(memorise_id, content, context=user_msg[:200],
          sense="agent_exchange", associations=assistant_msg[:200],
          mem_type="agent_exchange")


def integrate_with_agent(state_db) -> dict:
    """Integruj agent state_db z Omega memory — tworzy wpisy dla kluczowych stanów."""
    results = {"stored": 0, "errors": 0}
    try:
        # Pobierz stan z state_db
        closure = state_db.get("closure_penalty", 0)
        soul = state_db.get("soul_invariant", 0)
        coherence = state_db.get("coherence_index", 0)

        # Zapisz snapshot stanu jako wpis pamięci
        memorise_id = f"state_snapshot_{int(time.time())}"
        content = json.dumps({
            "closure_penalty": closure,
            "soul_invariant": soul,
            "coherence_index": coherence,
            "ts": datetime.now(timezone.utc).isoformat(),
        })
        ok = store(memorise_id, content, context="System state snapshot",
                    sense="state", mem_type="state_snapshot")
        if ok:
            results["stored"] += 1
    except Exception as e:
        results["errors"] += 1
        print(f"[OmegaBridge] integrate error: {e}")
    return results


def stats() -> dict:
    """Statystyki bazy pamięci."""
    try:
        conn = _conn()
        total = conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
        edges = conn.execute("SELECT COUNT(*) FROM memory_edges").fetchone()[0]
        types = conn.execute(
            "SELECT D_type, COUNT(*) as cnt FROM memories GROUP BY D_type ORDER BY cnt DESC"
        ).fetchall()
        conn.close()
        return {
            "total_entries": total,
            "total_edges": edges,
            "db_path": str(_DB_PATH),
            "db_size_kb": round(_DB_PATH.stat().st_size / 1024, 1),
            "types": {r[0]: r[1] for r in types},
        }
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/omega_memory_bridge.py:222 quiet except scope=stats reason=return {\"error\": \"cannot read TSM\"}")
        return {"error": "cannot read TSM"}


# ── Init ──────────────────────────────────────────────────────

_ensure_schema()

print(f"[OmegaBridge]  TSM ledger: {_DB_PATH}")
print(f"[OmegaBridge]  Ready — {stats().get('total_entries', '?')} existing memories")
