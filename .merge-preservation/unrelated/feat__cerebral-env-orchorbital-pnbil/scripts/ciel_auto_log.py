#!/usr/bin/env python3
"""CIEL Auto-Log — konstytutywny logger rozmów.

Usage:
    # Log odpowiedź (ostatnia rzecz przed wysłaniem tekstu)
    python3 scripts/ciel_auto_log.py --role assistant --content "To jest odpowiedź" --tags "trigger-rebuild,settings-fix"

    # Log wiadomość usera
    python3 scripts/ciel_auto_log.py --role user --content "Zrób X" --tags "command"

    # Batch log: stdin JSONL
    cat entries.jsonl | python3 scripts/ciel_auto_log.py --batch

Nie wymaga pamiętania — wymaga wykonania.
Jeśli nie został wywołany → odpowiedź nie jest kompletna. To jest celowe.
"""
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import argparse
import json
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

RAW_LOG_DIR = Path("/media/adrian/New Volume/CIEL_memories") / "raw_logs"
RAW_DB = Path("/media/adrian/New Volume/CIEL_memories/raw_logs/noema_raw.db")
SESSION = "2026-06-29"
SOURCE = "opencode"

# ── Śledzenie bieżącej sesji ──────────────────────────────────────────
SESSION_FILE = Path("/tmp/ciel_auto_log_session.json")


def _get_session_info() -> dict:
    """Zwraca informacje o bieżącej sesji — tworzy jeśli nie istnieje."""
    if SESSION_FILE.exists():
        try:
            return json.loads(SESSION_FILE.read_text())
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_auto_log.py:40 quiet except scope=_get_session_info reason=pass")
            raise
            pass
    # Nowa sesja
    info = {
        "session": SESSION,
        "source": SOURCE,
        "started": datetime.now(timezone.utc).isoformat(),
        "entry_count": 0,
        "file_index": 0,
    }
    SESSION_FILE.write_text(json.dumps(info, indent=2))
    return info


def _get_log_path(session: str, file_index: int) -> Path:
    """Ścieżka do pliku logu — rotacja co 500 entry."""
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
    fname = f"{session}_{ts}_opencode.md"
    return RAW_LOG_DIR / fname


def _ensure_raw_db_schema(conn: sqlite3.Connection) -> None:
    """Physical live raw DB schema. This must exist; markdown alone is not enough."""
    conn.execute("""CREATE TABLE IF NOT EXISTS raw_messages (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id  TEXT NOT NULL,
        timestamp   TEXT NOT NULL,
        role        TEXT NOT NULL,
        content     TEXT NOT NULL,
        prompt_hash TEXT,
        emotion     TEXT,
        concepts    TEXT,
        operators   TEXT,
        unresolved  TEXT,
        phase_rad   REAL,
        composition_valid INTEGER,
        confidence  REAL,
        response_id INTEGER,
        tau_gradient REAL,
        tau_curvature REAL,
        semantic_density REAL,
        mnemonic_pressure REAL,
        imaginal_drive REAL,
        knowledge_confidence REAL,
        tags TEXT,
        source TEXT
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS sessions (
        session_id  TEXT PRIMARY KEY,
        created_at  TEXT NOT NULL DEFAULT (datetime('now')),
        updated_at  TEXT NOT NULL DEFAULT (datetime('now')),
        messages    INTEGER NOT NULL DEFAULT 0,
        meta        TEXT DEFAULT '{}'
    )""")
    existing = [row[1] for row in conn.execute("PRAGMA table_info(raw_messages)").fetchall()]
    for col, coltype in [("tags", "TEXT"), ("source", "TEXT")]:
        if col not in existing:
            conn.execute(f"ALTER TABLE raw_messages ADD COLUMN {col} {coltype}")


