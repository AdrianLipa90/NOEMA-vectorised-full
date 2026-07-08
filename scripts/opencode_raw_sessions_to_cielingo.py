#!/usr/bin/env python3
"""Ingest OpenCode raw-session logs into CIELingo live raw memory."""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import argparse
import hashlib
import json
import os
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

NOEMA_ROOT = Path(os.environ.get("NOEMA_ROOT", Path(__file__).resolve().parent.parent))
SRC = NOEMA_ROOT / "src"
SCRIPTS = NOEMA_ROOT / "scripts"
RAW_SESSIONS_DIR = NOEMA_ROOT / ".opencode" / "raw-sessions"
STATE_PATH = NOEMA_ROOT / "state" / "opencode_raw_ingest_state.json"
REPORT_PATH = NOEMA_ROOT / "state" / "opencode_raw_ingest_report.json"
DEFAULT_RAW_DB = Path(os.environ.get("NOEMA_RAW_DB", "/media/adrian/New Volume1/CIEL_memories/raw_logs/noema_raw.db"))
FALLBACK_RAW_DB = NOEMA_ROOT / "state" / "noema_raw.db"

for path in (SRC, SCRIPTS):
    text = str(path)
    if path.exists() and text not in sys.path:
        sys.path.insert(0, text)

from ciel_sot_agent.cielingo_bridge import build_lingo_frame  # noqa: E402
from consolidate_raw_logs_to_tsm import _ensure_raw_schema  # noqa: E402


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/opencode_raw_sessions_to_cielingo.py:40 quiet except scope=_load_json reason=return default")
        return default


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _iter_session_dirs(limit_sessions: int) -> list[Path]:
    if not RAW_SESSIONS_DIR.exists():
        return []
    sessions = [path for path in RAW_SESSIONS_DIR.iterdir() if path.is_dir()]
    sessions.sort(key=lambda path: path.stat().st_mtime, reverse=True)
    return sessions[: max(0, limit_sessions)]


def _read_chat_records(session_dir: Path) -> list[dict[str, Any]]:
    path = session_dir / "chat.jsonl"
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    with path.open(encoding="utf-8", errors="replace") as handle:
        for line_no, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
            except Exception as exc:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/opencode_raw_sessions_to_cielingo.py:69 quiet except scope=_read_chat_records reason=no_log_no_raise")
                records.append({"_parse_error": repr(exc), "_line_no": line_no})
                continue
            if isinstance(item, dict):
                item["_line_no"] = line_no
                records.append(item)
    return records


def _message_roles(records: list[dict[str, Any]]) -> dict[str, str]:
    roles: dict[str, str] = {}
    for record in records:
        message = record.get("message")
        if isinstance(message, dict):
            mid = str(message.get("id") or "")
            role = str(message.get("role") or "")
            if mid and role:
                roles[mid] = role
        for part in record.get("parts") or []:
            if isinstance(part, dict):
                mid = str(part.get("messageID") or "")
                if mid and record.get("message", {}).get("role"):
                    roles[mid] = str(record["message"]["role"])
    return roles


def _text_parts(record: dict[str, Any], roles: dict[str, str]) -> list[dict[str, str]]:
    parts: list[dict[str, Any]] = []
    if record.get("kind") == "chat.message":
        parts = [part for part in (record.get("parts") or []) if isinstance(part, dict)]
    elif record.get("kind") == "message.part.updated" and isinstance(record.get("part"), dict):
        parts = [record["part"]]

    out: list[dict[str, str]] = []
    for part in parts:
        if part.get("type") != "text":
            continue
        text = str(part.get("text") or "").strip()
        if not text:
            continue
        mid = str(part.get("messageID") or "")
        role = roles.get(mid) or str(record.get("message", {}).get("role") or "user")
        out.append(
            {
                "message_id": mid,
                "part_id": str(part.get("id") or ""),
                "role": role if role in {"user", "assistant"} else "user",
                "text": text,
            }
        )
    return out


