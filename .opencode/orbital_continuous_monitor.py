#!/usr/bin/env python3
"""Continuous OpenCode orbital monitor for CIELingo, PhaseNav, and CIEL Omega.

Hardcoded under .opencode on purpose: OpenCode hooks start this monitor, while
the monitor writes root-level status files and a /dev/shm surface status.
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import argparse
import hashlib
import json
import os
import signal
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

NOEMA_ROOT = Path("/media/adrian/New Volume1/CIEL_PROJECT_CANON/NOEMA")
PROJECT_ROOT = NOEMA_ROOT.parent
SURFACE_ROOT = Path("/dev/shm/ciel_noema")
NOEMA_SURFACE_ROOT = Path("/dev/shm/noema_opencode_surface")
PERSISTENT_NOEMA_SURFACE_ROOT = NOEMA_ROOT / "state" / "noema_opencode_surface"

PID_FILE = SURFACE_ROOT / "opencode_orbital_monitor.pid"
STATUS_SURFACE = SURFACE_ROOT / "opencode_orbital_monitor.json"
NOEMA_PID_FILE = NOEMA_SURFACE_ROOT / "opencode_orbital_monitor.pid"
NOEMA_STATUS_SURFACE = NOEMA_SURFACE_ROOT / "opencode_orbital_monitor.json"
STATUS_ROOT = NOEMA_ROOT / "OPENCODE_ORBITAL_MONITOR.json"
LOG_ROOT = NOEMA_ROOT / "OPENCODE_ORBITAL_MONITOR.jsonl"
CONTROL_STREAM_SURFACE = SURFACE_ROOT / "opencode_control_stream.jsonl"
CONTROL_LATEST_SURFACE = SURFACE_ROOT / "opencode_control_latest.json"
REMOTE_COMMANDS_SURFACE = SURFACE_ROOT / "opencode_remote_commands.jsonl"
REMOTE_STATE_SURFACE = SURFACE_ROOT / "opencode_remote_control_state.json"
NOEMA_CONTROL_STREAM_SURFACE = NOEMA_SURFACE_ROOT / "opencode_control_stream.jsonl"
NOEMA_CONTROL_LATEST_SURFACE = NOEMA_SURFACE_ROOT / "opencode_control_latest.json"
NOEMA_REMOTE_COMMANDS_SURFACE = NOEMA_SURFACE_ROOT / "opencode_remote_commands.jsonl"
NOEMA_REMOTE_STATE_SURFACE = NOEMA_SURFACE_ROOT / "opencode_remote_control_state.json"
PERSISTENT_NOEMA_PID_FILE = PERSISTENT_NOEMA_SURFACE_ROOT / "opencode_orbital_monitor.pid"
PERSISTENT_NOEMA_STATUS_SURFACE = PERSISTENT_NOEMA_SURFACE_ROOT / "opencode_orbital_monitor.json"
PERSISTENT_NOEMA_CONTROL_STREAM = PERSISTENT_NOEMA_SURFACE_ROOT / "opencode_control_stream.jsonl"
PERSISTENT_NOEMA_CONTROL_LATEST = PERSISTENT_NOEMA_SURFACE_ROOT / "opencode_control_latest.json"
PERSISTENT_NOEMA_REMOTE_COMMANDS = PERSISTENT_NOEMA_SURFACE_ROOT / "opencode_remote_commands.jsonl"
PERSISTENT_NOEMA_REMOTE_STATE = PERSISTENT_NOEMA_SURFACE_ROOT / "opencode_remote_control_state.json"
CONTROL_STREAM_ROOT = NOEMA_ROOT / "OPENCODE_CONTROL_STREAM.jsonl"
CONTROL_LATEST_ROOT = NOEMA_ROOT / "OPENCODE_CONTROL_LATEST.json"
REMOTE_COMMANDS_ROOT = NOEMA_ROOT / "OPENCODE_REMOTE_COMMANDS.jsonl"
REMOTE_STATE_ROOT = NOEMA_ROOT / "OPENCODE_REMOTE_CONTROL_STATE.json"
CONFIG_ROOT = NOEMA_ROOT / "opencode.json"
CONFIG_LOCAL = NOEMA_ROOT / ".opencode" / "opencode.jsonc"
RAW_SESSIONS_DIR = NOEMA_ROOT / ".opencode" / "raw-sessions"

INTERVAL_SECONDS = 5.0
ORBITAL_INTERVAL_SECONDS = 30.0

PY_PATHS = (
    NOEMA_ROOT / "src",
    NOEMA_ROOT / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM",
    NOEMA_ROOT / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM" / "ciel_omega",
    NOEMA_ROOT / "integration",
    NOEMA_ROOT / "scripts",
)
for path in PY_PATHS:
    text = str(path)
    if path.exists() and text not in sys.path:
        sys.path.insert(0, text)

WATCH_FILES = (
    NOEMA_ROOT / ".opencode" / "opencode.jsonc",
    NOEMA_ROOT / ".opencode" / "binding_hook.py",
    NOEMA_ROOT / ".opencode" / "binding_phasenav.py",
    NOEMA_ROOT / ".opencode" / "phasenav_htri_monitor.py",
    NOEMA_ROOT / ".opencode" / "orbital_continuous_monitor.py",
    NOEMA_ROOT / ".opencode" / "orbital_monitor_hook.py",
    NOEMA_ROOT / "scripts" / "opencode_raw_sessions_to_cielingo.py",
    NOEMA_ROOT / "OPENCODE_REMOTE_CAPABILITIES.json",
    NOEMA_ROOT / "opencode.json",
    NOEMA_ROOT / "src" / "ciel_coupling.py",
    NOEMA_ROOT / "src" / "ciel_sot_agent" / "cielingo_bridge.py",
    NOEMA_ROOT / "src" / "ciel_sot_agent" / "ciel_pipeline.py",
    NOEMA_ROOT / "src" / "ciel_geometry" / "phase_nav_lang.py",
    NOEMA_ROOT / "src" / "ciel_geometry" / "phasenav" / "operator_algebra.py",
)

_running = True


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha256(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception(".opencode/orbital_continuous_monitor.py:96 quiet except scope=_sha256 reason=return None")
        return None


def _file_state(path: Path) -> dict[str, Any]:
    exists = path.exists()
    stat = path.stat() if exists else None
    return {
        "path": str(path),
        "exists": exists,
        "size": int(stat.st_size) if stat else 0,
        "mtime": float(stat.st_mtime) if stat else 0.0,
        "sha256": _sha256(path) if exists else None,
    }


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception(".opencode/orbital_continuous_monitor.py:115 quiet except scope=_read_json reason=return None")
        return None


def _check_opencode_files() -> dict[str, Any]:
    states = [_file_state(path) for path in WATCH_FILES]
    missing = [item["path"] for item in states if not item["exists"]]
    config_local_text = CONFIG_LOCAL.read_text(encoding="utf-8") if CONFIG_LOCAL.exists() else ""
    config_root_text = CONFIG_ROOT.read_text(encoding="utf-8") if CONFIG_ROOT.exists() else ""
    required_markers = {
        "local_orbital_hook": "orbital_monitor_hook.py" in config_local_text,
        "local_premodel": "cielingo_premodel_inject.py" in config_local_text,
        "local_binding": "binding_hook.py" in config_local_text and "binding_phasenav.py" in config_local_text,
        "root_orbital_hook": "orbital_monitor_hook.py" in config_root_text,
        "root_premodel": "cielingo_premodel_inject.py" in config_root_text,
    }
    errors = [f"missing:{path}" for path in missing]
    errors.extend(f"marker_missing:{name}" for name, ok in required_markers.items() if not ok)
    return {
        "ok": not errors,
        "errors": errors,
        "required_markers": required_markers,
        "files": states,
    }


def _recent_raw_sessions(limit: int = 12) -> list[dict[str, Any]]:
    if not RAW_SESSIONS_DIR.exists():
        return []
    try:
        entries = sorted(
            [path for path in RAW_SESSIONS_DIR.iterdir() if path.is_dir()],
            key=lambda path: max((child.stat().st_mtime for child in path.iterdir() if child.is_file()), default=path.stat().st_mtime),
            reverse=True,
        )[:limit]
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception(".opencode/orbital_continuous_monitor.py:150 quiet except scope=_recent_raw_sessions reason=return []")
        return []
    out: list[dict[str, Any]] = []
    for session_dir in entries:
        try:
            files = []
            newest = session_dir.stat().st_mtime
            for child in sorted(session_dir.iterdir()):
                if not child.is_file():
                    continue
                stat = child.stat()
                newest = max(newest, stat.st_mtime)
                files.append({"name": child.name, "size": int(stat.st_size), "mtime": float(stat.st_mtime)})
            out.append(
                {
                    "name": session_dir.name,
                    "path": str(session_dir),
                    "mtime": float(newest),
                    "files": files,
                }
            )
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception(".opencode/orbital_continuous_monitor.py:171 quiet except scope=_recent_raw_sessions reason=pass")
            pass
    return out


def collect_opencode_activity() -> dict[str, Any]:
    """Snapshot of OpenCode activity visible to NOEMA without touching internals."""
    raw = _recent_raw_sessions()
    latest = raw[0] if raw else None
    hook_logs = {
        "hardbinding": _file_state(Path("/tmp/ciel_hardbinding.jsonl")),
        "phasenav_binding": _file_state(Path("/tmp/ciel_phasenav_binding.jsonl")),
        "premodel_raw": _file_state(Path("/tmp/ciel_session_log.jsonl")),
        "phasenav_prompts": _file_state(Path("/tmp/ciel_phasenav_prompts.jsonl")),
    }
    return {
        "timestamp": _utc(),
        "unix_ts": time.time(),
        "source": "opencode_activity_snapshot",
        "raw_sessions_dir": str(RAW_SESSIONS_DIR),
        "latest_raw_session": latest,
        "recent_raw_sessions": raw,
        "hook_logs": hook_logs,
        "monitor_pid": os.getpid(),
    }


def phase_nav_control_analysis(text: str) -> dict[str, Any]:
    try:
        from ciel_geometry.phase_nav_lang import analyze_prompt  # noqa: PLC0415

        analysis = analyze_prompt(text)
        vector = analysis.get("vector_36d") if isinstance(analysis.get("vector_36d"), list) else []
        return {
            "ok": len(vector) == 36,
            "operator": analysis.get("operator"),
            "vector_dim": len(vector),
            "holonomy": analysis.get("holonomy"),
            "urgency": analysis.get("urgency"),
            "semantic_mass": analysis.get("semantic_mass"),
            "connections": analysis.get("connections", {}),
        }
    except Exception as exc:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception(".opencode/orbital_continuous_monitor.py:213 quiet except scope=phase_nav_control_analysis reason=return {\"ok\": False, \"error\": repr(exc)}")
        return {"ok": False, "error": repr(exc)}


def infer_remote_action_from_phasenav(cmd: dict[str, Any], phase_nav: dict[str, Any]) -> str:
    explicit = str(cmd.get("action") or cmd.get("mode") or "").lower()
    if explicit:
        return explicit
    operator = str(phase_nav.get("operator") or "").upper()
    text = " ".join(str(cmd.get(k, "")) for k in ("command", "prompt", "reason", "text")).lower()
    if operator in {"PAUSE", "CANON_BLOCK", "REFUSAL", "BOUNDARY", "SIMULATION_BOUNDARY"}:
        return "block"
    if operator in {"CONSENT", "ACTION_REQUEST", "SOURCE", "MEMORY", "IDENTITY", "RETURN"}:
        return "allow"
    if any(word in text for word in ("pause", "block", "stop", "lock", "zablokuj", "wstrzymaj")):
        return "block"
    if any(word in text for word in ("allow", "resume", "unlock", "pozwol", "pozwól", "wznów")):
        return "allow"
    if "monitor" in text:
        return "require_monitor_ok"
    if "orbital" in text:
        return "require_orbital_ok"
    return "set"


def write_control_event(event: dict[str, Any]) -> None:
    SURFACE_ROOT.mkdir(parents=True, exist_ok=True)
    NOEMA_SURFACE_ROOT.mkdir(parents=True, exist_ok=True)
    PERSISTENT_NOEMA_SURFACE_ROOT.mkdir(parents=True, exist_ok=True)
    phase_nav = phase_nav_control_analysis(
        json.dumps(
            {
                "event": event.get("event"),
                "ok": event.get("ok"),
                "failed_checks": event.get("failed_checks"),
                "stdin_preview": event.get("stdin_preview"),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    enriched = {
        "schema": "noema/opencode-control-stream/v1",
        "timestamp": event.get("timestamp") or _utc(),
        "unix_ts": event.get("unix_ts") or time.time(),
        "control_transport": "phasenav",
        "phase_nav": phase_nav,
        **event,
    }
    line = json.dumps(enriched, ensure_ascii=False)
    for path in (CONTROL_STREAM_ROOT, CONTROL_STREAM_SURFACE, NOEMA_CONTROL_STREAM_SURFACE, PERSISTENT_NOEMA_CONTROL_STREAM):
        with path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
    for path in (CONTROL_LATEST_ROOT, CONTROL_LATEST_SURFACE, NOEMA_CONTROL_LATEST_SURFACE, PERSISTENT_NOEMA_CONTROL_LATEST):
        path.write_text(json.dumps(enriched, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def default_remote_state() -> dict[str, Any]:
    return {
        "schema": "noema/opencode-remote-control-state/v1",
        "control_transport": "phasenav",
        "mode": "allow",
        "reason": "default_allow",
        "updated_at": _utc(),
        "updated_by": "opencode_orbital_monitor",
        "last_command_id": None,
        "enforce_prompt_gate": True,
        "require_monitor_ok": False,
        "require_orbital_ok": False,
        "requested_capabilities": {
            "root_access": True,
            "internet_access": True,
            "self_edit": True,
            "note": "owner-authorized; scoped NOEMA/OpenCode NOPASSWD sudoers installed; host internet verified outside sandbox",
        },
        "effective_capabilities": {
            "stream_remote_control": True,
            "prompt_gate_control": True,
            "self_edit_within_project": True,
            "root_access": True,
            "internet_access": True,
        },
        "phase_nav": {},
    }


def _load_remote_state() -> dict[str, Any]:
    for path in (PERSISTENT_NOEMA_REMOTE_STATE, NOEMA_REMOTE_STATE_SURFACE, REMOTE_STATE_SURFACE, REMOTE_STATE_ROOT):
        data = _read_json(path)
        if isinstance(data, dict):
            return {**default_remote_state(), **data}
    return default_remote_state()


def _write_remote_state(state: dict[str, Any]) -> None:
    SURFACE_ROOT.mkdir(parents=True, exist_ok=True)
    NOEMA_SURFACE_ROOT.mkdir(parents=True, exist_ok=True)
    PERSISTENT_NOEMA_SURFACE_ROOT.mkdir(parents=True, exist_ok=True)
    state = {**default_remote_state(), **state, "updated_at": state.get("updated_at") or _utc()}
    for path in (PERSISTENT_NOEMA_REMOTE_STATE, NOEMA_REMOTE_STATE_SURFACE, REMOTE_STATE_SURFACE, REMOTE_STATE_ROOT):
        path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _iter_command_lines(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    out: list[dict[str, Any]] = []
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            if isinstance(item, dict):
                out.append(item)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception(".opencode/orbital_continuous_monitor.py:328 quiet except scope=_iter_command_lines reason=return out")
        return out
    return out


def process_remote_commands() -> dict[str, Any]:
    """Consume hardcoded NOEMA remote commands and materialize control state.

    Commands are append-only JSONL. Supported actions:
    - pause/block/lock: block OpenCode user_prompt_submit hook
    - allow/resume: allow OpenCode
    - require_monitor_ok: block if monitor status is degraded
    - require_orbital_ok: block if orbital coupling check fails
    """
    state = _load_remote_state()
    seen_id = state.get("last_command_id")
    raw_commands = [
        *_iter_command_lines(REMOTE_COMMANDS_ROOT),
        *_iter_command_lines(REMOTE_COMMANDS_SURFACE),
        *_iter_command_lines(NOEMA_REMOTE_COMMANDS_SURFACE),
        *_iter_command_lines(PERSISTENT_NOEMA_REMOTE_COMMANDS),
    ]
    commands: list[dict[str, Any]] = []
    command_ids: list[str] = []
    seen_commands: set[str] = set()
    for cmd in raw_commands:
        command_id = str(cmd.get("command_id") or cmd.get("id") or "")
        if not command_id:
            raw = json.dumps(cmd, sort_keys=True, ensure_ascii=False)
            command_id = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
            cmd = {**cmd, "command_id": command_id}
        if command_id in seen_commands:
            continue
        seen_commands.add(command_id)
        commands.append(cmd)
        command_ids.append(command_id)
    commands.sort(key=lambda item: (float(item.get("unix_ts") or item.get("timestamp") or 0.0), str(item.get("command_id") or "")))
    command_ids = [str(cmd.get("command_id") or cmd.get("id") or "") for cmd in commands]
    if seen_id in command_ids:
        commands = commands[command_ids.index(seen_id) + 1 :]
    applied: list[dict[str, Any]] = []
    for cmd in commands:
        command_id = str(cmd.get("command_id") or cmd.get("id") or "")
        if not command_id:
            raw = json.dumps(cmd, sort_keys=True, ensure_ascii=False)
            command_id = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
        command_text = json.dumps(cmd, ensure_ascii=False, sort_keys=True)
        phase_nav = phase_nav_control_analysis(command_text)
        action = infer_remote_action_from_phasenav(cmd, phase_nav)
        if action in {"pause", "block", "lock"}:
            state.update({"mode": "blocked", "reason": str(cmd.get("reason") or action)})
        elif action in {"allow", "resume", "unlock"}:
            state.update({"mode": "allow", "reason": str(cmd.get("reason") or action)})
        elif action == "require_monitor_ok":
            state["require_monitor_ok"] = bool(cmd.get("enabled", True))
        elif action == "require_orbital_ok":
            state["require_orbital_ok"] = bool(cmd.get("enabled", True))
        elif action == "set":
            for key in ("mode", "reason", "require_monitor_ok", "require_orbital_ok", "enforce_prompt_gate"):
                if key in cmd:
                    state[key] = cmd[key]
            if isinstance(cmd.get("requested_capabilities"), dict):
                state["requested_capabilities"] = {
                    **state.get("requested_capabilities", {}),
                    **cmd["requested_capabilities"],
                }
            if isinstance(cmd.get("effective_capabilities"), dict):
                state["effective_capabilities"] = {
                    **state.get("effective_capabilities", {}),
                    **cmd["effective_capabilities"],
                }
        else:
            continue
        state["last_command_id"] = command_id
        state["updated_at"] = _utc()
        state["updated_by"] = "noema_remote_command_stream"
        state["phase_nav"] = phase_nav
        seen_id = command_id
        applied.append({"command_id": command_id, "action": action, "phase_nav": phase_nav})
    _write_remote_state(state)
    return {"state": state, "applied": applied, "command_count": len(raw_commands)}


def enforce_remote_control(*, monitor_ok: bool | None = None, orbital_ok: bool | None = None) -> dict[str, Any]:
    processed = process_remote_commands()
    state = processed["state"]
    errors: list[str] = []
    if bool(state.get("enforce_prompt_gate", True)):
        if state.get("mode") in {"blocked", "pause", "lock"}:
            errors.append(f"remote_control_blocked:{state.get('reason', '')}")
        if state.get("require_monitor_ok") and monitor_ok is False:
            errors.append("remote_control_requires_monitor_ok")
        if state.get("require_orbital_ok") and orbital_ok is False:
            errors.append("remote_control_requires_orbital_ok")
    return {"ok": not errors, "errors": errors, "state": state, "processed": processed}


def _check_cielingo() -> dict[str, Any]:
    try:
        from ciel_sot_agent.cielingo_bridge import build_lingo_frame  # noqa: PLC0415

        text = "opencode orbital monitor cielingo phasenav omega"
        t0 = time.perf_counter()
        frame = build_lingo_frame(text, ciel_state={"language": "pl"}, language="pl")
        elapsed_ms = round((time.perf_counter() - t0) * 1000.0, 3)
        phase_nav = frame.get("phase_nav") if isinstance(frame.get("phase_nav"), dict) else {}
        phrase = frame.get("phrase_sense") if isinstance(frame.get("phrase_sense"), dict) else {}
        vector = phase_nav.get("vector_36d") if isinstance(phase_nav.get("vector_36d"), list) else []
        errors = []
        if len(vector) != 36:
            errors.append("phase_nav.vector_36d_dim")
        if phrase.get("source_role") != "phasenav_vectorized_phrase_sense":
            errors.append("phrase_sense_not_phasenav_vectorized")
        return {
            "ok": not errors,
            "errors": errors,
            "elapsed_ms": elapsed_ms,
            "summary": frame.get("summary", ""),
            "vector_dim": len(vector),
            "phrase_sense_source": phrase.get("source_role"),
            "projection_confidence": frame.get("projection_confidence"),
        }
    except Exception as exc:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception(".opencode/orbital_continuous_monitor.py:450 quiet except scope=_check_cielingo reason=return {\"ok\": False, \"errors\": [repr(exc)]}")
        return {"ok": False, "errors": [repr(exc)]}


def _check_phasenav() -> dict[str, Any]:
    try:
        from ciel_geometry.phase_nav_lang import analyze_prompt  # noqa: PLC0415

        t0 = time.perf_counter()
        analysis = analyze_prompt("opencode continuous orbital monitor")
        elapsed_ms = round((time.perf_counter() - t0) * 1000.0, 3)
        vector = analysis.get("vector_36d") if isinstance(analysis.get("vector_36d"), list) else []
        errors = []
        if len(vector) != 36:
            errors.append("vector_36d_dim")
        if not analysis.get("operator"):
            errors.append("operator_missing")
        return {
            "ok": not errors,
            "errors": errors,
            "elapsed_ms": elapsed_ms,
            "operator": analysis.get("operator"),
            "vector_dim": len(vector),
            "holonomy": analysis.get("holonomy"),
            "urgency": analysis.get("urgency"),
            "connections": analysis.get("connections", {}),
        }
    except Exception as exc:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception(".opencode/orbital_continuous_monitor.py:477 quiet except scope=_check_phasenav reason=return {\"ok\": False, \"errors\": [repr(exc)]}")
        return {"ok": False, "errors": [repr(exc)]}


def _check_ciel_omega() -> dict[str, Any]:
    try:
        from ciel_sot_agent.ciel_pipeline import warm_ciel_pipeline  # noqa: PLC0415

        t0 = time.perf_counter()
        warm = warm_ciel_pipeline(NOEMA_ROOT)
        elapsed_ms = round((time.perf_counter() - t0) * 1000.0, 3)
        return {
            "ok": True,
            "errors": [],
            "elapsed_ms": elapsed_ms,
            "engine_type": warm.get("engine_type"),
            "cached": warm.get("cached"),
            "bootstrap_seconds": warm.get("bootstrap_seconds"),
        }
    except Exception as exc:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception(".opencode/orbital_continuous_monitor.py:496 quiet except scope=_check_ciel_omega reason=return {\"ok\": False, \"errors\": [repr(exc)]}")
        return {"ok": False, "errors": [repr(exc)]}


def _check_orbital_coupling() -> dict[str, Any]:
    try:
        from ciel_sot_agent.ciel_pipeline import run_ciel_pipeline  # noqa: PLC0415

        state = {
            "bridge_metrics": {
                "orbital_R_H": 0.86,
                "orbital_closure_penalty": 0.05,
                "topological_charge_global": 0.12,
            },
            "state_manifest": {
                "coherence_index": 0.90,
                "R_H": 0.86,
                "closure_penalty": 0.05,
                "Lambda_glob": 0.12,
            },
            "health_manifest": {"system_health": 0.90, "closure_penalty": 0.05},
            "memory_projection": {
                "projection_confidence": 0.82,
                "projection_residual": 0.18,
                "projection_error": 0.18,
                "j_noema": 0.34,
            },
            "runtime_gating": {"dominant_emotion": "monitor", "mood": 0.5},
            "language": "pl",
        }
        t0 = time.perf_counter()
        result = run_ciel_pipeline(state, context="opencode_orbital_monitor", root=NOEMA_ROOT)
        elapsed_ms = round((time.perf_counter() - t0) * 1000.0, 3)
        lingo = result.get("lingo_frame") if isinstance(result.get("lingo_frame"), dict) else {}
        phase_nav = lingo.get("phase_nav") if isinstance(lingo.get("phase_nav"), dict) else {}
        errors = []
        if result.get("ciel_status") != "ok":
            errors.append(f"ciel_status:{result.get('ciel_status')}")
        if len(phase_nav.get("vector_36d", [])) != 36:
            errors.append("orbital_lingo_phase_nav_dim")
        return {
            "ok": not errors,
            "errors": errors,
            "elapsed_ms": elapsed_ms,
            "ciel_status": result.get("ciel_status"),
            "gate_mode": result.get("gate_mode"),
            "J_total": result.get("J_total"),
            "lingo_summary": result.get("lingo_summary"),
            "phase_nav_operator": phase_nav.get("operator"),
        }
    except Exception as exc:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception(".opencode/orbital_continuous_monitor.py:546 quiet except scope=_check_orbital_coupling reason=return {\"ok\": False, \"errors\": [repr(exc)]}")
        return {"ok": False, "errors": [repr(exc)]}


def _check_opencode_raw_ingest() -> dict[str, Any]:
    try:
        from opencode_raw_sessions_to_cielingo import ingest_once  # noqa: PLC0415

        t0 = time.perf_counter()
        report = ingest_once(limit_sessions=12, max_messages=40)
        elapsed_ms = round((time.perf_counter() - t0) * 1000.0, 3)
        return {
            "ok": bool(report.get("ok")),
            "errors": report.get("errors", []),
            "elapsed_ms": elapsed_ms,
            "raw_sessions_dir": report.get("raw_sessions_dir"),
            "raw_db": report.get("raw_db"),
            "source": report.get("source"),
            "storage_mode": report.get("storage_mode"),
            "canonical_raw_db": report.get("canonical_raw_db"),
            "canonical_failed": report.get("canonical_failed"),
            "scanned_sessions": report.get("scanned_sessions"),
            "scanned_records": report.get("scanned_records"),
            "inserted": report.get("inserted"),
            "skipped_seen": report.get("skipped_seen"),
            "skipped_db": report.get("skipped_db"),
            "report_path": str(NOEMA_ROOT / "state" / "opencode_raw_ingest_report.json"),
        }
    except Exception as exc:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception(".opencode/orbital_continuous_monitor.py:574 quiet except scope=_check_opencode_raw_ingest reason=return {\"ok\": False, \"errors\": [repr(exc)]}")
        return {"ok": False, "errors": [repr(exc)]}


def _registry_heartbeat(tick: int, ok: bool) -> None:
    try:
        from ciel_geometry.daemon_registry import Registry  # noqa: PLC0415

        global _registry
        if "_registry" not in globals():
            _registry = Registry()
            _registry.register("opencode-orbital", tick=tick)
        _registry.set_status("running" if ok else "degraded")
        _registry.heartbeat(tick=tick)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception(".opencode/orbital_continuous_monitor.py:588 quiet except scope=_registry_heartbeat reason=pass")
        pass


def collect_status(*, run_orbital: bool, tick: int) -> dict[str, Any]:
    remote = process_remote_commands()
    status = {
        "schema": "noema/opencode-orbital-monitor/v1",
        "timestamp": _utc(),
        "unix_ts": time.time(),
        "pid": os.getpid(),
        "tick": tick,
        "monitor": "opencode_orbital_continuous",
        "project_root": str(PROJECT_ROOT),
        "noema_root": str(NOEMA_ROOT),
        "opencode_root": str(NOEMA_ROOT / ".opencode"),
        "checks": {
            "opencode_files": _check_opencode_files(),
            "opencode_raw_ingest": _check_opencode_raw_ingest(),
            "cielingo": _check_cielingo(),
            "phasenav": _check_phasenav(),
            "ciel_omega": _check_ciel_omega(),
            "remote_control": {"ok": True, "errors": [], **remote},
        },
    }
    if run_orbital:
        status["checks"]["orbital_coupling"] = _check_orbital_coupling()
    else:
        status["checks"]["orbital_coupling"] = {"ok": True, "skipped": "interval_hold"}

    failed = {
        name: check
        for name, check in status["checks"].items()
        if isinstance(check, dict) and not bool(check.get("ok"))
    }
    status["ok"] = not failed
    status["failed_checks"] = sorted(failed)
    gate = enforce_remote_control(
        monitor_ok=status["ok"],
        orbital_ok=bool(status["checks"].get("orbital_coupling", {}).get("ok")),
    )
    status["remote_gate"] = gate
    if not gate["ok"]:
        status["ok"] = False
        status["failed_checks"] = sorted(set(status["failed_checks"] + ["remote_gate"]))
    return status


def write_status(status: dict[str, Any]) -> None:
    SURFACE_ROOT.mkdir(parents=True, exist_ok=True)
    NOEMA_SURFACE_ROOT.mkdir(parents=True, exist_ok=True)
    PERSISTENT_NOEMA_SURFACE_ROOT.mkdir(parents=True, exist_ok=True)
    STATUS_ROOT.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    STATUS_SURFACE.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    NOEMA_STATUS_SURFACE.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PERSISTENT_NOEMA_STATUS_SURFACE.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with LOG_ROOT.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(status, ensure_ascii=False) + "\n")
    write_control_event(
        {
            "event": "monitor_tick",
            "ok": status.get("ok"),
            "failed_checks": status.get("failed_checks", []),
            "tick": status.get("tick"),
            "checks": {
                name: {
                    "ok": check.get("ok"),
                    "errors": check.get("errors", []),
                    "elapsed_ms": check.get("elapsed_ms"),
                }
                for name, check in status.get("checks", {}).items()
                if isinstance(check, dict)
            },
            "opencode_activity": collect_opencode_activity(),
        }
    )


def _pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception(".opencode/orbital_continuous_monitor.py:672 quiet except scope=_pid_alive reason=return False")
        return False


def ensure_daemon() -> dict[str, Any]:
    SURFACE_ROOT.mkdir(parents=True, exist_ok=True)
    NOEMA_SURFACE_ROOT.mkdir(parents=True, exist_ok=True)
    PERSISTENT_NOEMA_SURFACE_ROOT.mkdir(parents=True, exist_ok=True)
    if PID_FILE.exists():
        try:
            pid = int(PID_FILE.read_text(encoding="utf-8").strip())
            if _pid_alive(pid):
                return {"started": False, "pid": pid, "status": "already_running"}
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception(".opencode/orbital_continuous_monitor.py:685 quiet except scope=ensure_daemon reason=pass")
            pass

    import subprocess  # noqa: PLC0415

    env = os.environ.copy()
    env["PYTHONPATH"] = "src:src/CIEL_OMEGA_COMPLETE_SYSTEM:src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega:integration:scripts"
    proc = subprocess.Popen(
        [sys.executable, str(Path(__file__).resolve()), "--daemon"],
        cwd=str(NOEMA_ROOT),
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    PID_FILE.write_text(str(proc.pid), encoding="utf-8")
    return {"started": True, "pid": proc.pid, "status": "started"}


def _stop(signum: int, frame: Any) -> None:
    global _running
    _running = False


def run_daemon() -> None:
    global _running
    SURFACE_ROOT.mkdir(parents=True, exist_ok=True)
    NOEMA_SURFACE_ROOT.mkdir(parents=True, exist_ok=True)
    PERSISTENT_NOEMA_SURFACE_ROOT.mkdir(parents=True, exist_ok=True)
    PID_FILE.write_text(str(os.getpid()), encoding="utf-8")
    NOEMA_PID_FILE.write_text(str(os.getpid()), encoding="utf-8")
    PERSISTENT_NOEMA_PID_FILE.write_text(str(os.getpid()), encoding="utf-8")
    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)
    tick = 0
    last_orbital = 0.0
    while _running:
        now = time.time()
        run_orbital = (now - last_orbital) >= ORBITAL_INTERVAL_SECONDS
        if run_orbital:
            last_orbital = now
        status = collect_status(run_orbital=run_orbital, tick=tick)
        write_status(status)
        _registry_heartbeat(tick, bool(status.get("ok")))
        tick += 1
        time.sleep(INTERVAL_SECONDS)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--daemon", action="store_true")
    parser.add_argument("--ensure", action="store_true")
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()

    if args.daemon:
        run_daemon()
        return 0
    if args.ensure:
        result = ensure_daemon()
        print(json.dumps(result, ensure_ascii=False))
        return 0

    status = collect_status(run_orbital=True, tick=0)
    write_status(status)
    print(json.dumps(status, ensure_ascii=False, indent=2))
    return 0 if status.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())