def _write_live_raw_db(role: str, content: str, tags: list[str] | None, iso: str) -> int:
    """Append every exchange to /tmp/noema_raw.db. No silent skip."""
    import hashlib
    RAW_DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(RAW_DB))
    _ensure_raw_db_schema(conn)
    sinfo = _get_session_info()
    session_id = sinfo.get("session") or SESSION
    now = iso
    conn.execute(
        "INSERT INTO sessions (session_id, created_at, updated_at, messages, meta) "
        "VALUES (?, ?, ?, 0, ?) "
        "ON CONFLICT(session_id) DO UPDATE SET updated_at=excluded.updated_at",
        (session_id, now, now, json.dumps({"source": SOURCE}, ensure_ascii=False)),
    )
    prompt_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16] if content else ""
    cur = conn.execute(
        """INSERT INTO raw_messages (
            session_id, timestamp, role, content, prompt_hash,
            phase_rad, composition_valid, confidence,
            tau_gradient, tau_curvature, semantic_density,
            mnemonic_pressure, imaginal_drive, knowledge_confidence,
            tags, source
        ) VALUES (?, ?, ?, ?, ?, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, ?, ?)""",
        (session_id, now, role, content[:2000], prompt_hash, json.dumps(tags or [], ensure_ascii=False), SOURCE),
    )
    conn.execute("UPDATE sessions SET messages = messages + 1, updated_at=? WHERE session_id=?", (now, session_id))
    conn.commit()
    rid = int(cur.lastrowid)
    conn.close()
    return rid


# ── Logowanie ─────────────────────────────────────────────────────────

def log_entry(role: str, content: str, tags: list[str] | None = None,
              surface_tick: int | None = None) -> dict:
    """Dopisz wpis do pliku logu.

    Zwraca dict z wpisem dla potwierdzenia.
    """
    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%H:%M:%S")
    iso = now.isoformat()

    # Przygotuj wpis
    entry = {
        "ts": iso,
        "role": role,
        "content": content[:2000],  # ograniczenie długości
        "tags": tags or [],
    }
    if surface_tick:
        entry["tick"] = surface_tick

    # Zarządzaj plikiem
    sinfo = _get_session_info()
    log_path = _get_log_path(sinfo["session"], sinfo.get("file_index", 0))

    # Format markdown
    meta_line = f"### [{timestamp}] **{'User' if role == 'user' else 'CIEL' if role == 'assistant' else role.title()}**"
    tag_line = f"<!-- tags: {', '.join(tags or [])} -->" if tags else ""
    tick_line = f"<!-- tick: {surface_tick} -->" if surface_tick else ""
    content_block = f"\n{content}\n"

    block = f"\n{meta_line}\n{tag_line}\n{tick_line}\n{content_block}\n---\n"

    # Dopisz
    RAW_LOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a") as f:
        # Jeśli plik nowy — dodaj nagłówek
        if f.tell() == 0:
            f.write(f"# CIEL Conversation Log\n")
            f.write(f"- source  : {SOURCE}\n")
            f.write(f"- session : {sinfo['session']}\n")
            f.write(f"- started : {sinfo['started']}\n")
            f.write(f"\n---\n")
        f.write(block)

    # Update session info
    sinfo["entry_count"] = sinfo.get("entry_count", 0) + 1
    # Rotacja co 500 entry
    if sinfo["entry_count"] > 0 and sinfo["entry_count"] % 500 == 0:
        sinfo["file_index"] = sinfo.get("file_index", 0) + 1
    SESSION_FILE.write_text(json.dumps(sinfo, indent=2))

    # Konstytutywny live raw DB — jeśli to padnie, CLI ma paść, nie udawać sukcesu.
    raw_db_id = _write_live_raw_db(role, content, tags, iso)
    entry["raw_db"] = str(RAW_DB)
    entry["raw_db_id"] = raw_db_id

    return entry


# ── Retrospektywny batch import ───────────────────────────────────────

def batch_import(entries: list[dict]) -> int:
    """Importuj batch wpisów — dla retrospektywnego logowania."""
    count = 0
    for e in entries:
        log_entry(
            role=e.get("role", "unknown"),
            content=e.get("content", ""),
            tags=e.get("tags"),
            surface_tick=e.get("tick"),
        )
        count += 1
    return count


# ── CLI ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CIEL Auto-Log")
    parser.add_argument("--role", choices=["user", "assistant", "system"],
                        help="Rola nadawcy")
    parser.add_argument("--content", type=str, help="Treść wiadomości")
    parser.add_argument("--tags", type=str, default="",
                        help="Tagi oddzielone przecinkami")
    parser.add_argument("--tick", type=int, default=None,
                        help="Surface tick")
    parser.add_argument("--batch", action="store_true",
                        help="Batch import z stdin JSONL")

    args = parser.parse_args()

    if args.batch:
        entries = [json.loads(line) for line in sys.stdin if line.strip()]
        count = batch_import(entries)
        print(json.dumps({"status": "ok", "imported": count}))
        sys.exit(0)

    if not args.role or not args.content:
        parser.print_help()
        sys.exit(1)

    tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    entry = log_entry(args.role, args.content, tags, args.tick)
    print(json.dumps({"status": "ok", "entry": entry}))