def _ensure_ingest_columns(conn: sqlite3.Connection) -> None:
    _ensure_raw_schema(conn)
    existing = [row[1] for row in conn.execute("PRAGMA table_info(raw_messages)").fetchall()]
    for column, column_type in (("tags", "TEXT"), ("source", "TEXT")):
        if column not in existing:
            conn.execute(f"ALTER TABLE raw_messages ADD COLUMN {column} {column_type}")


def _store_message(
    *,
    conn: sqlite3.Connection,
    session_id: str,
    role: str,
    content: str,
    analysis: dict[str, Any],
    source: str,
    tags: list[str],
) -> int:
    _ensure_ingest_columns(conn)
    now = _utc()
    prompt_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]
    existing = conn.execute(
        "SELECT id FROM raw_messages WHERE session_id=? AND role=? AND prompt_hash=? AND source=? LIMIT 1",
        (session_id, role, prompt_hash, source),
    ).fetchone()
    if existing:
        return 0
    conn.execute(
        "INSERT INTO sessions (session_id, created_at, updated_at, messages, meta) "
        "VALUES (?, ?, ?, 0, ?) "
        "ON CONFLICT(session_id) DO UPDATE SET updated_at=excluded.updated_at",
        (session_id, now, now, json.dumps({"source": source}, ensure_ascii=False)),
    )
    phase = analysis.get("phase_projection", {}) if isinstance(analysis.get("phase_projection"), dict) else {}
    tau = analysis.get("tau_bridge", {}) if isinstance(analysis.get("tau_bridge"), dict) else {}
    cur = conn.execute(
        """INSERT INTO raw_messages (
            session_id, timestamp, role, content, prompt_hash,
            emotion, concepts, operators, unresolved,
            phase_rad, composition_valid, confidence,
            tau_gradient, tau_curvature, semantic_density,
            mnemonic_pressure, imaginal_drive, knowledge_confidence,
            tags, source
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            session_id,
            now,
            role,
            content,
            prompt_hash,
            analysis.get("dominant_emotion", ""),
            json.dumps(analysis.get("concept_tokens", []), ensure_ascii=False),
            json.dumps(analysis.get("operator_tokens", []), ensure_ascii=False),
            json.dumps(analysis.get("unresolved", []), ensure_ascii=False),
            float(phase.get("target_phase", 0.0)),
            1 if analysis.get("composition_valid") else 0,
            float(analysis.get("projection_confidence", 0.0)),
            float(tau.get("tau_gradient_mean", 0.0)),
            float(tau.get("tau_curvature_rms", 0.0)),
            float(tau.get("semantic_density", 0.0)),
            float(tau.get("mnemonic_pressure", 0.0)),
            float(tau.get("imaginal_drive", 0.0)),
            float(tau.get("knowledge_confidence", 0.0)),
            json.dumps(tags, ensure_ascii=False),
            source,
        ),
    )
    conn.execute("UPDATE sessions SET messages = messages + 1, updated_at = ? WHERE session_id = ?", (now, session_id))
    return int(cur.lastrowid)


def ingest_once(
    *,
    limit_sessions: int = 12,
    max_messages: int = 200,
    raw_db: Path = DEFAULT_RAW_DB,
    source: str = "opencode_raw_session",
    _allow_fallback: bool = True,
) -> dict[str, Any]:
    state = _load_json(STATE_PATH, {})
    seen = set(state.get("seen_keys", []))
    inserted: list[dict[str, Any]] = []
    errors: list[str] = []
    scanned_records = 0
    skipped_seen = 0
    skipped_db = 0

    try:
        conn = sqlite3.connect(str(raw_db))
    except Exception as exc:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/opencode_raw_sessions_to_cielingo.py:211 quiet except scope=ingest_once reason=no_log_no_raise")
        report = {
            "ok": False,
            "timestamp": _utc(),
            "raw_db": str(raw_db),
            "errors": [f"raw_db_open:{exc!r}"],
            "inserted": 0,
            "scanned_sessions": 0,
            "scanned_records": 0,
            "skipped_seen": 0,
        }
        _write_json(REPORT_PATH, report)
        return report

    try:
        for session_dir in _iter_session_dirs(limit_sessions):
            records = _read_chat_records(session_dir)
            roles = _message_roles(records)
            for record in records:
                scanned_records += 1
                for item in _text_parts(record, roles):
                    key_src = "|".join(
                        [
                            session_dir.name,
                            item["message_id"],
                            item["role"],
                            hashlib.sha256(item["text"].encode("utf-8")).hexdigest(),
                        ]
                    )
                    key = hashlib.sha256(key_src.encode("utf-8")).hexdigest()
                    if key in seen:
                        skipped_seen += 1
                        continue
                    try:
                        frame = build_lingo_frame(item["text"], language="pl")
                        msg_id = _store_message(
                            conn=conn,
                            session_id=f"opencode:{session_dir.name}",
                            role=item["role"],
                            content=item["text"][:12000],
                            analysis=frame,
                            source=source,
                            tags=["opencode", "raw-session", session_dir.name],
                        )
                        seen.add(key)
                        if msg_id > 0:
                            inserted.append(
                                {
                                    "raw_message_id": msg_id,
                                    "session": session_dir.name,
                                    "role": item["role"],
                                    "message_id": item["message_id"],
                                    "part_id": item["part_id"],
                                }
                            )
                        else:
                            skipped_db += 1
                        if len(inserted) >= max_messages:
                            raise StopIteration
                    except StopIteration:
                        raise
                    except Exception as exc:
                        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/opencode_raw_sessions_to_cielingo.py:272 quiet except scope=ingest_once reason=Expr")
                        errors.append(f"{session_dir.name}:{record.get('_line_no')}:{exc!r}")
    except StopIteration:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/opencode_raw_sessions_to_cielingo.py:274 quiet except scope=ingest_once reason=pass")
        pass
    finally:
        conn.commit()
        conn.close()

    readonly_errors = [err for err in errors if "readonly database" in err or "Read-only file system" in err]
    if readonly_errors and raw_db != FALLBACK_RAW_DB and _allow_fallback:
        fallback_report = ingest_once(
            limit_sessions=limit_sessions,
            max_messages=max_messages,
            raw_db=FALLBACK_RAW_DB,
            source=source,
            _allow_fallback=False,
        )
        fallback_report["canonical_raw_db"] = str(raw_db)
        fallback_report["canonical_failed"] = True
        fallback_report["canonical_errors"] = readonly_errors[:5]
        fallback_report["storage_mode"] = "fallback_state_db"
        _write_json(REPORT_PATH, fallback_report)
        return fallback_report

    state = {
        "updated_at": _utc(),
        "seen_keys": sorted(seen)[-100000:],
    }
    _write_json(STATE_PATH, state)
    report = {
        "ok": not errors,
        "timestamp": _utc(),
        "raw_sessions_dir": str(RAW_SESSIONS_DIR),
        "raw_db": str(raw_db),
        "source": source,
        "storage_mode": "canonical_raw_db" if raw_db == DEFAULT_RAW_DB else "fallback_state_db",
        "canonical_failed": False,
        "scanned_sessions": len(_iter_session_dirs(limit_sessions)),
        "scanned_records": scanned_records,
        "inserted": len(inserted),
        "inserted_items": inserted[-20:],
        "skipped_seen": skipped_seen,
        "skipped_db": skipped_db,
        "errors": errors[:20],
        "elapsed_unix_ts": time.time(),
    }
    _write_json(REPORT_PATH, report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Feed OpenCode raw sessions into CIELingo raw memory")
    parser.add_argument("--limit-sessions", type=int, default=12)
    parser.add_argument("--max-messages", type=int, default=200)
    parser.add_argument("--raw-db", type=Path, default=DEFAULT_RAW_DB)
    args = parser.parse_args()
    report = ingest_once(limit_sessions=args.limit_sessions, max_messages=args.max_messages, raw_db=args.raw_db)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
