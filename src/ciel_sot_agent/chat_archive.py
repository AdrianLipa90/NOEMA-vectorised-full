"""CIEL Chat Archive — append-only conversation log in Markdown.

All runtime locations are resolved through the canonical NOEMA path registry.
No host-specific mount is assumed. Each session creates one append-only file and
is indexed in the configured memories database.
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import sqlite3
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path

from ciel_geometry.paths import P

_MEMORIES_BASE = Path(P.MEMORY)
_RAW_LOGS = Path(P.LOGS.RAW_LOGS_DIR)
_DB_PATH = Path(P.DB.MEMORIES_INDEX)

_lock = threading.Lock()
_default_session_id: str = str(uuid.uuid4())[:8]
_session_file: dict[tuple[str, str], Path] = {}


def _init_db() -> None:
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(str(_DB_PATH)) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                path TEXT NOT NULL,
                source TEXT,
                model TEXT,
                started_at TEXT,
                message_count INTEGER DEFAULT 0
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                role TEXT,
                content TEXT,
                ts TEXT,
                source TEXT,
                model TEXT
            )
        """)
        conn.commit()


def _db_register_session(session_id: str, path: Path, source: str) -> None:
    try:
        _init_db()
        with sqlite3.connect(str(_DB_PATH)) as conn:
            conn.execute(
                "INSERT OR IGNORE INTO sessions (id, path, source, started_at) VALUES (?,?,?,?)",
                (session_id, str(path), source, datetime.now(timezone.utc).isoformat())
            )
            conn.commit()
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("chat_archive session registration failed")


def _db_append_message(session_id: str, role: str, content: str, source: str, model: str) -> None:
    try:
        _init_db()
        ts = datetime.now(timezone.utc).isoformat()
        with sqlite3.connect(str(_DB_PATH)) as conn:
            conn.execute(
                "INSERT INTO messages (session_id, role, content, ts, source, model) VALUES (?,?,?,?,?,?)",
                (session_id, role, content, ts, source, model)
            )
            conn.execute(
                "UPDATE sessions SET message_count = message_count + 1, model = ? WHERE id = ?",
                (model, session_id)
            )
            conn.commit()
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("chat_archive message index append failed")


def _normalize_session_id(session_id: str | None) -> str:
    sid = (session_id or _default_session_id).strip() or _default_session_id
    return sid[:32]


def _source_root(source: str) -> Path:
    src = (source or "").strip().lower()
    if src in {"codex", "codex_tui", "codex-cli", "codex_cli"}:
        return _RAW_LOGS / "codex"
    if src == "claude_code":
        return _RAW_LOGS / "claude_code"
    return _RAW_LOGS


def _session_path(source: str, session_id: str | None) -> Path:
    now = datetime.now(timezone.utc)
    week = f"W{now.strftime('%V')}"
    folder = _source_root(source) / now.strftime("%Y") / now.strftime("%m") / week
    folder.mkdir(parents=True, exist_ok=True)
    sid = _normalize_session_id(session_id)
    fname = f"{now.strftime('%Y-%m-%d_%H-%M')}_{sid}_{source}.md"
    return folder / fname


def _get_session_file(source: str, session_id: str | None) -> Path:
    sid = _normalize_session_id(session_id)
    key = (source, sid)
    if key not in _session_file:
        path = _session_path(source, sid)
        with _lock:
            if key not in _session_file:
                path.write_text(
                    f"# CIEL Conversation Log\n"
                    f"- source  : {source}\n"
                    f"- session : {sid}\n"
                    f"- started : {datetime.now(timezone.utc).isoformat()}\n\n---\n\n",
                    encoding="utf-8",
                )
                _session_file[key] = path
                _db_register_session(sid, path, source)
    return _session_file[key]


def open_session(source: str = "gui_gguf", session_id: str | None = None) -> Path:
    return _get_session_file(source, session_id=session_id)


def append(
    role: str,
    content: str,
    source: str = "gui_gguf",
    model: str = "unknown",
    session_id: str | None = None,
    extra: dict | None = None,
) -> None:
    try:
        ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
        role_label = "**User**" if role == "user" else f"**{model}** (assistant)"
        extra_str = ""
        if extra:
            extra_str = "\n" + "\n".join(f"_{k}: {v}_" for k, v in extra.items())
        block = f"### [{ts}] {role_label}\n\n{content}{extra_str}\n\n---\n\n"
        path = _get_session_file(source, session_id=session_id)
        with _lock:
            with open(path, "a", encoding="utf-8") as file:
                file.write(block)
        _db_append_message(_normalize_session_id(session_id), role, content, source, model)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("chat_archive append failed")


def append_exchange(
    user_msg: str,
    assistant_reply: str,
    source: str = "gui_gguf",
    model: str = "unknown",
    session_id: str | None = None,
) -> None:
    append("user", user_msg, source=source, model=model, session_id=session_id)
    append("assistant", assistant_reply, source=source, model=model, session_id=session_id)


def load_recent(n: int = 30, source: str | None = None) -> list[dict]:
    if not _RAW_LOGS.exists():
        return []
    files = sorted(_RAW_LOGS.rglob("*.md"), key=lambda path: path.stat().st_mtime, reverse=True)
    result = []
    for file in files:
        if source and source not in file.name:
            continue
        result.append({
            "path": str(file),
            "name": file.name,
            "rel": str(file.relative_to(_MEMORIES_BASE)),
            "size_kb": round(file.stat().st_size / 1024, 1),
        })
        if len(result) >= n:
            break
    return result


def load_last_session_history(source: str = "gui_gguf", max_messages: int = 40) -> list[dict]:
    if not _RAW_LOGS.exists():
        return []
    files = sorted(
        (file for file in _RAW_LOGS.rglob("*.md") if source in file.name),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    current = {path for (src, _sid), path in _session_file.items() if src == source}
    for file in files:
        if file in current:
            continue
        try:
            text = file.read_text(encoding="utf-8")
        except OSError:
            continue
        history: list[dict] = []
        blocks = text.split("\n---\n")
        for block in blocks:
            if "### [" not in block:
                continue
            lines = block.strip().splitlines()
            if not lines:
                continue
            header = lines[0]
            content = "\n".join(lines[1:]).strip()
            if not content:
                continue
            role = "user" if "**User**" in header else "assistant"
            history.append({"role": role, "content": content})
        if history:
            return history[-max_messages:]
    return []


__all__ = [
    "append",
    "append_exchange",
    "load_last_session_history",
    "load_recent",
    "open_session",
]
