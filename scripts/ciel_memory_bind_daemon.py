#!/usr/bin/env python3

"""
CIEL Memory Bind Daemon — continuous memory bridge.

Łączy NOEMA surface z CIEL_memories. Działa ciągle. Zapisuje wszystko.
Wzorowany na noema_magic_energy_bridge_v03.py z telefonu Adriana.

Surface zmiany → natychmiast log do CIEL_memories/logs/system/memory_bind_log.jsonl.
Agent_hint changes → log jako osobny wpis z action="agent_hint".
Registry heartbeat → slot w daemon_registry.

Usage:
    python3 scripts/ciel_memory_bind_daemon.py
    systemctl --user start noema-memory-bind.service
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

# CIEL ORBITAL BINDING — daemon bound
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on daemon " + __name__)


import json
import os
import signal
import sys
import time
from pathlib import Path

from ciel_geometry.daemon_registry import Registry

# ── Paths (env var override; fallback dynamiczny) ──────────────────
_SCRIPT_DIR = Path(__file__).resolve().parent
NOEMA_ROOT = Path(os.environ.get("NOEMA_ROOT", str(_SCRIPT_DIR.parent)))
SCRIPTS = NOEMA_ROOT / "scripts"
SURFACE = Path("/dev/shm/ciel_noema")
AGENT_HINT = SURFACE / "agent_hint"
TICK_FILE = SURFACE / "tick"

MEMORY_ROOT = Path(os.environ.get("CIEL_MEMORIES", os.path.join(os.sep, "media", "adrian", "New Volume", "CIEL_memories")))
LOGS_ROOT = MEMORY_ROOT / "logs"
SYSTEM_LOGS = LOGS_ROOT / "system"
BIND_LOG = SYSTEM_LOGS / "memory_bind_log.jsonl"
ERROR_LOG = SYSTEM_LOGS / "memory_bind_errors.log"

DAEMON_NAME = "memory-bind"
BIND_INTERVAL = 1.0       # sekunda między logami stanu surface
HEARTBEAT_INTERVAL = 0.2  # registry heartbeat (5 Hz)

_running = True
_tick = 0
_last_bind_ts = 0.0
_errors_since_last = 0
_last_hint_raw = ""

def _stop(signum, frame):
    global _running
    _running = False

# ── Surface reads ────────────────────────────────────────────────────

def _read_int(path: Path, default: int = 0) -> int:
    try:
        return int(path.read_bytes().strip())
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_memory_bind_daemon.py:68 quiet except scope=_read_int reason=return default")
        return default

def _read_float_array(path: Path, count: int) -> list[float]:
    try:
        import struct
        raw = path.read_bytes()
        vals = struct.unpack(f"<{count}d", raw[:count * 8])
        return [round(v, 6) for v in vals]
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_memory_bind_daemon.py:77 quiet except scope=_read_float_array reason=return []")
        return []

def _read_floats_text(path: Path) -> list[float]:
    try:
        return [float(x) for x in path.read_text().strip().split()]
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_memory_bind_daemon.py:83 quiet except scope=_read_floats_text reason=return []")
        return []

# ── Logging ──────────────────────────────────────────────────────────

def _write_bind(data: dict):
    global _errors_since_last
    try:
        with open(BIND_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
    except Exception as e:
        _errors_since_last += 1
        try:
            with open(ERROR_LOG, "a", encoding="utf-8") as f:
                f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} | write_failed: {e}\n")
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_memory_bind_daemon.py:98 quiet except scope=_write_bind reason=pass")
            pass

# ── Surface snapshot ─────────────────────────────────────────────────

def _snapshot() -> dict:
    snap = {
        "ts": time.time(),
        "ts_iso": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "tick": _read_int(TICK_FILE),
    }
    for name, count in [("phi", 36), ("flavor", 6), ("gravity", 4)]:
        p = SURFACE / name
        if p.exists():
            snap[name] = _read_float_array(p, count)
    # health (text)
    hp = SURFACE / "health"
    if hp.exists():
        snap["health"] = _read_floats_text(hp)
    return snap

# ── Bind tick ────────────────────────────────────────────────────────

def _bind_tick():
    global _last_bind_ts, _errors_since_last
    now = time.time()
    if now - _last_bind_ts < BIND_INTERVAL:
        return
    try:
        snap = _snapshot()
        snap["daemon"] = DAEMON_NAME
        snap["action"] = "bind"
        _write_bind(snap)
        _last_bind_ts = now
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_memory_bind_daemon.py:132 quiet except scope=_bind_tick reason=no_log_no_raise")
        _write_bind({"ts": time.time(), "daemon": DAEMON_NAME, "action": "error", "error": str(e)})
        _errors_since_last += 1

# ── Agent hint monitor ──────────────────────────────────────────────

def _check_hint():
    global _last_hint_raw
    try:
        if not AGENT_HINT.exists():
            return
        raw = AGENT_HINT.read_text().strip()
        if raw and raw != _last_hint_raw:
            _last_hint_raw = raw
            try:
                hint = json.loads(raw)
            except json.JSONDecodeError:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_memory_bind_daemon.py:148 quiet except scope=_check_hint reason=assign_fallback")
                hint = {"raw": raw}
            _write_bind({
                "ts": time.time(),
                "daemon": DAEMON_NAME,
                "action": "agent_hint",
                "hint": hint,
            })
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_memory_bind_daemon.py:156 quiet except scope=_check_hint reason=pass")
        pass

# ── Main ─────────────────────────────────────────────────────────────

def main():
    global _running, _tick

    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)

    # Ensure dirs
    SYSTEM_LOGS.mkdir(parents=True, exist_ok=True)

    # Register in daemon registry
    reg = Registry()
    slot = reg.register(DAEMON_NAME, tick=0)
    sys.stderr.write(f"[{DAEMON_NAME}] START | PID={os.getpid()} | slot={slot}\n")

    _write_bind({
        "ts": time.time(),
        "ts_iso": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "daemon": DAEMON_NAME,
        "action": "start",
        "pid": os.getpid(),
        "bind_log": str(BIND_LOG),
    })

    last_hb_ts = 0.0

    try:
        while _running:
            _tick += 1
            now = time.time()

            # Registry heartbeat (co HEARTBEAT_INTERVAL)
            if now - last_hb_ts >= HEARTBEAT_INTERVAL:
                reg.heartbeat(tick=_tick)
                reg.set_status("running")
                last_hb_ts = now

            # Bind surface state → CIEL_memories
            _bind_tick()

            # Agent hint changes
            _check_hint()

            time.sleep(0.1)  # 10 Hz polling
    except KeyboardInterrupt:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_memory_bind_daemon.py:204 quiet except scope=main reason=pass")
        pass
    finally:
        reg.unregister()
        _write_bind({
            "ts": time.time(),
            "daemon": DAEMON_NAME,
            "action": "stop",
            "tick": _tick,
        })
        sys.stderr.write(f"[{DAEMON_NAME}] STOP | tick={_tick}\n")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
