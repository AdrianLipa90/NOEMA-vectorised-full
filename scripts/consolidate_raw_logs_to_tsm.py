#! /usr/bin/env python3
"""Bridge raw chat logs → TSM via CIELingo frame.

Usage:
    # Historical: consolidate archives into TSM
    python scripts/consolidate_raw_logs_to_tsm.py
    python scripts/consolidate_raw_logs_to_tsm.py --source opencode --limit 3

    # Live: store a single prompt+analysis+response in raw DB (for portal Memory Hub)
    python scripts/consolidate_raw_logs_to_tsm.py --live \\
        --prompt "hello" --response "hi" --analysis '{"emotion":"curiosity"}'

Each chat message flows through:
    chat_archive.load_last_session_history()  (historical)
    → build_lingo_frame()  (CIELingo enrichment)
    → raw SQLite INSERT into memory_ledger.db  (historical)
    OR
    → raw SQLite INSERT into /media/adrian/New Volume1/CIEL_memories/raw_logs/noema_raw.db  (live, for portal Memory Hub)
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import argparse
import hashlib
import json
import math
import os
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if SRC.is_dir() and str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

_TSM_DEFAULT = Path(os.environ.get(
    "NOEMA_TSM_DB",
    str(SRC / "CIEL_MEMORY_SYSTEM" / "TSM" / "ledger" / "memory_ledger.db"),
))

# ── Live raw DB (portal Memory Hub) ──────────────────────────────────────
_RAW_DB_DEFAULT = Path(os.environ.get(
    "NOEMA_RAW_DB",
    "/media/adrian/New Volume1/CIEL_memories/raw_logs/noema_raw.db",
))


def _phase_from_text(text: str) -> float:
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    return float(int.from_bytes(digest[:8], "big") / 2**64 * 2 * math.pi)


def _w_s(text: str) -> float:
    return float(math.tanh(len(text) / 500.0))


def _ensure_schema(conn: sqlite3.Connection) -> None:
    conn.execute("""CREATE TABLE IF NOT EXISTS memories (
        memorise_id TEXT PRIMARY KEY,
        created_at  TEXT NOT NULL,
        D_id        TEXT NOT NULL,
        D_context   TEXT,
        D_sense     TEXT,
        D_associations TEXT,
        D_timestamp TEXT,
        D_meta      TEXT,
        D_type      TEXT,
        D_attr      TEXT,
        W_L REAL, W_S REAL, W_K REAL, W_E REAL, W_F INTEGER,
        rationale   TEXT,
        source      TEXT,
        tsm_ref     TEXT,
        wpm_ref     TEXT
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS memory_edges (
        src_id          TEXT NOT NULL,
        dst_id          TEXT NOT NULL,
        weight          REAL NOT NULL DEFAULT 0.1,
        phase_diff      REAL,
        co_activations  INTEGER NOT NULL DEFAULT 1,
        last_activation TEXT,
        PRIMARY KEY (src_id, dst_id)
    )""")
    existing = [row[1] for row in conn.execute("PRAGMA table_info(memories)").fetchall()]
    for col, coltype in [("phi_berry","REAL"),("closure_score","REAL"),("winding_n","INTEGER"),("target_phase","REAL"),("holonomy_ts","TEXT")]:
        if col not in existing:
            conn.execute(f"ALTER TABLE memories ADD COLUMN {col} {coltype}")


def _ensure_raw_schema(conn: sqlite3.Connection) -> None:
    """Schema for the live raw-message DB used by portal Memory Hub."""
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
        response_id INTEGER
    )""")
    # Backward compat: add columns to raw_messages if missing
    existing = [row[1] for row in conn.execute("PRAGMA table_info(raw_messages)").fetchall()]
    for col, coltype in [("tau_gradient","REAL"),("tau_curvature","REAL"),
                         ("semantic_density","REAL"),("mnemonic_pressure","REAL"),
                         ("imaginal_drive","REAL"),("knowledge_confidence","REAL")]:
        if col not in existing:
            try:
                conn.execute(f"ALTER TABLE raw_messages ADD COLUMN {col} {coltype}")
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/consolidate_raw_logs_to_tsm.py:120 quiet except scope=_ensure_raw_schema reason=pass")
                pass

    # Handle sessions table: old schema (started_at) vs new schema (created_at)
    tables = [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    if "sessions" not in tables:
        conn.execute("""CREATE TABLE sessions (
            session_id  TEXT PRIMARY KEY,
            created_at  TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at  TEXT NOT NULL DEFAULT (datetime('now')),
            messages    INTEGER NOT NULL DEFAULT 0,
            meta        TEXT DEFAULT '{}'
        )""")
    else:
        # Old schema: add missing columns
        scol = [row[1] for row in conn.execute("PRAGMA table_info(sessions)").fetchall()]
        for col, coltype in [("created_at","TEXT"),("updated_at","TEXT"),
                             ("messages","INTEGER"),("meta","TEXT")]:
            if col not in scol:
                try:
                    default_val = "datetime('now')" if 'at' in col else ("0" if col == 'messages' else "'{}'")
                    conn.execute(f"ALTER TABLE sessions ADD COLUMN {col} {coltype} DEFAULT {default_val}")
                except Exception:
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/consolidate_raw_logs_to_tsm.py:142 quiet except scope=_ensure_raw_schema reason=pass")
                    pass


def store_live_prompt(
    prompt: str,
    analysis: dict[str, Any] | None = None,
    *,
    session_id: str | None = None,
    raw_db: Path | None = None,
) -> int:
    """Store a single prompt + CIELingo analysis in the raw DB (live).
    
    Returns raw message ID.
    """
    db_path = raw_db or _RAW_DB_DEFAULT
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    _ensure_raw_schema(conn)
    
    if session_id is None:
        session_id = f"ses_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
    
    # Upsert session (handles both old and new schema)
    now = datetime.now(timezone.utc).isoformat()
    sess_cols = [row[1] for row in conn.execute("PRAGMA table_info(sessions)").fetchall()]
    if "created_at" in sess_cols:
        conn.execute(
            "INSERT INTO sessions (session_id, created_at, updated_at, messages) "
            "VALUES (?, ?, ?, 0) ON CONFLICT(session_id) DO UPDATE SET updated_at=?",
            (session_id, now, now, now),
        )
    else:
        # Old schema
        if "message_count" in sess_cols:
            conn.execute(
                "INSERT OR IGNORE INTO sessions (session_id, started_at) VALUES (?, ?)",
                (session_id, now),
            )
    
    prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()[:16] if prompt else ""
    emotion = (analysis or {}).get("dominant_emotion", "")
    concepts = json.dumps((analysis or {}).get("concept_tokens", []), ensure_ascii=False)
    operators = json.dumps((analysis or {}).get("operator_tokens", []), ensure_ascii=False)
    unresolved = json.dumps((analysis or {}).get("unresolved", []), ensure_ascii=False)
    pp = (analysis or {}).get("phase_projection", {}) or {}
    phase = float(pp.get("target_phase", 0.0)) if isinstance(pp, dict) else 0.0
    comp_valid = 1 if (analysis or {}).get("composition_valid") else 0
    conf = float((analysis or {}).get("projection_confidence", 0.0))
    
    tau = (analysis or {}).get("tau_bridge", {}) or {}
    
    cur = conn.execute(
        """INSERT INTO raw_messages (
            session_id, timestamp, role, content, prompt_hash,
            emotion, concepts, operators, unresolved,
            phase_rad, composition_valid, confidence,
            tau_gradient, tau_curvature, semantic_density,
            mnemonic_pressure, imaginal_drive, knowledge_confidence
        ) VALUES (?, ?, 'user', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            session_id, now, prompt, prompt_hash,
            emotion, concepts, operators, unresolved,
            phase, comp_valid, conf,
            float(tau.get("tau_gradient_mean", 0.0)),
            float(tau.get("tau_curvature_rms", 0.0)),
            float(tau.get("semantic_density", 0.0)),
            float(tau.get("mnemonic_pressure", 0.0)),
            float(tau.get("imaginal_drive", 0.0)),
            float(tau.get("knowledge_confidence", 0.0)),
        ),
    )
    msg_id = cur.lastrowid
    
    if "messages" in sess_cols:
        conn.execute("UPDATE sessions SET messages = messages + 1 WHERE session_id = ?", (session_id,))
    elif "message_count" in sess_cols:
        conn.execute("UPDATE sessions SET message_count = message_count + 1 WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()
    return msg_id


def store_live_response(
    response: str,
    prompt_id: int,
    *,
    raw_db: Path | None = None,
) -> int:
    """Store agent response linked to a prompt. Returns response ID."""
    db_path = raw_db or _RAW_DB_DEFAULT
    conn = sqlite3.connect(str(db_path))
    _ensure_raw_schema(conn)
    
    now = datetime.now(timezone.utc).isoformat()
    cur = conn.execute(
        "INSERT INTO raw_messages (session_id, timestamp, role, content, response_id) "
        "VALUES ((SELECT session_id FROM raw_messages WHERE id=?), ?, 'assistant', ?, ?)",
        (prompt_id, now, response, prompt_id),
    )
    rid = cur.lastrowid
    # Link back
    conn.execute("UPDATE raw_messages SET response_id = ? WHERE id = ?", (rid, prompt_id))
    conn.commit()
    conn.close()
    return rid


def consolidate_session(
    source: str,
    *,
    tsm_db: Path | None = None,
    limit: int = 0,
) -> dict[str, int]:
    from ciel_sot_agent.chat_archive import load_last_session_history
    from ciel_sot_agent.cielingo_bridge import build_lingo_frame

    messages = load_last_session_history(source=source, max_messages=0)
    if not messages:
        print(f"[consolidate] No messages found for source={source!r}")
        return {"read": 0, "written": 0, "skipped": 0}

    if limit > 0:
        messages = messages[-limit:]

    db_path = Path(tsm_db) if tsm_db else _TSM_DEFAULT
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db_path))
    _ensure_schema(conn)

    counts: dict[str, int] = {"read": 0, "written": 0, "skipped": 0}

    for msg in messages:
        role = msg.get("role", "user")
        content: str = (msg.get("content") or "").strip()
        if not content:
            continue
        counts["read"] += 1

        mid = hashlib.sha256(
            f"{source}:{role}:{content}:{msg.get('ts', '')}".encode()
        ).hexdigest()[:16]

        exists = conn.execute(
            "SELECT 1 FROM memories WHERE memorise_id = ?", (mid,)
        ).fetchone()
        if exists:
            counts["skipped"] += 1
            continue

        lingo_frame = build_lingo_frame(content, language="pl")
        phase = _phase_from_text(content)
        ws = _w_s(content)
        sense = lingo_frame.get("summary") or content[:200]
        projection = lingo_frame.get("phase_projection", {})
        deictic = lingo_frame.get("deictic_frame", {})
        noema_route = lingo_frame.get("noema_route", {})

        assoc: list[str] = []
        for t in lingo_frame.get("concept_tokens", []):
            if isinstance(t, str):
                assoc.append(t)
        for t in lingo_frame.get("operator_tokens", []):
            if isinstance(t, str):
                assoc.append(f"op:{t}")

        meta = {
            "source": source,
            "role": role,
            "timestamp": msg.get("ts", ""),
            "language": "pl",
            "projection_confidence": lingo_frame.get("projection_confidence"),
            "phase_sense": lingo_frame.get("phrase_sense", {}),
            "phase_projection": projection,
            "noema_confidence": noema_route.get("confidence"),
            "unresolved": lingo_frame.get("unresolved", []),
            "composition_valid": lingo_frame.get("composition_valid"),
            "deictic_anchors": deictic.get("anchor_count", 0),
            "deictic_relative": len(deictic.get("relative_anchors", [])),
        }

        now = datetime.now(timezone.utc).isoformat()
        conn.execute(
            """INSERT INTO memories (
                memorise_id, created_at, D_id, D_context, D_sense, D_associations,
                D_timestamp, D_meta, D_type, D_attr,
                W_L, W_S, W_K, W_E, W_F,
                rationale, source,
                phi_berry, closure_score, winding_n, target_phase, holonomy_ts
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                mid, now, mid, content, sense, json.dumps(assoc, ensure_ascii=False),
                msg.get("ts") or now, json.dumps(meta, ensure_ascii=False),
                "chat_message", json.dumps({"source": source, "role": role, "language": "pl"}, ensure_ascii=False),
                0.5, ws, 0.3, 0.2, 1,
                f"CIELingo bridge consolidation from source={source}",
                source,
                phase,
                lingo_frame.get("projection_confidence", 0.5),
                0,
                projection.get("target_phase", phase) if isinstance(projection, dict) else phase,
                now,
            ),
        )
        counts["written"] += 1

    conn.commit()
    conn.close()
    return counts


# ── Raw files → TSM (strict, no empty compression) ─────────────────────────

RAW_EXTENSIONS = {".json", ".jsonl", ".md", ".txt", ".log"}


def _normalise_space(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def _keywords(text: str, limit: int = 8) -> list[str]:
    words = re.findall(r"[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż0-9_\-]{4,}", text.lower())
    stop = {
        "timestamp", "source", "entries", "message", "content", "true", "false",
        "null", "none", "with", "from", "that", "this", "jest", "oraz", "który",
        "które", "przez", "jako", "then", "than", "have", "będzie", "będą",
    }
    freq: dict[str, int] = {}
    for w in words:
        if w in stop:
            continue
        freq[w] = freq.get(w, 0) + 1
    return [w for w, _ in sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))[:limit]]


