#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import struct
import time
from typing import Any

DEFAULT_ROOT = Path(os.environ.get("NOEMA_SURFACE_ROOT", "/dev/shm/ciel_noema"))
AUX_DIM = 36
AUX_BYTES = AUX_DIM * 8

JSON_INPUTS = {
    "current_memory": "current_memory.json",
    "current_task": "current_task.json",
    "active_path": "active_path.json",
    "closed_topics": "closed_topics.json",
    "timeline_head": "timeline_head.json",
    "provenance": "provenance.json",
    "latest_receipt": "receipts/latest.json",
}

DERIVED_STARTPOINT = Path("session/startpoint.json")
DERIVED_SYSTEM_MESSAGE = Path("session/system_message.txt")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_meta(path: Path) -> dict[str, Any]:
    st = path.stat()
    raw = path.read_bytes()
    return {
        "path": str(path),
        "size": st.st_size,
        "mtime_ns": st.st_mtime_ns,
        "sha256": sha256_bytes(raw),
    }


def read_json(path: Path) -> tuple[Any | None, dict[str, Any]]:
    meta = file_meta(path)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        meta["parse_status"] = "PASS"
        return value, meta
    except Exception as exc:
        meta["parse_status"] = "INVALID"
        meta["error"] = f"{type(exc).__name__}:{exc}"
        return None, meta


def read_aux(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"status": "UNAVAILABLE", "path": str(path)}
    try:
        raw = path.read_bytes()
        meta = file_meta(path)
        if len(raw) != AUX_BYTES:
            return {**meta, "status": "INVALID", "reason": f"size:{len(raw)}!=288"}
        vals = list(struct.unpack("<" + ("d" * AUX_DIM), raw))
        if not all(math.isfinite(v) for v in vals):
            return {**meta, "status": "INVALID", "reason": "non_finite"}
        re = sum(math.cos(v) for v in vals) / AUX_DIM
        im = sum(math.sin(v) for v in vals) / AUX_DIM
        return {
            **meta,
            "status": "PASS",
            "dim": AUX_DIM,
            "coherence": round(math.hypot(re, im), 9),
            "phase_vector_36d": [round(v, 9) for v in vals],
        }
    except Exception as exc:
        return {
            "status": "INVALID",
            "path": str(path),
            "reason": f"{type(exc).__name__}:{exc}",
        }


def unwrap(value: Any, preferred: str | None = None) -> Any:
    if isinstance(value, dict):
        if preferred and preferred in value:
            return value[preferred]
        for key in ("value", "state", "data", "current", "items"):
            if key in value:
                return value[key]
    return value


def build_packet(root: Path) -> dict[str, Any]:
    files: dict[str, Any] = {}
    values: dict[str, Any] = {}
    unknown: list[str] = []
    conflicts: list[str] = []

    for key, rel in JSON_INPUTS.items():
        path = root / rel
        if not path.is_file():
            files[key] = {"path": str(path), "status": "UNAVAILABLE"}
            unknown.append(key)
            continue
        value, meta = read_json(path)
        files[key] = meta
        if meta.get("parse_status") == "PASS":
            values[key] = value
        else:
            conflicts.append(f"{key}:invalid_json")

    aux = read_aux(root / "aux_phi")
    files["aux_phi"] = {
        k: v for k, v in aux.items()
        if k in {"path", "size", "mtime_ns", "sha256", "status", "reason"}
    }
    if aux["status"] == "UNAVAILABLE":
        unknown.append("aux_phi")
    elif aux["status"] == "INVALID":
        conflicts.append("aux_phi:invalid")

    current_task = unwrap(values.get("current_task"), "current_task")
    active_path = unwrap(values.get("active_path"), "active_path")
    closed_topics = unwrap(values.get("closed_topics"), "closed_topics")
    timeline_head = unwrap(values.get("timeline_head"), "timeline_head")
    provenance = unwrap(values.get("provenance"), "provenance")

    if conflicts:
        status = "CONFLICT"
    elif "current_memory" in values and current_task is not None and active_path is not None:
        status = "VERIFIED"
    elif values or aux.get("status") == "PASS":
        status = "PARTIAL"
    else:
        status = "UNKNOWN"

    packet = {
        "schema": "noema/session-startpoint/v1",
        "status": status,
        "surface_root": str(root),
        "observed_at_unix_ns": time.time_ns(),
        "authority": "derived_session_state_read_only_inputs",
        "current_task": current_task,
        "active_path": active_path,
        "closed_topics": closed_topics,
        "timeline_head": timeline_head,
        "provenance": provenance,
        "latest_receipt": values.get("latest_receipt"),
        "current_memory_present": "current_memory" in values,
        "aux": aux,
        "files": files,
        "unknown": sorted(set(unknown)),
        "conflicts": sorted(set(conflicts)),
    }

    canonical = json.dumps(packet, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    packet["packet_sha256"] = sha256_bytes(canonical)
    return packet


def compact_system_message(packet: dict[str, Any]) -> str:
    def one_line(value: Any, limit: int = 1000) -> str:
        if value is None:
            return "null"
        s = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        return s if len(s) <= limit else s[:limit] + "...<truncated>"

    aux = packet.get("aux", {})
    return "\n".join([
        "NOEMA_SURFACE_BOOT:",
        f"  status: {packet.get('status')}",
        f"  surface_root: {packet.get('surface_root')}",
        f"  packet_sha256: {packet.get('packet_sha256')}",
        f"  aux_status: {aux.get('status')}",
        f"  aux_dim: {aux.get('dim')}",
        f"  aux_sha256: {aux.get('sha256')}",
        f"  current_task: {one_line(packet.get('current_task'))}",
        f"  active_path: {one_line(packet.get('active_path'))}",
        f"  closed_topics: {one_line(packet.get('closed_topics'))}",
        f"  unknown: {one_line(packet.get('unknown'))}",
        f"  conflicts: {one_line(packet.get('conflicts'))}",
        "  rule: CURRENT_TASK > ACTIVE_PATH > recent-but-closed history",
        "  rule: one user correction must update ACTIVE_PATH; do not require repetition",
        "  authority: read_only_canonical_inputs; derived_session_output_only",
    ])


def emit(packet: dict[str, Any], root: Path) -> None:
    session = root / "session"
    session.mkdir(parents=True, exist_ok=True)
    startpoint = root / DERIVED_STARTPOINT
    system_msg = root / DERIVED_SYSTEM_MESSAGE
    startpoint.write_text(
        json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    system_msg.write_text(compact_system_message(packet) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="NOEMA /dev/shm session startpoint")
    ap.add_argument("--root", default=str(DEFAULT_ROOT))
    ap.add_argument("--probe-only", action="store_true",
                    help="do not write derived session/startpoint.json or system_message.txt")
    ap.add_argument("--codex-hook", action="store_true",
                    help="emit Codex SessionStart JSON on stdout")
    ns = ap.parse_args()

    root = Path(ns.root)
    packet = build_packet(root)

    if not ns.probe_only:
        emit(packet, root)

    if ns.codex_hook:
        payload = {
            "continue": True,
            "systemMessage": compact_system_message(packet),
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "runtime": "codex-native",
                "bridge": "NOEMA_SURFACE->AUX->binary",
                "surface_status": packet["status"],
                "packet_sha256": packet["packet_sha256"],
                "read_only_inputs": True,
            },
        }
        print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    else:
        print(json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
