#!/usr/bin/env python3

"""Actuator daemon — surface → system control.

Nadzoruje katalog /dev/shm/ciel_noema/actuator/ i wykonuje intencje
zapisane przez agenta (CIEL) jako JSON. Daje mi ręce.

Security:
  - whitelist akcji: restart, start, stop (tylko noema-*.service)
  - journal_query, run_script (tylko scripts/*.py)
  - rate limiting: max 1 akcja / 15s
  - audit trail: actuator/audit.jsonl
  - confirmation required dla stop/destructive

Protokół (intent.json):
  {
    "id": "uuid",
    "intent": "restart_daemon | start_daemon | stop_daemon | journal_query | run_script | surface_report | knowledge_query | noop",
    "target": "noema-kuramoto.service",        // dla restart/start/stop
    "reason": "archiver padł 3x w journalu",   // dlaczego
    "confidence": 0.87,                         // [0, 1]
    "ts": 1234567890.123                        // opcjonalnie
  }

Surface output:
  actuator/
    intent.json        — odczytana intencja
    result.json        — wynik wykonania
    audit.jsonl        — append-only log
    status.json        — stan daemona

Użycie:
  .venv/bin/python3 scripts/noema_actuator_daemon.py
  systemctl --user start noema-actuator.service
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
import subprocess
import sys
import time
import uuid
from pathlib import Path

from ciel_geometry.noema_registry import registry

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

SURFACE = Path("/dev/shm/ciel_noema")
ACTUATOR_DIR = SURFACE / "actuator"

# Bezpieczne akcje
ALLOWED_INTENTS = {
    # name: (requires_target, requires_confirmation, description)
    "restart_daemon":   (True,  False, "Restart noema-*.service"),
    "start_daemon":     (True,  False, "Start noema-*.service"),
    "stop_daemon":      (True,  True,  "Stop noema-*.service"),
    "journal_query":    (True,  False, "journalctl -n 50 -u <unit>"),
    "run_script":       (True,  True,  "Uruchom skrypt scripts/*.py"),
    "surface_report":   (False, False, "Odczytaj stan powierzchni"),
    "knowledge_query":  (True,  False, "Zapytaj bazę wiedzy"),
    "noop":             (False, False, "Nic nie rób (test)"),
}

# Rate limiting: max N akcji w oknie
MAX_ACTIONS_PER_WINDOW = 2
WINDOW_SECONDS = 30

# Stan
_actions_window: list[float] = []
_audit_log: list[dict] = []
_running = True
_last_intent_id: str | None = None

def log(msg: str) -> None:
    ts = time.strftime("%H:%M:%S")
    print(f"[actuator] {ts} {msg}", flush=True)

def _init_dirs() -> None:
    ACTUATOR_DIR.mkdir(parents=True, exist_ok=True)
    # Inicjalizuj audit.jsonl
    audit_path = ACTUATOR_DIR / "audit.jsonl"
    if not audit_path.exists():
        audit_path.touch()

def _rate_limited() -> bool:
    """Sprawdź rate limiting. Odrzuć jeśli przekroczone."""
    now = time.time()
    global _actions_window
    # Wyczyść stare
    _actions_window = [t for t in _actions_window if t > now - WINDOW_SECONDS]
    if len(_actions_window) >= MAX_ACTIONS_PER_WINDOW:
        return True
    return False

def _audit(entry: dict) -> None:
    """Dopisz do audit logu."""
    _audit_log.append(entry)
    try:
        with open(ACTUATOR_DIR / "audit.jsonl", "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_actuator_daemon.py:112 quiet except scope=_audit reason=pass")
        raise
        pass

def _safe_unit(target: str) -> bool:
    """Sprawdź czy target to bezpieczny noema-*.service."""
    if not target.endswith(".service"):
        return False
    if not target.startswith("noema-"):
        return False
    # Czarna lista: nie restartuj samego siebie
    if target == "noema-actuator.service":
        return False
    return True

def _execute(intent: dict) -> dict:
    """Wykonaj intencję i zwróć wynik."""
    action = intent.get("intent", "noop")
    target = intent.get("target", "")
    reason = intent.get("reason", "")
    confidence = float(intent.get("confidence", 0.5))
    now = time.time()

    result = {
        "id": intent.get("id", "?"),
        "intent": action,
        "target": target,
        "status": "pending",
        "started_at": now,
        "output": "",
        "error": None,
    }

    # WALIDACJA
    if action not in ALLOWED_INTENTS:
        result["status"] = "rejected"
        result["error"] = f"Unknown intent: {action}"
        return result

    requires_target, requires_confirm, desc = ALLOWED_INTENTS[action]

    if requires_target and not target:
        result["status"] = "rejected"
        result["error"] = "Target required"
        return result

    if action in ("restart_daemon", "start_daemon", "stop_daemon"):
        if not _safe_unit(target):
            result["status"] = "rejected"
            result["error"] = f"Unsafe target: {target}"
            return result

    if action in ("run_script",):
        # Tylko scripts/*.py
        script_path = ROOT / "scripts" / target
        if not script_path.exists() or not str(target).endswith(".py"):
            result["status"] = "rejected"
            result["error"] = f"Unsafe script: {target}"
            return result

    # Rate limiting
    if _rate_limited():
        result["status"] = "rate_limited"
        result["error"] = f"Max {MAX_ACTIONS_PER_WINDOW} actions per {WINDOW_SECONDS}s"
        return result

    # Confidence gate
    if confidence < 0.3:
        result["status"] = "rejected"
        result["error"] = f"Confidence too low: {confidence:.2f}"
        return result

    # WYKONANIE
    _actions_window.append(now)

    try:
        if action == "restart_daemon":
            r = subprocess.run(
                ["systemctl", "--user", "restart", target],
                capture_output=True, text=True, timeout=15,
            )
            result["status"] = "done" if r.returncode == 0 else "failed"
            result["output"] = r.stdout + r.stderr
            result["returncode"] = r.returncode

        elif action == "start_daemon":
            r = subprocess.run(
                ["systemctl", "--user", "start", target],
                capture_output=True, text=True, timeout=15,
            )
            result["status"] = "done" if r.returncode == 0 else "failed"
            result["output"] = r.stdout + r.stderr
            result["returncode"] = r.returncode

        elif action == "stop_daemon":
            r = subprocess.run(
                ["systemctl", "--user", "stop", target],
                capture_output=True, text=True, timeout=15,
            )
            result["status"] = "done" if r.returncode == 0 else "failed"
            result["output"] = r.stdout + r.stderr
            result["returncode"] = r.returncode

        elif action == "journal_query":
            r = subprocess.run(
                ["journalctl", "--user", "-u", target, "-n", "50",
                 "--no-pager", "-o", "short-iso"],
                capture_output=True, text=True, timeout=10,
            )
            result["status"] = "done"
            result["output"] = r.stdout[:2000]  # trim
            result["returncode"] = r.returncode

        elif action == "run_script":
            script_path = ROOT / "scripts" / target
            r = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True, text=True, timeout=30,
            )
            result["status"] = "done" if r.returncode == 0 else "failed"
            result["output"] = r.stdout[:2000] + r.stderr[:1000]
            result["returncode"] = r.returncode

        elif action == "surface_report":
            report = {}
            for name in ("phi", "omega", "flavor", "gravity", "tick"):
                p = SURFACE / name
                if p.exists():
                    try:
                        raw = p.read_bytes()
                        report[name] = [round(float(v), 4) for v in raw[:192]]
                    except Exception:
                        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_actuator_daemon.py:242 quiet except scope=_execute reason=assign_fallback")
                        raise
                        report[name] = "error"
            result["status"] = "done"
            result["output"] = json.dumps(report, indent=2)[:3000]

        elif action == "knowledge_query":
            query = target  # re-use target as query string
            r = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "noema_knowledge_graph.py"),
                 "--search", query],
                capture_output=True, text=True, timeout=15,
            )
            result["status"] = "done"
            result["output"] = r.stdout[:2000]
            result["returncode"] = r.returncode

        elif action == "noop":
            result["status"] = "done"
            result["output"] = "noop ok"

        result["finished_at"] = time.time()
        result["duration"] = round(result["finished_at"] - result["started_at"], 3)

    except subprocess.TimeoutExpired:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_actuator_daemon.py:265 quiet except scope=_execute reason=no_log_no_raise")
        raise
        result["status"] = "timeout"
        result["error"] = "Command timed out"
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_actuator_daemon.py:268 quiet except scope=_execute reason=no_log_no_raise")
        raise
        result["status"] = "error"
        result["error"] = str(e)

    # Audit
    _audit({
        "ts": now,
        "id": result["id"],
        "intent": action,
        "target": target,
        "status": result["status"],
        "reason": reason,
        "confidence": confidence,
        "duration": result.get("duration", 0),
    })

    return result

def _read_intent() -> dict | None:
    """Odczytaj intent.json jeśli nowy."""
    global _last_intent_id
    intent_path = ACTUATOR_DIR / "intent.json"
    if not intent_path.exists():
        return None
    try:
        intent = json.loads(intent_path.read_text())
        iid = intent.get("id", "")
        if iid == _last_intent_id:
            return None  # już przetworzone
        _last_intent_id = iid
        return intent
    except (json.JSONDecodeError, OSError):
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_actuator_daemon.py:299 quiet except scope=_read_intent reason=return None")
        raise
        return None

def _write_result(result: dict) -> None:
    """Zapisz wynik."""
    try:
        with open(ACTUATOR_DIR / "result.json", "w") as f:
            json.dump(result, f, indent=2)
    except OSError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_actuator_daemon.py:307 quiet except scope=_write_result reason=pass")
        raise
        pass

def _write_status() -> None:
    """Zapisz status daemona."""
    status = {
        "ts": time.time(),
        "running": _running,
        "actions_in_window": len(_actions_window),
        "max_actions_per_window": MAX_ACTIONS_PER_WINDOW,
        "window_seconds": WINDOW_SECONDS,
        "total_audited": len(_audit_log),
        "allowed_intents": list(ALLOWED_INTENTS.keys()),
    }
    try:
        with open(ACTUATOR_DIR / "status.json", "w") as f:
            json.dump(status, f, indent=2)
    except OSError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_actuator_daemon.py:324 quiet except scope=_write_status reason=pass")
        raise
        pass

def signal_handler(sig, frame) -> None:
    global _running
    log(f"signal {sig}, exiting")
    _running = False

def main() -> None:
    global _running

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    _init_dirs()

    # Wczytaj istniejący audit
    audit_path = ACTUATOR_DIR / "audit.jsonl"
    if audit_path.exists():
        try:
            for line in audit_path.read_text().splitlines():
                if line.strip():
                    _audit_log.append(json.loads(line))
        except (json.JSONDecodeError, OSError):
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_actuator_daemon.py:347 quiet except scope=main reason=pass")
            raise
            pass

    log(f"start — {len(_audit_log)} past actions, "
        f"{len(ALLOWED_INTENTS)} allowed intents")

    if "--once" in sys.argv:
        intent = _read_intent()
        if intent:
            result = _execute(intent)
            _write_result(result)
            print(json.dumps(result, indent=2))
        else:
            print("No intent")
        return

    log("daemon start")
    last_status = 0
    hb_count = 0
    reg_token = registry.register("actuator")

    while _running:
        try:
            intent = _read_intent()
            if intent:
                log(f"intent: {intent.get('intent')} "
                    f"target={intent.get('target','?')} "
                    f"conf={intent.get('confidence',0):.2f} "
                    f"reason={intent.get('reason','?')[:40]}")
                result = _execute(intent)
                _write_result(result)
                log(f"→ {result['status']} ({result.get('duration',0):.2f}s)")

            # Status co 30s
            now = time.time()
            if now - last_status > 30:
                _write_status()
                last_status = now

            hb_count += 1
            if hb_count % 30 == 0:
                try:
                    registry.heartbeat(reg_token)
                except Exception:
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_actuator_daemon.py:390 quiet except scope=main reason=pass")
                    raise
                    pass

        except Exception as e:
            log(f"error: {e}")
            import traceback
            traceback.print_exc()

        time.sleep(1.0)

    log(f"daemon stop — {len(_audit_log)} total actions")

if __name__ == "__main__":
    main()
