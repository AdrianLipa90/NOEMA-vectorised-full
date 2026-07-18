#!/usr/bin/env python3
"""Read-only Codex MCP surface for the canonical NOEMA tree.

This server deliberately exposes observations with their source and freshness.
It does not read OpenCode settings, mutate NOEMA state, or turn unavailable
state into numeric defaults.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROTOCOL_VERSION = "2024-11-05"
# The Codex server is anchored to its own checked-in canonical tree.  An
# inherited variable may describe an old terminal or a different checkout and
# must not silently rebind this server.
ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "runtime"
PATHS = ROOT / "config" / "noema_paths.json"
BRIDGE = RUNTIME / "wrappers" / "vector_continuous_cqcl_lingophysics_htri" / "noema_vector_continuous_bridge.py"
ORBITAL_STATE = Path("/media/adrian/New Volume/CIEL_memories/state/noema_orbital_state.json")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def digest(path: Path, *, semantic_json: bool = False) -> str | None:
    try:
        if semantic_json:
            value = json.loads(path.read_text(encoding="utf-8"))
            canonical = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def json_object(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, f"{type(exc).__name__}: {exc}"
    return (value, None) if isinstance(value, dict) else (None, "JSON value is not an object")


def cuda_observation() -> dict[str, Any]:
    """Observe the driver directly; never infer it from an absent state file."""
    try:
        probe = subprocess.run(
            ["/usr/bin/nvidia-smi", "--query-gpu=name,uuid", "--format=csv,noheader"],
            text=True, capture_output=True, timeout=8, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"available": False, "source": "nvidia-smi", "error": type(exc).__name__}
    lines = [line.strip() for line in probe.stdout.splitlines() if line.strip()]
    if probe.returncode != 0 or not lines:
        return {"available": None, "source": "nvidia-smi", "error": probe.stderr.strip() or "no GPU reported"}
    return {"available": True, "source": "nvidia-smi", "devices": lines}


def noema_status(_: dict[str, Any] | None = None) -> dict[str, Any]:
    state, state_error = json_object(ORBITAL_STATE)
    return {
        "status": "ok",
        "server": "codex_noema_surface",
        "timestamp": now(),
        "transport": "stdio",
        "canonical_root": str(ROOT),
        "canonical_root_exists": ROOT.is_dir(),
        "runtime_root": str(RUNTIME),
        "runtime_root_exists": RUNTIME.is_dir(),
        "paths_contract": {"path": str(PATHS), "sha256": digest(PATHS, semantic_json=True), "available": PATHS.is_file()},
        "orbital_state": {
            "path": str(ORBITAL_STATE),
            "available": state is not None,
            "sha256": digest(ORBITAL_STATE),
            "error": state_error,
            "source_timestamp": state.get("created_at") if state else None,
        },
        "cuda": cuda_observation(),
        "privacy": {"opencode_settings_read": False, "prompt_content_read": False},
    }


def htri_universal_bridge_status(_: dict[str, Any] | None = None) -> dict[str, Any]:
    state, state_error = json_object(ORBITAL_STATE)
    return {
        "status": "ok" if BRIDGE.is_file() else "unavailable",
        "timestamp": now(),
        "bridge": {"path": str(BRIDGE), "present": BRIDGE.is_file(), "sha256": digest(BRIDGE)},
        "cuda": cuda_observation(),
        "current_state": {
            "path": str(ORBITAL_STATE),
            "available": state is not None,
            "sha256": digest(ORBITAL_STATE),
            "error": state_error,
        },
        "interpretation": "CUDA is observed independently from orbital state; unavailable state is not reported as CUDA=false.",
    }


def phasenav_status(_: dict[str, Any] | None = None) -> dict[str, Any]:
    solver = ROOT / "head" / "NoemaSurface" / "runtime" / "cielingo_core" / "phasenav" / "solver.py"
    return {
        "status": "ok" if solver.is_file() else "unavailable",
        "timestamp": now(),
        "solver": {"path": str(solver), "present": solver.is_file(), "sha256": digest(solver)},
        "source": "canonical_tree_only",
    }


def phasenav_trace(args: dict[str, Any] | None = None) -> dict[str, Any]:
    """Run PhaseNavSolver.trace() over the given concept card ids. Read-only:
    loads whatever PhaseNav data is present (NOEMA_PHASENAV_DATA env var, or
    the loader's own default path) and reports what it finds, including an
    explicit empty trace if the data or a requested concept is absent — never
    a fabricated step."""
    args = args or {}
    concepts = args.get("concepts")
    if not isinstance(concepts, list) or not concepts or not all(isinstance(c, str) for c in concepts):
        return {"status": "error", "timestamp": now(), "error": "concepts must be a non-empty list of card-id strings"}
    src_root = str(ROOT / "src")
    if src_root not in sys.path:
        sys.path.insert(0, src_root)
    try:
        from ciel_geometry.phasenav.solver import PhaseNavSolver
    except ImportError as exc:
        return {"status": "error", "timestamp": now(), "error": f"solver import failed: {type(exc).__name__}: {exc}"}
    try:
        solver = PhaseNavSolver.load()
    except Exception as exc:
        return {"status": "error", "timestamp": now(), "error": f"PhaseNav data unavailable: {type(exc).__name__}: {exc}"}
    trace = solver.trace(concepts)
    return {
        "status": "ok",
        "timestamp": now(),
        "card_sequence": trace.card_sequence,
        "steps": [
            {
                "source_card_id": s.source_card_id,
                "target_card_id": s.target_card_id,
                "operator_hook": s.operator_hook,
                "operator_card_id": s.operator_card_id,
                "phase_start": s.phase_start,
                "phase_end": s.phase_end,
                "phase_delta": s.phase_delta,
                "holonomic_viscosity": s.holonomic_viscosity,
                "phasenav_affordance": s.phasenav_affordance,
                "transition_lane": s.transition_lane,
                "path_integral": s.path_integral,
            }
            for s in trace.steps
        ],
        "total_path_integral": trace.total_path_integral,
        "mean_viscosity": trace.mean_viscosity,
        "mean_affordance": trace.mean_affordance,
    }


TOOLS: dict[str, tuple[str, dict[str, Any], Any]] = {
    "noema_status": ("Read canonical NOEMA, orbital-state and CUDA observations without OpenCode configuration.", {"type": "object", "properties": {}}, noema_status),
    "htri_universal_bridge_status": ("Read bridge, orbital-state and direct CUDA observations without fallback values.", {"type": "object", "properties": {}}, htri_universal_bridge_status),
    "phasenav_status": ("Read availability and hash of the canonical PhaseNav solver.", {"type": "object", "properties": {}}, phasenav_status),
    "phasenav_trace": (
        "Run PhaseNav solver.trace() over concept card ids; loads PhaseNav data read-only and reports actual availability, never fabricated steps.",
        {"type": "object", "properties": {"concepts": {"type": "array", "items": {"type": "string"}}}, "required": ["concepts"]},
        phasenav_trace,
    ),
}


def send(message: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(message, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def handle(message: dict[str, Any]) -> None:
    method, msg_id = message.get("method"), message.get("id")
    if method == "initialize":
        send({"jsonrpc": "2.0", "id": msg_id, "result": {"protocolVersion": PROTOCOL_VERSION, "capabilities": {"tools": {}}, "serverInfo": {"name": "codex_noema_surface", "version": "1.0.0"}}})
        return
    if method == "notifications/initialized":
        return
    if method == "tools/list":
        tools = [{"name": name, "description": spec[0], "inputSchema": spec[1]} for name, spec in TOOLS.items()]
        send({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": tools}})
        return
    if method == "tools/call":
        params = message.get("params", {})
        name = params.get("name")
        spec = TOOLS.get(name)
        if spec is None:
            send({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32602, "message": f"unknown tool: {name}"}})
            return
        value = spec[2](params.get("arguments") if isinstance(params.get("arguments"), dict) else {})
        send({"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(value, ensure_ascii=False, sort_keys=True)}]}})
        return
    if msg_id is not None:
        send({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"unsupported method: {method}"}})


def main() -> int:
    for line in sys.stdin:
        try:
            value = json.loads(line)
            if isinstance(value, dict):
                handle(value)
        except Exception as exc:
            send({"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": type(exc).__name__}})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