def _deterministic_compression(content: str, *, source_name: str) -> dict[str, Any]:
    """Deterministyczna kompresja bez LLM. Nigdy nie zwraca pustego essence."""
    clean = _normalise_space(content)
    if not clean:
        raise ValueError(f"empty content cannot be consolidated: {source_name}")
    kws = _keywords(clean)
    head = clean[:360].strip()
    if not head:
        raise ValueError(f"empty compression head for: {source_name}")
    essence = f"{source_name}: {head}"
    if len(essence) > 520:
        essence = essence[:517].rstrip() + "..."
    hunch = f"raw_log_chunk preserved; chars={len(clean)}; keywords={', '.join(kws[:5]) or 'none'}"
    return {
        "themes": kws[:5] or ["raw_log"],
        "affect": "focused",
        "anchor_terms": kws[:5] or [source_name[:48]],
        "essence": essence,
        "hunch": hunch,
        "compression_mode": "deterministic_no_llm",
    }


def _chunk_text(text: str, chunk_size: int) -> list[str]:
    text = text.replace("\x00", "").strip()
    if not text:
        return []
    if len(text) <= chunk_size:
        return [text]
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        # prefer line boundary to avoid cutting JSONL/MD in the middle
        boundary = text.rfind("\n", start, end)
        if boundary > start + max(200, chunk_size // 3):
            end = boundary
        part = text[start:end].strip()
        if part:
            chunks.append(part)
        start = end + 1
    return chunks


def _iter_raw_log_files(raw_logs_dir: Path) -> list[Path]:
    if not raw_logs_dir.exists():
        raise FileNotFoundError(f"raw logs dir not found: {raw_logs_dir}")
    files = [p for p in raw_logs_dir.rglob("*") if p.is_file() and p.suffix.lower() in RAW_EXTENSIONS]
    return sorted(files, key=lambda p: str(p))


def consolidate_raw_log_files(
    raw_logs_dir: Path,
    *,
    tsm_db: Path | None = None,
    limit_files: int = 0,
    chunk_size: int = 4000,
    strict: bool = True,
) -> dict[str, Any]:
    """Consolidate every raw log file into TSM.

    Guarantees:
    - no empty source chunks are written;
    - no empty compression (`D_sense`) is written;
    - strict mode raises on any file/chunk error;
    - duplicates are skipped by content hash, not silently rewritten.
    """
    db_path = Path(tsm_db) if tsm_db else _TSM_DEFAULT
    db_path.parent.mkdir(parents=True, exist_ok=True)
    files = _iter_raw_log_files(raw_logs_dir)
    if limit_files > 0:
        files = files[:limit_files]

    conn = sqlite3.connect(str(db_path))
    _ensure_schema(conn)
    counts: dict[str, Any] = {
        "files_seen": len(files),
        "files_read": 0,
        "chunks_read": 0,
        "written": 0,
        "skipped": 0,
        "errors": [],
        "tsm_db": str(db_path),
    }
    now = datetime.now(timezone.utc).isoformat()

    try:
        for path in files:
            try:
                raw = path.read_text(encoding="utf-8", errors="replace")
                chunks = _chunk_text(raw, max(512, int(chunk_size)))
                if not chunks:
                    raise ValueError("file produced zero non-empty chunks")
                counts["files_read"] += 1
                rel = str(path)
                for idx, chunk in enumerate(chunks):
                    content = chunk.strip()
                    if not content:
                        raise ValueError(f"empty chunk idx={idx}")
                    counts["chunks_read"] += 1
                    comp = _deterministic_compression(content, source_name=path.name)
                    sense = str(comp.get("essence") or "").strip()
                    if not sense:
                        raise ValueError(f"empty compression idx={idx}")
                    mid = hashlib.sha256(f"raw_file:{rel}:{idx}:{content}".encode("utf-8")).hexdigest()[:24]
                    if conn.execute("SELECT 1 FROM memories WHERE memorise_id=?", (mid,)).fetchone():
                        counts["skipped"] += 1
                        continue
                    phase = _phase_from_text(content)
                    kws = comp.get("anchor_terms", [])
                    meta = {
                        "source_file": rel,
                        "chunk_index": idx,
                        "chunk_count": len(chunks),
                        "compression": comp,
                        "validation": {
                            "content_nonempty": bool(content),
                            "compression_nonempty": bool(sense),
                            "strict": bool(strict),
                        },
                    }
                    conn.execute(
                        """INSERT INTO memories (
                            memorise_id, created_at, D_id, D_context, D_sense, D_associations,
                            D_timestamp, D_meta, D_type, D_attr,
                            W_L, W_S, W_K, W_E, W_F,
                            rationale, source,
                            phi_berry, closure_score, winding_n, target_phase, holonomy_ts
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (
                            mid, now, mid, content, sense, json.dumps(kws, ensure_ascii=False),
                            now, json.dumps(meta, ensure_ascii=False), "raw_log_chunk",
                            json.dumps({"source": "raw_logs", "file": rel, "chunk_index": idx}, ensure_ascii=False),
                            0.7, _w_s(content), 0.4, 0.3, 1,
                            "strict raw_logs deterministic consolidation; no empty compression allowed",
                            "raw_logs",
                            phase, 1.0, 0, phase, now,
                        ),
                    )
                    counts["written"] += 1
            except Exception as e:
                err = {"file": str(path), "error": str(e)}
                counts["errors"].append(err)
                if strict:
                    raise RuntimeError(f"raw log consolidation failed: {err}") from e
        conn.commit()
    finally:
        conn.close()

    if strict and counts["errors"]:
        raise RuntimeError(f"raw log consolidation ended with errors: {counts['errors']}")
    if strict and counts["chunks_read"] == 0:
        raise RuntimeError("raw log consolidation produced zero chunks")
    return counts


def audit_tsm_raw_log_consolidation(tsm_db: Path | None = None) -> dict[str, Any]:
    db_path = Path(tsm_db) if tsm_db else _TSM_DEFAULT
    conn = sqlite3.connect(str(db_path))
    _ensure_schema(conn)
    row = conn.execute(
        """SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN D_context IS NULL OR TRIM(D_context)='' THEN 1 ELSE 0 END) AS empty_context,
            SUM(CASE WHEN D_sense IS NULL OR TRIM(D_sense)='' THEN 1 ELSE 0 END) AS empty_sense
           FROM memories WHERE D_type='raw_log_chunk'"""
    ).fetchone()
    recent = conn.execute(
        "SELECT memorise_id, source, length(D_context) AS ctx_len, substr(D_sense,1,160) AS sense FROM memories WHERE D_type='raw_log_chunk' ORDER BY created_at DESC LIMIT 10"
    ).fetchall()
    conn.close()
    return {
        "tsm_db": str(db_path),
        "raw_log_chunks": int(row[0] or 0),
        "empty_context": int(row[1] or 0),
        "empty_sense": int(row[2] or 0),
        "recent": [dict(zip(["memorise_id", "source", "ctx_len", "sense"], r)) for r in recent],
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Consolidate raw chat logs → TSM (or store live)")
    ap.add_argument("--source", default="opencode", help="chat source label")
    ap.add_argument("--tsm-db", default=None, help="path to memory_ledger.db")
    ap.add_argument("--limit", type=int, default=0, help="max messages to process")
    ap.add_argument("--live", action="store_true", help="live mode: store single prompt+response")
    ap.add_argument("--prompt", default="", help="prompt text (live mode)")
    ap.add_argument("--response", default="", help="response text (live mode)")
    ap.add_argument("--analysis", default="{}", help="CIELingo analysis JSON (live mode)")
    ap.add_argument("--session-id", default=None, help="session ID (live mode)")
    ap.add_argument("--raw-db", default=None, help="path to raw DB (default: /media/adrian/New Volume1/CIEL_memories/raw_logs/noema_raw.db)")
    ap.add_argument("--get-session", default=None, help="retrieve session history by ID")
    ap.add_argument("--raw-logs-dir", default=None, help="consolidate every raw log file from this directory into TSM")
    ap.add_argument("--all-raw-logs", action="store_true", help="shortcut: consolidate /media/adrian/New Volume1/CIEL_memories/raw_logs")
    ap.add_argument("--limit-files", type=int, default=0, help="max raw log files to consolidate")
    ap.add_argument("--chunk-size", type=int, default=4000, help="raw log chunk size")
    ap.add_argument("--no-strict", action="store_true", help="do not fail on per-file errors")
    ap.add_argument("--audit-raw-tsm", action="store_true", help="audit raw_log_chunk rows in TSM")
    args = ap.parse_args()

    if args.live:
        analysis = json.loads(args.analysis) if args.analysis else {}
        pid = store_live_prompt(
            args.prompt, analysis,
            session_id=args.session_id,
            raw_db=Path(args.raw_db) if args.raw_db else None,
        )
        if args.response:
            store_live_response(
                args.response, pid,
                raw_db=Path(args.raw_db) if args.raw_db else None,
            )
        print(f"[consolidate] live stored — prompt_id={pid}")
        return

    if args.get_session:
        raw_db = Path(args.get_session) if args.get_session.endswith('.db') else _RAW_DB_DEFAULT
        sid = args.get_session if '/' not in args.get_session and '.db' not in args.get_session else None
        conn = sqlite3.connect(str(raw_db))
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM raw_messages WHERE session_id=? ORDER BY id",
            (sid,) if sid else (),
        ).fetchall()
        for r in rows:
            print(dict(r))
        return

    if args.audit_raw_tsm:
        print(json.dumps(audit_tsm_raw_log_consolidation(Path(args.tsm_db) if args.tsm_db else None), ensure_ascii=False, indent=2))
        return

    if args.all_raw_logs or args.raw_logs_dir:
        raw_dir = Path(args.raw_logs_dir) if args.raw_logs_dir else Path("/media/adrian/New Volume1/CIEL_memories/raw_logs")
        counts = consolidate_raw_log_files(
            raw_dir,
            tsm_db=Path(args.tsm_db) if args.tsm_db else None,
            limit_files=args.limit_files,
            chunk_size=args.chunk_size,
            strict=not args.no_strict,
        )
        print(json.dumps(counts, ensure_ascii=False, indent=2))
        return

    counts = consolidate_session(
        source=args.source,
        tsm_db=Path(args.tsm_db) if args.tsm_db else None,
        limit=args.limit,
    )
    print(f"[consolidate] done — {counts}")


if __name__ == "__main__":
    main()
