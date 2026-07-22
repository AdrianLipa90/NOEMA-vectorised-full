#!/usr/bin/env python3
"""CIEL Monitor Daemon — keeps CIEL engine alive, exposes state via Unix socket.

Mosty: lingophysics, orbital, euler, TSM, raw_logs — wszystko w jednym procesie.

Usage:
    python3 scripts/ciel_monitor.py              # one-shot state dump
    python3 scripts/ciel_monitor.py --daemon     # background daemon
    python3 scripts/ciel_monitor.py --status     # query daemon state via socket
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import argparse
import json
import os
import select
import signal
import socket
import sys
import threading
import time
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_SRC = str(_PROJECT_ROOT / "src")
_CIEL_OMEGA = str(_PROJECT_ROOT / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM" / "ciel_omega")
for _p in (_SRC, _CIEL_OMEGA):
    if _p not in sys.path:
        sys.path.insert(0, _p)

SOCKET_PATH = Path.home() / ".ciel" / "monitor.sock"
from ciel_geometry.paths import P

STATE_PATH = Path(P.MEMORY) / "state" / "ciel_last_metrics.json"
RAW_LOG_DIR = Path(P.MEMORY) / "raw_logs"
TSM_DB = _PROJECT_ROOT / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM" / "CIEL_MEMORY_SYSTEM" / "TSM" / "ledger" / "memory_ledger.db"

from ciel_sot_agent.cielingo_bridge import build_lingo_frame
from ciel_sot_agent.ciel_pipeline import run_ciel_pipeline, resolve_project_root
from ciel_sot_agent.state_db import get_or_create_identity_seed, load_metrics_history

# Singleton (cached) CIEL engine — avoids 52s re-init per call
_ENGINE: Any = None
_ENGINE_ROOT: Path | None = None


def _get_cached_engine(root: Path | None = None) -> Any:
    global _ENGINE, _ENGINE_ROOT
    if _ENGINE is not None and root is None:
        return _ENGINE
    if root is None:
        root = resolve_project_root(Path(__file__))
    if _ENGINE is not None and root == _ENGINE_ROOT:
        return _ENGINE
    from ciel.engine import CielEngine
    _ENGINE = CielEngine()
    _ENGINE_ROOT = root
    return _ENGINE

# ── Daemon state ──────────────────────────────────────────────────────────────

_LOCK = threading.Lock()
_STATE: dict[str, Any] = {
    "dominant_emotion": "curiosity",
    "ethical_score": 0.5,
    "soul_invariant": 0.5,
    "closure_penalty": 0.15,
    "operating_mode": "standard",
    "phi_berry_mean": 0.0,
    "cycle_index": 0,
    "system_health": 0.5,
    "coherence_index": 0.5,
    "mood": 0.0,
    "identity_seed": "",
    "pipeline_count": 0,
    "last_input": "",
    "last_response": "",
    "tsm_count": 0,
    "raw_log_count": 0,
    "uptime": 0.0,
    "daemon_pid": os.getpid(),
}
_STARTED: float = 0.0


def _init_engine() -> None:
    """Pre-warm CIEL engine (slow init, ~52s on first call)."""
    root = resolve_project_root(Path(__file__))
    _get_cached_engine(root)
    _STATE["identity_seed"] = get_or_create_identity_seed().get("seed", "")


def _process_text(text: str) -> dict[str, Any]:
    """Run text through CIELingo + CielEngine directly (cached engine)."""
    lingo = build_lingo_frame(text)
    summary = lingo.get("summary", "")
    engine = _get_cached_engine()
    raw = engine.step(summary, context=f"monitor|{text[:80]}")

    identity = get_or_create_identity_seed()
    cp = float(raw.get("closure_penalty", lingo.get("closure_penalty", 0.15)))
    with _LOCK:
        _STATE["dominant_emotion"] = raw.get("dominant_emotion", lingo.get("dominant_emotion", "curiosity"))
        _STATE["ethical_score"] = float(raw.get("ethical_score", identity.get("ethical_baseline", 0.5)))
        _STATE["soul_invariant"] = float(raw.get("soul_invariant", identity.get("soul_baseline", 0.5)))
        _STATE["closure_penalty"] = cp
        _STATE["phi_berry_mean"] = float(raw.get("phi_berry_mean", 0.0))
        _STATE["cycle_index"] = int(raw.get("cycle_index", _STATE["cycle_index"])) + 1
        _STATE["system_health"] = float(raw.get("system_health", 0.5))
        _STATE["coherence_index"] = float(raw.get("coherence_index", 0.5))
        _STATE["mood"] = float(raw.get("mood", 0.0))
        _STATE["operating_mode"] = "deep" if cp < 0.15 else "standard" if cp <= 0.35 else "safe"
        _STATE["pipeline_count"] += 1
        _STATE["last_input"] = text[:200]
        _STATE["tsm_count"] = _count_tsm()
        _STATE["raw_log_count"] = _count_raw_logs()
    return dict(_STATE)


_run_pipeline = _process_text  # backward compat


def _count_tsm() -> int:
    try:
        import sqlite3
        if TSM_DB.exists():
            conn = sqlite3.connect(str(TSM_DB))
            c = conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
            conn.close()
            return int(c)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_monitor.py:131 quiet except scope=_count_tsm reason=pass")
        raise
        pass
    return 0


def _count_raw_logs() -> int:
    if not RAW_LOG_DIR.exists():
        return 0
    return sum(1 for _ in RAW_LOG_DIR.rglob("*.md"))


# ── Unix socket server ────────────────────────────────────────────────────────

_ENGINE_READY = threading.Event()


def _handle_client(conn: socket.socket) -> None:
    """Handle one client request: return current state as JSON."""
    try:
        data = conn.recv(4096).decode("utf-8", errors="replace").strip()
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_monitor.py:151 quiet except scope=_handle_client reason=assign_fallback")
        raise
        data = ""
    with _LOCK:
        resp = json.dumps(dict(_STATE), ensure_ascii=False)
    if data and _ENGINE_READY.is_set():
        try:
            resp = json.dumps(_process_text(data), ensure_ascii=False)
        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_monitor.py:158 quiet except scope=_handle_client reason=assign_fallback")
            raise
            resp = json.dumps({"error": str(e), **dict(_STATE)}, ensure_ascii=False)
    try:
        conn.sendall(resp.encode("utf-8"))
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_monitor.py:162 quiet except scope=_handle_client reason=pass")
        raise
        pass
    finally:
        conn.close()


def _init_bg(root: Path) -> None:
    """Background engine init (slow, ~52s)."""
    _get_cached_engine(root)
    _STATE["identity_seed"] = get_or_create_identity_seed().get("seed", "")
    _ENGINE_READY.set()
    sys.stderr.write(f"CIEL Monitor engine ready ({_ENGINE_READY} — processing enabled)\n")
    sys.stderr.flush()


def _daemon_loop() -> None:
    """Unix socket daemon — accepts connections immediately, inits engine in bg."""
    global _STARTED
    _STARTED = time.time()
    SOCKET_PATH.parent.mkdir(parents=True, exist_ok=True)
    if SOCKET_PATH.exists():
        SOCKET_PATH.unlink()

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(str(SOCKET_PATH))
    server.listen(5)
    server.settimeout(1.0)

    root = resolve_project_root(Path(__file__))
    _STATE["identity_seed"] = get_or_create_identity_seed().get("seed", "")
    threading.Thread(target=_init_bg, args=(root,), daemon=True).start()

    sys.stderr.write(f"CIEL Monitor daemon ready (pid={os.getpid()}, socket={SOCKET_PATH})\n")
    sys.stderr.write("Engine init in background — queries return default state until ready\n")
    sys.stderr.flush()

    while True:
        try:
            conn, _ = server.accept()
            _handle_client(conn)
        except socket.timeout:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_monitor.py:202 quiet except scope=_daemon_loop reason=pass")
            raise
            pass
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_monitor.py:204 quiet except scope=_daemon_loop reason=break")
            raise
            break

    server.close()
    if SOCKET_PATH.exists():
        SOCKET_PATH.unlink()


# ── CLI ───────────────────────────────────────────────────────────────────────

def _query_daemon(text: str = "") -> dict[str, Any]:
    """Query running daemon via Unix socket."""
    if not SOCKET_PATH.exists():
        return {"error": "daemon not running", "socket": str(SOCKET_PATH)}
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(5)
    sock.connect(str(SOCKET_PATH))
    sock.sendall(text.encode("utf-8"))
    sock.shutdown(socket.SHUT_WR)
    data = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
    sock.close()
    return json.loads(data.decode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="CIEL Monitor Daemon")
    parser.add_argument("--daemon", action="store_true", help="Run as background daemon")
    parser.add_argument("--status", action="store_true", help="Query daemon state")
    parser.add_argument("--text", type=str, default="", help="Text to process (pipeline)")
    args = parser.parse_args()

    if args.daemon:
        _daemon_loop()
        return 0
    if args.status:
        state = _query_daemon(args.text)
        print(json.dumps(state, ensure_ascii=False, indent=2))
        return 0

    # One-shot
    _init_engine()
    state = _process_text(args.text or "init")
    print(json.dumps(state, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    main()
