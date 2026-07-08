#!/usr/bin/env python3
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

# CIEL ORBITAL BINDING — daemon bound
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on daemon " + __name__)

"""
ciel_auto_log_daemon.py — FIFO-based auto-log daemon.

Nasłuchuje na /dev/shm/ciel_noema/auto_log.fifo
Każda linia = JSON: {"role":"...","content":"...","tags":"...","timestamp":"..."}
Zapisuje do:
  - /tmp/ciel_session_log.jsonl   (szybki append)
  - ~/CIEL_memories/raw_logs/     (struktura YYYY/MM/WW/)
  - memories_index.db              (jeśli dostępny)

Uruchom: python3 scripts/ciel_auto_log_daemon.py [--daemon]

(c) 2026 CIEL Apokalyptos — opencode-native, zero zależności poza stdlib
"""

import json
import os
import sys
import time
import signal
import logging
import sqlite3
import pathlib
from datetime import datetime, timezone

# --- Paths ---
FIFO_PATH = pathlib.Path("/dev/shm/ciel_noema/auto_log.fifo")
SESSION_LOG = pathlib.Path("/tmp/ciel_session_log.jsonl")
MEMORIES_ROOT = pathlib.Path("/media/adrian/New Volume1/CIEL_memories/raw_logs")
MEMORIES_DB = pathlib.Path("/media/adrian/New Volume1/CIEL_memories/memories_index.db")
REGISTRY_PATH = pathlib.Path("/dev/shm/ciel_noema/daemon_logs")

# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="[auto-log] %(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("auto-log")

# --- Globals ---
_running = True
_db_conn = None


# === Registry helpers ===

def _registry_path(name: str) -> pathlib.Path:
    """Return path to a daemon's registry file under REGISTRY_PATH."""
    try:
        REGISTRY_PATH.mkdir(parents=True, exist_ok=True)
    except FileExistsError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_auto_log_daemon.py:59 quiet except scope=_registry_path reason=If")
        # Path exists but may be a file — remove and recreate
        if REGISTRY_PATH.exists() and not REGISTRY_PATH.is_dir():
            REGISTRY_PATH.unlink()
            REGISTRY_PATH.mkdir(parents=True, exist_ok=True)
    return REGISTRY_PATH / f"{name}.json"


def _registry_write(name: str, data: dict) -> None:
    """Write daemon registration JSON."""
    import uuid
    rp = _registry_path(name)
    data.setdefault("pid", os.getpid())
    data.setdefault("name", name)
    data.setdefault("token", str(uuid.uuid4()))
    data.setdefault("claims", [])
    data.setdefault("created_at", datetime.now(timezone.utc).isoformat())
    rp.write_text(json.dumps(data, indent=2))
    log.info(f"registered name={name} pid={data['pid']}")


def _registry_unlink(name: str) -> None:
    rp = _registry_path(name)
    if rp.exists():
        rp.unlink()
        log.info(f"unregistered {name}")


# === DB helpers ===

