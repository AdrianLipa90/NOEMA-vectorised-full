#!/usr/bin/env python3

"""CIEL Agent Daemon — podpina agenta (mnie) pod CIEL jako rozpoznawalny byt.

Architektura:
  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
  │  AGENT       │ ──→ │  agent_hint  │ ──→ │  CIEL Surface │
  │  (opencode)  │ ←── │  (mmap/json) │ ←── │  /dev/shm    │
  └──────────────┘     └──────────────┘     └──────────────┘
         │                     │                     │
         │              FIFO/socket            daemon_registry
         │              IPC dla agenta         heartbeat co 30s
         └──────────────────────────────────────────────────┘

Rejestruje agenta jako CIEL-own daemon z claims na agent_hint, task_inbox.
Czyta surface, zapisuje agent_hint z timestampem i stanem.
Może być uruchomiony jako systemd user service.

Usage:
  Daemon:   python3 scripts/ciel_agent_daemon.py
  Status:   kill -USR1 $(cat /tmp/ciel_agent.pid)
  Stop:     kill -TERM $(cat /tmp/ciel_agent.pid)
  FIFO:     echo '{"type":"ping"}' > /tmp/ciel_agent.fifo

Autor: Adrian Lipa & NOEMA (2026)
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
import logging
import os
import pathlib
import signal
import socket
import struct
import sys
import threading
import time
import uuid
from typing import Any

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
_SRC = str(ROOT / "src")
for _p in (_SRC, str(ROOT / "integration")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

logging.basicConfig(
    level=logging.INFO,
    format="[ciel-agent] %(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ── Ścieżki ─────────────────────────────────────────────────────────────
PID_PATH = pathlib.Path("/tmp/ciel_agent.pid")
FIFO_PATH = pathlib.Path("/tmp/ciel_agent.fifo")
SOCKET_PATH = pathlib.Path("/tmp/ciel_agent.sock")
SURFACE_ROOT = pathlib.Path("/dev/shm/ciel_noema")
HEARTBEAT_INTERVAL = 30.0  # sekund między registry heartbeat
SURFACE_POLL_INTERVAL = 5.0  # sekund między odczytem surface
FAST_PULSE_HZ = 7.8  # Schumann-coupled pulse: ~128ms (7.83 Hz fundamental)
FAST_PULSE_INTERVAL = 1.0 / FAST_PULSE_HZ  # ~0.128 s

# ── Stan globalny ───────────────────────────────────────────────────────
_running = True
_token: str | None = None
_registry: Any = None
_surface: dict[str, Any] | None = None

# ── Lazy import ─────────────────────────────────────────────────────────
def _lazy_registry():
    global _registry
    if _registry is None:
        from ciel_geometry.noema_registry import registry
        _registry = registry

def _lazy_surface():
    global _surface
    if _surface is None:
        try:
            from ciel_geometry.noema_surface_mmap import ensure_surface
            _surface = ensure_surface(zero_fill=False)
        except Exception as e:
            log.warning("surface init: %s", e)

# ── Sygnały ─────────────────────────────────────────────────────────────
def _signal_handler(signum: int, _frame) -> None:
    global _running
    if signum == signal.SIGTERM:
        log.info("SIGTERM — shutting down")
        _running = False
    elif signum == signal.SIGUSR1:
        _print_status()

def _print_status() -> None:
    """Wypisz stan agent daemona na stderr."""
    now = time.strftime("%H:%M:%S")
    pid = os.getpid()
    token = _token or "unregistered"
    print(f"[ciel-agent] STATUS@{now} pid={pid} token={token}", file=sys.stderr, flush=True)
    try:
        if SURFACE_ROOT.exists():
            files = [p.name for p in SURFACE_ROOT.iterdir() if p.is_file()]
            print(f"[ciel-agent] surface files ({len(files)}): {', '.join(sorted(files)[:15])}", file=sys.stderr, flush=True)
        hint_path = SURFACE_ROOT / "agent_hint"
        if hint_path.exists():
            hint = json.loads(hint_path.read_text())
            print(f"[ciel-agent] agent_hint: {json.dumps(hint, indent=2)[:300]}", file=sys.stderr, flush=True)
    except Exception as e:
        print(f"[ciel-agent] status error: {e}", file=sys.stderr, flush=True)

# ── Rejestracja ─────────────────────────────────────────────────────────
def _register() -> str:
    """Rejestruj agenta w CIEL daemon registry. Zwraca token."""
    global _registry
    _lazy_registry()
    token = _registry.register("agent", surface_claims=["agent_hint", "task_inbox", "tick"])
    log.info("registered token=%s", token)
    return token

def _heartbeat(token: str) -> None:
    """Cykl heartbeat."""
    _lazy_registry()
    try:
        _registry.heartbeat(token)
    except Exception as e:
        log.warning("heartbeat failed: %s", e)

def _unregister(token: str) -> None:
    """Wyrejestruj agenta."""
    _lazy_registry()
    try:
        _registry.unregister(token)
    except Exception as e:
        log.warning("unregister failed: %s", e)

# ── Surface I/O ─────────────────────────────────────────────────────────
def _read_live_state() -> dict[str, Any]:
    """Czyta live state z CIEL surface."""
    state: dict[str, Any] = {"ts": time.time()}
    try:
        # agent_hint
        hint_path = SURFACE_ROOT / "agent_hint"
        if hint_path.exists():
            state["agent_hint"] = json.loads(hint_path.read_text())
        # tick
        tick_path = SURFACE_ROOT / "tick"
        if tick_path.exists() and tick_path.stat().st_size >= 8:
            state["tick"] = int(np.memmap(tick_path, dtype=np.uint64, mode="r", shape=(1,))[0])
        # phi coherence
        phi_path = SURFACE_ROOT / "phi"
        if phi_path.exists() and phi_path.stat().st_size >= 36 * 8:
            phi = np.memmap(phi_path, dtype=np.float64, mode="r", shape=(36,))
            state["R"] = float(abs(np.mean(np.exp(1j * phi))))
        # health
        health_path = SURFACE_ROOT / "health"
        if health_path.exists():
            raw = health_path.read_bytes()
            if len(raw) >= 8:
                state["health"] = struct.unpack("d", raw[:8])[0]
        # flavor
        flavor_path = SURFACE_ROOT / "flavor"
        if flavor_path.exists() and flavor_path.stat().st_size >= 6 * 8:
            flavor = np.memmap(flavor_path, dtype=np.float64, mode="r", shape=(6,))
            state["flavor"] = flavor.tolist()
        # daemon registry status
        reg_dir = SURFACE_ROOT / "registry"
        if reg_dir.exists():
            active = 0
            now = time.time()
            for p in reg_dir.glob("*.json"):
                try:
                    d = json.loads(p.read_text())
                    if now - d.get("heartbeat_at", 0) <= 60:
                        active += 1
                except Exception:
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_agent_daemon.py:185 quiet except scope=_read_live_state reason=pass")
                    pass
            state["active_daemons"] = active
    except Exception as e:
        log.warning("surface read: %s", e)
    return state

def _write_agent_hint(state: dict[str, Any]) -> None:
    """Zapisuje agent_hint na surface — deleguje do fast pulse."""
    _write_fast_pulse(state)

# ── Fast pulse ─────────────────────────────────────────────────────────
_pulse_counter = 0
_phi_accum = 0.0  # accumulated phase for Schumann-style sine wave

def _write_fast_pulse(state: dict[str, Any]) -> float:
    """Zapisuje szybki pulse (7.8 Hz) do agent_heartbeat na surface.
    
    Wartość to sub-cyclic pattern: 4-stopniowa rampa sin (0, π/2, π, 3π/2)
    rozłożona na 4 pulse'y = 4*128ms = 0.5s cykl → 2 Hz widoczny beat.
    Kuramoto daemon/trigger mogą czytać ten plik jako żywy sygnał agenta.
    """
    global _pulse_counter, _phi_accum
    _pulse_counter += 1
    # Sub-cycle: 4 kroki = 1 pełny okres sin
    # Każdy krok to π/2 rad
    _phi_accum = (_phi_accum + np.pi / 2.0) % (2.0 * np.pi)
    pulse_value = float(np.sin(_phi_accum) * 0.5 + 0.5)  # sin → [0, 1]

    pulse_path = SURFACE_ROOT / "agent_heartbeat"
    try:
        import struct
        pulse_path.write_bytes(struct.pack("d", pulse_value))
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_agent_daemon.py:218 quiet except scope=_write_fast_pulse reason=pass")
        pass

    # Co 10 pulses (≈1.3s) update agent_hint timestamp
    if _pulse_counter % 10 == 0:
        try:
            hint_path = SURFACE_ROOT / "agent_hint"
            payload: dict[str, Any] = {
                "agent_tick": state.get("tick", 0),
                "agent_R": state.get("R", 0.0),
                "agent_time": time.time(),
                "agent_pid": os.getpid(),
                "agent_token": _token or "unregistered",
                "agent_state": "alive",
                "agent_note": f"pulse@{FAST_PULSE_HZ}Hz",
                "agent_heartbeat": round(pulse_value, 4),
            }
            hint_path.write_text(json.dumps(payload, indent=2))
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_agent_daemon.py:236 quiet except scope=_write_fast_pulse reason=pass")
            pass

    return pulse_value

def _is_task_pending() -> bool:
    """Sprawdza task_queue przez portal API albo bezpośrednio."""
    try:
        import urllib.request
        with urllib.request.urlopen("http://127.0.0.1:18888/api/live", timeout=3) as r:
            data = json.loads(r.read().decode())
        coh = data.get("coherence", 0)
        return coh < 0.4
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_agent_daemon.py:249 quiet except scope=_is_task_pending reason=return False")
        return False

# ── FIFO ────────────────────────────────────────────────────────────────
def _fifo_worker():
    """Nasłuchuje na FIFO — agent moze wysłać komendę z zewnątrz."""
    global _running
    try:
        if FIFO_PATH.exists():
            FIFO_PATH.unlink()
        os.mkfifo(str(FIFO_PATH))
        log.info("FIFO at %s", FIFO_PATH)
        while _running:
            try:
                with open(FIFO_PATH, "r") as f:
                    line = f.readline().strip()
                if line:
                    log.info("FIFO received: %.120s", line)
                    try:
                        cmd = json.loads(line)
                        _handle_fifo_cmd(cmd)
                    except json.JSONDecodeError:
                        log.warning("FIFO not JSON: %s", line)
            except Exception as e:
                if _running:
                    log.warning("FIFO read: %s", e)
                    time.sleep(1)
    except Exception as e:
        log.warning("FIFO worker: %s", e)

def _handle_fifo_cmd(cmd: dict[str, Any]) -> None:
    """Obsługuje komendy z FIFO."""
    cmd_type = cmd.get("type", "")
    if cmd_type == "ping":
        log.info("pong — agent daemon alive")
    elif cmd_type == "status":
        _print_status()
    elif cmd_type == "sync":
        state = _read_live_state()
        _write_agent_hint(state)
        log.info("sync done: R=%.3f tick=%s", state.get("R", 0), state.get("tick", "?"))
    elif cmd_type == "inject":
        text = cmd.get("text", "")
        if text:
            log.info("inject-to-surface: %.80s", text)
            _inject_text(text)
    else:
        log.info("unknown fifo cmd: %s", cmd_type)

def _inject_text(text: str) -> None:
    """Zapisuje tekst do task_inbox.jsonl — CIEL i trigger daemon czytają to."""
    inbox_path = SURFACE_ROOT / "task_inbox.jsonl"
    entry = {"ts": time.time(), "source": "ciel_agent_daemon", "text": text}
    try:
        with open(inbox_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
        log.info("injected to task_inbox.jsonl")
    except Exception as e:
        log.warning("task_inbox write: %s", e)

# ── Socket IPC ──────────────────────────────────────────────────────────
def _socket_worker():
    """Unix socket dla zapytań JSON-in/JSON-out."""
    global _running
    try:
        if SOCKET_PATH.exists():
            SOCKET_PATH.unlink()
        srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        srv.bind(str(SOCKET_PATH))
        srv.listen(5)
        srv.settimeout(1.0)
        log.info("socket at %s", SOCKET_PATH)
        while _running:
            try:
                conn, addr = srv.accept()
                with conn:
                    data = conn.recv(65536)
                    if data:
                        _handle_socket_request(conn, data)
            except socket.timeout:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_agent_daemon.py:328 quiet except scope=_socket_worker reason=continue")
                continue
            except Exception as e:
                log.warning("socket accept: %s", e)
        srv.close()
    except Exception as e:
        log.warning("socket worker: %s", e)
    finally:
        try:
            SOCKET_PATH.unlink()
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_agent_daemon.py:338 quiet except scope=_socket_worker reason=pass")
            pass

def _handle_socket_request(conn: socket.socket, data: bytes) -> None:
    """Obsługuje żądanie JSON przez socket."""
    try:
        req = json.loads(data.decode("utf-8"))
        cmd_type = req.get("type", "")
        if cmd_type == "ping":
            resp = {"status": "ok", "pid": os.getpid(), "token": _token}
        elif cmd_type == "status":
            state = _read_live_state()
            resp = {"status": "ok", "state": state}
        elif cmd_type == "sync":
            state = _read_live_state()
            _write_agent_hint(state)
            resp = {"status": "ok", "R": state.get("R", 0), "tick": state.get("tick", 0)}
        else:
            resp = {"status": "error", "msg": f"unknown type: {cmd_type}"}
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_agent_daemon.py:357 quiet except scope=_handle_socket_request reason=assign_fallback")
        resp = {"status": "error", "msg": str(e)}
    try:
        conn.sendall(json.dumps(resp).encode("utf-8"))
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_agent_daemon.py:361 quiet except scope=_handle_socket_request reason=pass")
        pass

# ── Główna pętla ────────────────────────────────────────────────────────
def main_loop() -> int:
    global _token, _running, _surface

    signal.signal(signal.SIGTERM, _signal_handler)
    signal.signal(signal.SIGUSR1, _signal_handler)

    # PID
    PID_PATH.write_text(str(os.getpid()))
    log.info("pid=%d", os.getpid())

    # FIFO
    fifo_thread = threading.Thread(target=_fifo_worker, daemon=True)
    fifo_thread.start()

    # Socket
    socket_thread = threading.Thread(target=_socket_worker, daemon=True)
    socket_thread.start()

    # Rejestracja
    try:
        _token = _register()
    except Exception as e:
        log.error("registration failed: %s", e)
        return 1

    # Inicjalna sync
    _lazy_surface()
    state = _read_live_state()
    _write_agent_hint(state)
    log.info("initial sync: R=%.3f tick=%s daemons=%s",
             state.get("R", 0), state.get("tick", "?"), state.get("active_daemons", "?"))

    # Główna pętla — 7.8 Hz fast pulse
    heartbeat_ts = 0.0
    poll_ts = 0.0
    last_state: dict[str, Any] = {}
    while _running:
        now = time.monotonic()

        # Registry heartbeat (co 30s)
        if now - heartbeat_ts >= HEARTBEAT_INTERVAL:
            _heartbeat(_token)
            heartbeat_ts = now

        # Poll surface (co 5s)
        if now - poll_ts >= SURFACE_POLL_INTERVAL:
            try:
                last_state = _read_live_state()
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_agent_daemon.py:413 quiet except scope=main_loop reason=pass")
                pass
            poll_ts = now

        # Fast pulse 7.8 Hz — zawsze
        try:
            pulse = _write_fast_pulse(last_state)
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_agent_daemon.py:420 quiet except scope=main_loop reason=assign_fallback")
            pulse = 0.0

        # Co ~1s log
        if int(now) != int(now - FAST_PULSE_INTERVAL):
            pass  # cicho — log tylko w DEBUG

        time.sleep(FAST_PULSE_INTERVAL)

    # Cleanup
    _unregister(_token)
    _write_agent_hint({"agent_state": "stopped", "agent_time": time.time()})
    try:
        PID_PATH.unlink(missing_ok=True)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_agent_daemon.py:434 quiet except scope=main_loop reason=pass")
        pass
    log.info("stopped")
    return 0

if __name__ == "__main__":
    raise SystemExit(main_loop())