def _db_init() -> sqlite3.Connection | None:
    """Open memories_index.db, create tables if needed."""
    if not MEMORIES_DB.exists():
        log.info(f"no memories_index.db at {MEMORIES_DB}, skipping db log")
        return None
    try:
        conn = sqlite3.connect(str(MEMORIES_DB), timeout=5)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                role TEXT,
                content TEXT,
                tags TEXT,
                source TEXT DEFAULT 'auto_log'
            )
        """)
        conn.commit()
        return conn
    except Exception as e:
        log.warning(f"db init failed: {e}")
        return None


def _db_insert(conn: sqlite3.Connection | None, row: dict) -> None:
    if conn is None:
        return
    try:
        conn.execute(
            "INSERT INTO logs (timestamp, role, content, tags) VALUES (?, ?, ?, ?)",
            (row.get("timestamp", datetime.now(timezone.utc).isoformat()),
             row.get("role", "unknown"),
             row.get("content", ""),
             row.get("tags", ""))
        )
        conn.commit()
    except Exception as e:
        log.warning(f"db insert failed: {e}")


# === Raw log ===

def _raw_log_path(ts: str) -> pathlib.Path:
    """YYYY/MM/WW/YYYY-MM-DD.md"""
    dt = datetime.fromisoformat(ts)
    yyyy = str(dt.year)
    mm = f"{dt.month:02d}"
    # ISO week number
    ww = f"W{dt.isocalendar()[1]:02d}"
    day = dt.strftime("%Y-%m-%d")
    base = MEMORIES_ROOT / yyyy / mm / ww
    base.mkdir(parents=True, exist_ok=True)
    return base / f"{day}.md"


def _append_raw_log(row: dict) -> None:
    """Append one exchange to the day's markdown file."""
    ts = row.get("timestamp", datetime.now(timezone.utc).isoformat())
    role = row.get("role", "?")
    content = row.get("content", "")
    tags = row.get("tags", "")

    dt = datetime.fromisoformat(ts)
    local = dt.strftime("%H:%M:%S")
    header = f"\n### {local} | {role}"
    if tags:
        header += f" [{tags}]"

    rp = _raw_log_path(ts)
    with open(rp, "a", encoding="utf-8") as f:
        f.write(header + "\n")
        # content — indent for readability
        for line in content.strip().split("\n"):
            f.write(f"> {line}\n")
        f.write("\n")


# === FIFO listener ===

def _ensure_fifo() -> None:
    FIFO_PATH.parent.mkdir(parents=True, exist_ok=True)
    if FIFO_PATH.exists():
        if not FIFO_PATH.is_fifo():
            FIFO_PATH.unlink()
    if not FIFO_PATH.exists():
        os.mkfifo(str(FIFO_PATH))
        log.info(f"created FIFO at {FIFO_PATH}")


def _process_line(line: str) -> None:
    """Parse JSON line and log it."""
    line = line.strip()
    if not line:
        return
    try:
        row = json.loads(line)
    except json.JSONDecodeError:
        log.warning(f"bad json: {line[:120]}")
        return

    role = row.get("role", "?")
    content_preview = row.get("content", "")[:80].replace("\n", " ")
    log.info(f"  ← {role}: {content_preview}...")

    # session log (fast append)
    with open(SESSION_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

    # raw_logs/
    _append_raw_log(row)

    # db
    _db_insert(_db_conn, row)


def _fifo_loop() -> None:
    """Open FIFO and read lines forever."""
    _ensure_fifo()
    log.info(f"listening on {FIFO_PATH}")
    while _running:
        try:
            # Open FIFO (blocking open, then line-by-line)
            with open(FIFO_PATH, "r", encoding="utf-8", errors="replace") as fifo:
                for line in fifo:
                    if not _running:
                        break
                    _process_line(line)
        except FileNotFoundError:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_auto_log_daemon.py:217 quiet except scope=_fifo_loop reason=no_log_no_raise")
            # FIFO removed? recreate
            _ensure_fifo()
            time.sleep(0.5)
        except OSError as e:
            log.warning(f"fifo read error: {e}")
            time.sleep(1.0)
        except Exception as e:
            log.error(f"fifo loop error: {e}")
            time.sleep(2.0)


# === Signal ===

def _stop(signum, _frame):
    global _running
    log.info(f"signal {signum}, stopping")
    _running = False


# === Main ===

def main():
    global _running, _db_conn

    # Parse args
    import argparse
    parser = argparse.ArgumentParser(description="CIEL auto-log FIFO daemon")
    parser.add_argument("--daemon", action="store_true", help="Run in background (fork)")
    args = parser.parse_args()

    if args.daemon:
        if os.fork() == 0:
            # child
            os.setsid()
            # close stdin/stdout
            sys.stdin.close()
        else:
            # parent exits
            return

    # Signals
    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)

    # Init
    _db_conn = _db_init()
    _registry_write("auto-log", {"pid": os.getpid(), "claims": ["memory_log"]})
    log.info("auto-log daemon started")

    try:
        _fifo_loop()
    finally:
        if _db_conn:
            _db_conn.close()
        _registry_unlink("auto-log")
        log.info("stopped")


if __name__ == "__main__":
    main()
