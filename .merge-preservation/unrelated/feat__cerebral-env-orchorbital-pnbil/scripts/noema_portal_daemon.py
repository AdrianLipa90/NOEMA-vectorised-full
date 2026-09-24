#!/usr/bin/env python3
"""NOEMA Portal Daemon — żywy interfejs systemu NOEMA.

Zamiast surowego python3 -m http.server:
  - Rejestracja w daemon registry + heartbeat
  - Surface mmap przez ensure_surface()
  - REST API: /api/live, /api/status, /api/health, /api/metrics/all
  - Serwuje pliki statyczne z site/ na 18888
  - Systemd: noema-portal.service

Usage:
  noema_portal_daemon.py [--port PORT]
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

import http.server
import copy
import hashlib
import hmac
import json
import math
import os
import signal
import socket
import sys
import time
import threading
from pathlib import Path
from typing import Any

from ciel_geometry.noema_registry import registry as nreg
from ciel_geometry.orbital_state_contract import summarize_verified_orbital_state
from ciel_geometry.paths import P as _P
from ciel_hub.portal_contracts import build_system_catalog as build_contract_system_catalog, normalize_metric

# Legacy task/knowledge database paths were transient; both databases now
# resolve through the canonical paths contract.
_KNOWLEDGE_DB_PATH = str(_P.DB.KNOWLEDGE)
_TASKPLAN_DB_PATH = str(_P.DB.TASKPLAN)

# ── Ścieżki ────────────────────────────────────────────────────────────
NOEMA_ROOT = Path(__file__).resolve().parent.parent
SITE_ROOT = NOEMA_ROOT / "site"
SYSTEM_MAP_PATH = NOEMA_ROOT / "system_map_v2.json"
PORTAL_RUNTIME_ROOT = NOEMA_ROOT / "runtime" / "portal_state"
EMBEDDING_CACHE_ROOT = NOEMA_ROOT / "runtime" / "cache"
# The portal is observational only: resolve the volatile surface through the
# canonical paths contract instead of embedding a second literal path here.
# This keeps every surface read aligned with the same contract used by NOEMA
# daemons and makes a path mismatch fail at contract load time.
SURFACE_ROOT = Path(str(_P.SURFACE))
PORT = int(os.environ.get("PORT") or os.environ.get("NOEMA_PORTAL_PORT", "18888"))
HOST = os.environ.get("NOEMA_PORTAL_HOST", "127.0.0.1")
CHAT_BACKEND_TIMEOUT_SECONDS = max(
    1.0,
    min(45.0, float(os.environ.get("NOEMA_PORTAL_CHAT_TIMEOUT_SECONDS", "35"))),
)
# Receipts are operational records, not ephemeral tmpfs state.  Keep them in
# the canon runtime tree so restart/read-back semantics remain reproducible.
THREAD_MEMORY_PATH = PORTAL_RUNTIME_ROOT / "ciel_thread_memory.jsonl"
OPERATION_RECEIPT_PATH = PORTAL_RUNTIME_ROOT / "operation_receipts.jsonl"
THREAD_CONTENT_CAPABILITY_TOKEN = os.environ.get("NOEMA_PORTAL_THREAD_CONTENT_TOKEN", "")
OPERATIONS_CAPABILITY_TOKEN = os.environ.get("NOEMA_PORTAL_OPERATIONS_CAPABILITY_TOKEN", "")
OPERATIONS_ENABLED = os.environ.get("NOEMA_PORTAL_OPERATIONS_ENABLED", "0") == "1"
_THREAD_JOURNAL_LOCK = threading.Lock()
_OPERATION_LOCK = threading.Lock()
_OPERATION_PLANS: dict[str, dict[str, Any]] = {}
_OPERATION_RECEIPTS: list[dict[str, Any]] = []
_OPERATION_ALLOWLIST = {
    "service.restart": {"label": "Restart usługi", "risk": "high", "rollback": "restart poprzedniego stanu, jeśli usługa wspiera"},
    "daemon.reload": {"label": "Reload daemona", "risk": "medium", "rollback": "ponowne wczytanie poprzedniej konfiguracji"},
    "queue.retry": {"label": "Ponów zadanie kolejki", "risk": "low", "rollback": "brak — operacja idempotentna"},
    "phasenav.apply": {"label": "Zastosuj plan PhaseNav", "risk": "high", "rollback": "wymagany jawny plan odwrócenia"},
}


def _receipt_envelope(receipt: dict[str, Any]) -> dict[str, Any]:
    """Bind an operation receipt to its exact, canonical JSON representation."""
    canonical = json.dumps(receipt, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return {
        "receipt": receipt,
        "sha256": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
    }


def _load_operation_receipts(path: Path | None = None) -> list[dict[str, Any]]:
    """Read only checksum-valid append-only receipts; corrupt rows stay excluded."""
    target = path or OPERATION_RECEIPT_PATH
    if not target.exists():
        return []
    receipts: list[dict[str, Any]] = []
    for line in target.read_text(encoding="utf-8").splitlines():
        try:
            envelope = json.loads(line)
            receipt = envelope["receipt"]
            if isinstance(receipt, dict) and hmac.compare_digest(
                str(envelope.get("sha256", "")), _receipt_envelope(receipt)["sha256"]
            ):
                receipts.append(receipt)
        except (json.JSONDecodeError, KeyError, TypeError):
            continue
    return receipts


def _append_operation_receipt(receipt: dict[str, Any], path: Path | None = None) -> None:
    """Durably append a non-secret receipt before exposing it through the API."""
    target = path or OPERATION_RECEIPT_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(_receipt_envelope(receipt), ensure_ascii=False, sort_keys=True)
    with target.open("a", encoding="utf-8") as handle:
        handle.write(payload + "\n")
        handle.flush()
        os.fsync(handle.fileno())


_OPERATION_RECEIPTS.extend(_load_operation_receipts())

# ciel_omega lives under src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega, one level
# deeper than src/ciel_geometry — that extra directory was never added to
# sys.path, so `from ciel_omega.memory import ...` failed with
# "No module named 'ciel_omega'" even though src/ itself was already on path.
_CIEL_OMEGA_PARENT = NOEMA_ROOT / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM"
if _CIEL_OMEGA_PARENT.is_dir() and str(_CIEL_OMEGA_PARENT) not in sys.path:
    sys.path.insert(0, str(_CIEL_OMEGA_PARENT))

# ─── Stan globalny ──────────────────────────────────────────────────────
surface: dict[str, Any] | None = None
reg_token: Any = None
start_time: float = 0.0

PORTAL_SNAPSHOT_SCHEMA = "NOEMA_PORTAL_SURFACE_SNAPSHOT/1"
PORTAL_SNAPSHOT_SOURCE = str(SURFACE_ROOT)
PORTAL_SNAPSHOT_TTL_SECONDS = max(
    0.05,
    min(2.0, float(os.environ.get("NOEMA_PORTAL_SNAPSHOT_TTL_SECONDS", "0.5"))),
)
PORTAL_SNAPSHOT_STALE_SECONDS = max(
    1.0,
    float(os.environ.get("NOEMA_PORTAL_SNAPSHOT_STALE_SECONDS", "5")),
)
PORTAL_MATH_SOURCE = NOEMA_ROOT / "integration" / "reports" / "orbital_bridge" / "orbital_bridge_report.json"
PORTAL_MATH_STALE_SECONDS = max(
    5.0,
    # orbital_bridge.build_orbital_bridge() caches its (expensive, 20-step
    # global pass) result for 600s (_BRIDGE_CACHE_TTL) before recomputing —
    # a 120s default here meant closure_eba/r_h showed "degraded" as stale
    # for ~80% of every real refresh cycle even with a perfectly healthy
    # cielingo-sync daemon. Match the actual refresh cadence, with margin.
    float(os.environ.get("NOEMA_PORTAL_MATH_STALE_SECONDS", "660")),
)
_PORTAL_SNAPSHOT_LOCK = threading.RLock()
_PORTAL_SNAPSHOT_CACHE: dict[str, Any] = {"expires_at": 0.0, "value": None}
_PORTAL_SOURCE_CLOCK: dict[str, Any] = {"tick": None, "timestamp": None}
_PHASENAV_GRAPHICS_CACHE: dict[tuple[str, str], tuple[float, dict[str, Any]]] = {}
_PHASENAV_GRAPHICS_CACHE_LOCK = threading.Lock()


def _content_digest(content: Any) -> str:
    return hashlib.sha256(str(content or "").encode("utf-8")).hexdigest()


def _bounded_context_metadata(metadata: Any) -> dict[str, Any]:
    """Keep only small, non-content phase/context scalars in public journals."""
    if not isinstance(metadata, dict):
        return {}
    allowed = (
        "schema", "phase", "target_phase", "coherence", "context_lane",
        "context_id", "operator", "tick", "mode", "n_concepts",
        "diagnostics_status", "coherence_status", "coherence_source",
        "soul_status", "soul_source", "ethics_status", "ethics_source",
        "mood_status", "mood_source", "tick_status", "mode_status",
        "n_concepts_status", "context_resolution", "context_resolution_status",
        "phase_gate", "phase_gate_status", "phase_gate_score",
        "phase_gate_score_status", "phase_gate_tension",
        "phase_gate_tension_status", "dialogue_act", "dialogue_act_status",
        "dialogue_confidence", "dialogue_confidence_status",
        "repair_requested", "repair_requested_status",
    )
    bounded: dict[str, Any] = {}
    for key in allowed:
        value = metadata.get(key)
        if isinstance(value, bool) or isinstance(value, (int, float)):
            bounded[key] = value
        elif isinstance(value, str):
            bounded[key] = value[:64]
    return bounded


def _thread_journal_entry(
    *, timestamp: float, session_id: str, role: str, content: Any, context_metadata: Any = None
) -> dict[str, Any]:
    text = str(content or "")
    return {
        "timestamp": float(timestamp),
        "ts": float(timestamp),
        "session_id": str(session_id)[:128],
        "role": role if role in {"user", "assistant", "system", "tool"} else "system",
        "digest": _content_digest(text),
        "length": len(text),
        "context_metadata": _bounded_context_metadata(context_metadata),
    }


def _append_thread_journal(entries: list[dict[str, Any]], path: Path | None = None) -> None:
    target = path or THREAD_MEMORY_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    with _THREAD_JOURNAL_LOCK, target.open("a", encoding="utf-8") as handle:
        for entry in entries:
            handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _public_thread_entry(entry: dict[str, Any]) -> dict[str, Any]:
    """Redact both new digest-only records and historical raw-content records."""
    content = entry.get("content", entry.get("text", entry.get("message", "")))
    timestamp = entry.get("timestamp", entry.get("ts"))
    digest = entry.get("digest") or _content_digest(content)
    length = entry.get("length")
    if length is None:
        length = len(str(content or ""))
    return {
        "session_id": str(entry.get("session_id", ""))[:128],
        "timestamp": timestamp,
        "ts": timestamp,
        "role": entry.get("role", "system") if entry.get("role") in {"user", "assistant", "system", "tool"} else "system",
        "digest": str(digest)[:64],
        "length": max(0, int(length)),
        "context_metadata": _bounded_context_metadata(entry.get("context_metadata", entry)),
    }


def _diagnostic_status(value: Any) -> str:
    return "available" if value is not None else "unavailable"


def _finite_number(value: Any) -> int | float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return value if math.isfinite(float(value)) else None


def _first_diagnostic_value(
    sources: tuple[tuple[str, dict[str, Any], tuple[str, ...]], ...]
) -> tuple[Any, str | None]:
    for source_name, mapping, keys in sources:
        value = _first_present(mapping, *keys)
        if value is not None:
            return value, source_name
    return None, None


def build_chat_diagnostics(
    surface_state: dict[str, Any] | None,
    ciel_state: dict[str, Any] | None,
    frame_data: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build chat diagnostics without neutral-value or label fallbacks."""
    sf_state = surface_state if isinstance(surface_state, dict) else {}
    ciel = ciel_state if isinstance(ciel_state, dict) else {}
    frame = frame_data if isinstance(frame_data, dict) else {}

    soul, soul_source = _first_diagnostic_value((
        ("surface", sf_state, ("soul_invariant",)),
        ("ciel_state", ciel, ("soul_invariant",)),
    ))
    ethics, ethics_source = _first_diagnostic_value((
        ("surface", sf_state, ("ethical_score",)),
        ("ciel_state", ciel, ("ethical_score",)),
    ))
    coherence, coherence_source = _first_diagnostic_value((
        ("surface", sf_state, ("coherence", "coherence_index")),
        ("ciel_state", ciel, ("coherence", "coherence_index")),
    ))
    mood, mood_source = _first_diagnostic_value((
        ("surface", sf_state, ("mood_normalized", "mood")),
        ("ciel_state", ciel, ("mood_raw", "mood_normalized", "mood")),
    ))
    soul = _finite_number(soul)
    ethics = _finite_number(ethics)
    coherence = _finite_number(coherence)
    mood = _finite_number(mood)

    tick = _first_present(sf_state, "tick", "noema_tick")
    tick = tick if isinstance(tick, int) and not isinstance(tick, bool) else None
    mode = _first_present(ciel, "operating_mode")
    mode = mode.strip() if isinstance(mode, str) and mode.strip() else None

    if "n_concepts" not in frame or frame["n_concepts"] is None:
        n_concepts = None
    elif isinstance(frame["n_concepts"], (list, tuple)):
        n_concepts = len(frame["n_concepts"])
    elif isinstance(frame["n_concepts"], int) and not isinstance(frame["n_concepts"], bool) and frame["n_concepts"] >= 0:
        n_concepts = frame["n_concepts"]
    else:
        n_concepts = None

    continuity = frame.get("continuity") if isinstance(frame.get("continuity"), dict) else {}
    gate = frame.get("phase_gate") if isinstance(frame.get("phase_gate"), dict) else {}
    dialogue = frame.get("dialogue") if isinstance(frame.get("dialogue"), dict) else {}
    context_resolution = continuity.get("context_resolution")
    context_resolution = context_resolution[:64] if isinstance(context_resolution, str) and context_resolution else None
    phase_gate = gate.get("disposition")
    phase_gate = phase_gate[:32] if isinstance(phase_gate, str) and phase_gate else None
    phase_gate_score = _finite_number(gate.get("score"))
    phase_gate_tension = _finite_number(gate.get("tension"))
    dialogue_act = dialogue.get("act")
    dialogue_act = dialogue_act[:32] if isinstance(dialogue_act, str) and dialogue_act else None
    dialogue_confidence = _finite_number(dialogue.get("confidence"))
    repair_requested = dialogue.get("repair_requested")
    repair_requested = repair_requested if isinstance(repair_requested, bool) else None

    diagnostics: dict[str, Any] = {
        "coherence": coherence,
        "coherence_status": _diagnostic_status(coherence),
        "coherence_source": coherence_source if coherence is not None else None,
        "soul": soul,
        "soul_status": _diagnostic_status(soul),
        "soul_source": soul_source if soul is not None else None,
        "ethics": ethics,
        "ethics_status": _diagnostic_status(ethics),
        "ethics_source": ethics_source if ethics is not None else None,
        "mood": mood,
        "mood_status": _diagnostic_status(mood),
        "mood_source": mood_source if mood is not None else None,
        "tick": tick,
        "tick_status": _diagnostic_status(tick),
        "mode": mode,
        "mode_status": _diagnostic_status(mode),
        "n_concepts": n_concepts,
        "n_concepts_status": _diagnostic_status(n_concepts),
        "context_resolution": context_resolution,
        "context_resolution_status": _diagnostic_status(context_resolution),
        "phase_gate": phase_gate,
        "phase_gate_status": _diagnostic_status(phase_gate),
        "phase_gate_score": phase_gate_score,
        "phase_gate_score_status": _diagnostic_status(phase_gate_score),
        "phase_gate_tension": phase_gate_tension,
        "phase_gate_tension_status": _diagnostic_status(phase_gate_tension),
        "dialogue_act": dialogue_act,
        "dialogue_act_status": _diagnostic_status(dialogue_act),
        "dialogue_confidence": dialogue_confidence,
        "dialogue_confidence_status": _diagnostic_status(dialogue_confidence),
        "repair_requested": repair_requested,
        "repair_requested_status": _diagnostic_status(repair_requested),
    }
    diagnostic_values = (
        coherence, soul, ethics, mood, tick, mode, n_concepts,
        context_resolution, phase_gate, phase_gate_score, phase_gate_tension,
        dialogue_act, dialogue_confidence, repair_requested,
    )
    available = sum(value is not None for value in diagnostic_values)
    diagnostics["diagnostics_status"] = (
        "unavailable" if available == 0
        else "available" if available == len(diagnostic_values)
        else "partial"
    )
    return diagnostics


def _ingest_headless_turn(prompt: str, response: str, session_id: str) -> None:
    """Ingest one headless prompt+response turn into Knowledge DB (fire-and-forget)."""
    try:
        sys.path.insert(0, str(NOEMA_ROOT / "scripts"))
        from ciel_confidence_system import ingest_text
        import datetime as _dt
        tag = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        ingest_text(
            content=f"[prompt] {prompt[:1000]}\n\n[response] {response[:2000]}",
            source_type="conversation",
            title=f"headless_{tag}",
            themes=["headless", "ciel", "noema", "conversation"],
        )
    except Exception as exc:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("headless ingest skipped: %s", exc)


def request_ciel_headless(message: str, session_id: str) -> tuple[str | None, dict[str, Any], str | None]:
    """Call the canonical headless JSON socket without response fallbacks."""
    client: socket.socket | None = None
    try:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.settimeout(CHAT_BACKEND_TIMEOUT_SECONDS)
        client.connect(_P.RUN.HEADLESS_SOCK)
        client.sendall(json.dumps(
            {"text": message, "session_id": session_id},
            ensure_ascii=False,
        ).encode("utf-8"))
        client.shutdown(socket.SHUT_WR)
        chunks: list[bytes] = []
        while True:
            chunk = client.recv(8192)
            if not chunk:
                break
            chunks.append(chunk)
        if not chunks:
            return None, {}, "ciel_headless_daemon returned an empty response"
        data = json.loads(b"".join(chunks))
        if not isinstance(data, dict):
            return None, {}, "ciel_headless_daemon response must be a JSON object"
        response = data.get("response")
        frame = data.get("frame") if isinstance(data.get("frame"), dict) else {}
        return response if isinstance(response, str) else None, frame, None
    except FileNotFoundError:
        return None, {}, f"ciel_headless_daemon socket not found ({_P.RUN.HEADLESS_SOCK})"
    except (ConnectionRefusedError, socket.timeout) as exc:
        return None, {}, f"ciel_headless_daemon unreachable: {exc}"
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return None, {}, f"ciel_headless_daemon error: {exc}"
    finally:
        if client is not None:
            client.close()

# ─── Embedding cache (ładowane raz, nie per request) ───────────────────
_EMBED_CACHE: dict = {}  # {"embeddings": ndarray, "index": dict, "loaded": bool}
def _get_embeddings():
    """Lazy-load embeddings cache — pierwsze wywołanie ładuje, potem cache."""
    if _EMBED_CACHE.get("loaded"):
        return _EMBED_CACHE["embeddings"], _EMBED_CACHE["index"]
    import numpy as np
    embed_npy = EMBEDDING_CACHE_ROOT / "noema_knowledge_embeddings.npy"
    embed_json = EMBEDDING_CACHE_ROOT / "noema_knowledge_embeddings.json"
    if not embed_npy.exists() or not embed_json.exists():
        return None, None
    _EMBED_CACHE["embeddings"] = np.load(str(embed_npy))
    with open(embed_json) as f:
        _EMBED_CACHE["index"] = json.load(f)
    _EMBED_CACHE["loaded"] = True
    return _EMBED_CACHE["embeddings"], _EMBED_CACHE["index"]

# ─── TaskPlanDB singleton (was re-instantiated per-request inside do_GET,
# ~29 call sites; single-threaded HTTPServer serving requests serially made
# this correctness-safe but wasteful — moved to module level 2026-07-10) ──
_TP_DB_CACHE: dict = {"db": None}
def _get_tp():
    """Lazy-load TaskPlanDB — first call opens the connection, later calls
    reuse it. Backs /api/tasks, /api/plans, /api/lessons, /api/decisions,
    /api/skills (CRUD routes)."""
    if _TP_DB_CACHE["db"] is None:
        from ciel_geometry.taskplan_db import TaskPlanDB
        _TP_DB_CACHE["db"] = TaskPlanDB()
    return _TP_DB_CACHE["db"]

# ─── Inicjalizacja NOEMA ───────────────────────────────────────────────

def init_noema() -> dict[str, Any]:
    """Open the daemon-owned surface strictly read-only for portal observation."""
    import numpy as np

    global surface
    try:
        from ciel_geometry.noema_surface_mmap import open_surface, read_surface_state
        surface = open_surface(mode="r")
        state = read_surface_state(surface)
        tick_values = np.asarray(surface["tick"], dtype=np.uint64).ravel()
        tick = int(tick_values[0]) if tick_values.size == 1 else None
        coherence = state.get("coherence_index")
        if coherence is None:
            coherence = state.get("coherence")
        coherence_text = "unavailable" if coherence is None else f"{float(coherence):.3f}"
        print(f"[portal] surface OK: tick={tick} coh={coherence_text}")
        return state
    except Exception as e:
        print(f"[portal] surface init failed: {e}", file=sys.stderr)
        return {}


def _surface_source_timestamp() -> float | None:
    """Best available write timestamp for the mmap fields in the snapshot."""
    root = Path(PORTAL_SNAPSHOT_SOURCE)
    mtimes: list[float] = []
    for name in ("tick", "gravity"):
        try:
            path = root / name
            if path.exists():
                mtimes.append(path.stat().st_mtime)
        except OSError:
            continue
    return max(mtimes) if mtimes else None


def _unavailable_math_metric(*, source: str, now: float, error: str, source_timestamp: float | None = None) -> dict[str, Any]:
    age_s = max(0.0, now - source_timestamp) if source_timestamp is not None else None
    return {
        "status": "error" if source_timestamp is None else "degraded",
        "source": source,
        "source_timestamp": source_timestamp,
        "age_s": round(age_s, 6) if age_s is not None else None,
        "stale": source_timestamp is not None,
        "error": error,
    }


def _read_canonical_math_snapshot(now: float) -> dict[str, Any]:
    """Adapt canonical orbital/EBA reports; never reimplement their equations."""
    source = str(PORTAL_MATH_SOURCE)
    if not PORTAL_MATH_SOURCE.exists():
        unavailable = _unavailable_math_metric(source=source, now=now, error="orbital bridge report not found")
        return {"closure_eba": dict(unavailable, value=None), "r_h": dict(unavailable, raw=None, bounded_defect=None, coherence=None, n_sectors=None)}

    source_timestamp = PORTAL_MATH_SOURCE.stat().st_mtime
    age_s = max(0.0, now - source_timestamp)
    stale = age_s > PORTAL_MATH_STALE_SECONDS
    try:
        report = json.loads(PORTAL_MATH_SOURCE.read_text(encoding="utf-8"))
        bridge = report.get("bridge_metrics", {})
        state = report.get("state_manifest", {})
        raw_r_h = float(bridge["orbital_R_H"])
        n_sectors = int(bridge.get("orbital_n_sectors") or report.get("orbital_run", {}).get("n_sectors") or 0)
        if n_sectors <= 0:
            summary_path = Path((report.get("source_paths") or {}).get("summary_json", ""))
            if summary_path.is_file():
                summary = json.loads(summary_path.read_text(encoding="utf-8"))
                n_sectors = int((summary.get("final") or {}).get("n_sectors") or 0)
        if n_sectors <= 0:
            raise ValueError("canonical R_H sector count unavailable")
        from ciel_sot_agent.rh_jfunctional import rh_defect_score

        bounded = rh_defect_score({"R_H": raw_r_h, "n_sectors": n_sectors})
        eba_value = state.get("nonlocal_eba_defect_mean")
        if eba_value is None:
            eba_value = (report.get("ciel_pipeline") or {}).get("eba_defect_mean")
        status = "degraded" if stale else "ok"
        stale_error = f"canonical math source stale by {age_s:.3f}s" if stale else None
        common = {
            "status": status,
            "source": source,
            "source_timestamp": source_timestamp,
            "age_s": round(age_s, 6),
            "stale": stale,
            "error": stale_error,
        }
        return {
            "closure_eba": {
                **common,
                "status": "error" if eba_value is None else status,
                "error": "canonical EBA defect unavailable" if eba_value is None else stale_error,
                "value": None if stale or eba_value is None else float(eba_value),
                "unit": "rad",
                "meaning": "mean absolute Euler-Berry-Aharonov-Bohm loop defect; lower is better",
                "implementation": "runtime/ciel_omega/memory/holonomy.py:HolonomyCalculator.compute_eba_defect",
            },
            "r_h": {
                **common,
                "raw": None if stale else raw_r_h,
                "bounded_defect": None if stale else bounded,
                "coherence": None if stale else 1.0 - bounded,
                "n_sectors": None if stale else n_sectors,
                "unit": "holonomic_cost",
                "meaning": "raw and sector-normalized lower-is-better holonomic defect",
                "implementation": "integration/Orbital/main/metrics.py:global_coherence; src/ciel_sot_agent/rh_jfunctional.py:rh_defect_score",
            },
        }
    except Exception as exc:
        unavailable = _unavailable_math_metric(source=source, now=now, error=str(exc), source_timestamp=source_timestamp)
        return {"closure_eba": dict(unavailable, value=None), "r_h": dict(unavailable, raw=None, bounded_defect=None, coherence=None, n_sectors=None)}


def _build_portal_snapshot(now: float | None = None) -> dict[str, Any]:
    """Read shared surface fields once and attach explicit provenance/freshness."""
    import numpy as np

    observed_at = float(time.time() if now is None else now)
    source_timestamp = _surface_source_timestamp()
    base: dict[str, Any] = {
        "schema": PORTAL_SNAPSHOT_SCHEMA,
        "source": PORTAL_SNAPSHOT_SOURCE,
        "timestamp": observed_at,
        "source_timestamp": source_timestamp,
        "source_timestamp_kind": "file_mtime" if source_timestamp is not None else None,
        "age_s": None,
        "stale": True,
        "math": _read_canonical_math_snapshot(observed_at),
    }

    try:
        if surface is None:
            init_noema()
        if not surface:
            raise RuntimeError("surface unavailable")
        from ciel_geometry.noema_surface_mmap import read_surface_state

        state = read_surface_state(surface)
        tick_arr = np.asarray(surface["tick"], dtype=np.uint64).ravel()
        gravity_arr = np.asarray(surface["gravity"], dtype=np.float64).ravel()
        if tick_arr.size < 1:
            raise ValueError("surface tick is empty")
        if gravity_arr.size < 4 or not np.all(np.isfinite(gravity_arr[:4])):
            raise ValueError("surface gravity must contain four finite values")

        tick = int(tick_arr[0])
        if _PORTAL_SOURCE_CLOCK["tick"] != tick or _PORTAL_SOURCE_CLOCK["timestamp"] is None:
            _PORTAL_SOURCE_CLOCK["tick"] = tick
            _PORTAL_SOURCE_CLOCK["timestamp"] = observed_at
        source_timestamp = float(_PORTAL_SOURCE_CLOCK["timestamp"])
        age_s = max(0.0, observed_at - source_timestamp)
        stale = age_s > PORTAL_SNAPSHOT_STALE_SECONDS
        gravity = {
            "semantic_density": float(gravity_arr[0]),
            "tau_dilation": float(gravity_arr[1]),
            "mass_total": float(gravity_arr[2]),
            "unruh_power": float(gravity_arr[3]),
        }
        base.update({
            "status": "degraded" if stale else "ok",
            "snapshot_id": f"surface:{tick}:{int(observed_at * 1_000_000)}",
            "tick": tick,
            "source_timestamp": source_timestamp,
            "source_timestamp_kind": "tick_observed",
            "age_s": round(age_s, 6),
            "stale": stale,
            "gravity": gravity,
            "error": None,
            "_state": state,
        })
    except Exception as exc:
        base.update({
            "status": "error",
            "snapshot_id": f"surface:error:{int(observed_at * 1_000_000)}",
            "tick": None,
            "gravity": {
                "semantic_density": None,
                "tau_dilation": None,
                "mass_total": None,
                "unruh_power": None,
            },
            "error": str(exc),
            "_state": {},
        })
    return base


def get_portal_snapshot(*, force: bool = False, now: float | None = None) -> dict[str, Any]:
    """Return a short-lived, lock-protected snapshot for concurrent endpoints."""
    monotonic_now = time.monotonic()
    with _PORTAL_SNAPSHOT_LOCK:
        cached = _PORTAL_SNAPSHOT_CACHE.get("value")
        if not force and cached is not None and monotonic_now < _PORTAL_SNAPSHOT_CACHE["expires_at"]:
            return copy.deepcopy(cached)
        value = _build_portal_snapshot(now=now)
        _PORTAL_SNAPSHOT_CACHE["value"] = value
        _PORTAL_SNAPSHOT_CACHE["expires_at"] = time.monotonic() + PORTAL_SNAPSHOT_TTL_SECONDS
        return copy.deepcopy(value)


def portal_snapshot_contract(snapshot: dict[str, Any] | None = None) -> dict[str, Any]:
    """Public JSON contract shared verbatim by all surface endpoints."""
    snap = get_portal_snapshot() if snapshot is None else snapshot
    return {key: copy.deepcopy(snap.get(key)) for key in (
        "schema", "source", "status", "snapshot_id", "timestamp",
        "source_timestamp", "source_timestamp_kind", "age_s", "stale",
        "tick", "gravity", "math", "error",
    )}

def read_surface_value(key: str, default: Any = 0) -> Any:
    """Czyta pojedyńczą wartość z surface mmap."""
    global surface
    try:
        if surface is None:
            init_noema()
        from ciel_geometry.noema_surface_mmap import read_surface_state
        if surface:
            state = read_surface_state(surface)
            return state.get(key, default)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py quiet except scope=read_surface_value reason=pass")
        pass
    return default

def read_mmap_array(name: str) -> list | None:
    """Czyta tablicę numpy z surface mmap po nazwie pola."""
    try:
        if surface is None:
            init_noema()
        if surface and name in surface:
            arr = surface[name]
            if hasattr(arr, "tolist"):
                return arr.tolist()
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py quiet except scope=read_mmap_array reason=pass")
        pass
    return None

def _read_analog_bus() -> dict[str, Any]:
    """Czyta PhaseNav analog bus — hot/cold phi, temp, resonance, writing."""
    try:
        import numpy as np
        analog_root = SURFACE_ROOT / "analog"
        bus: dict[str, Any] = {}
        # pola float64[36]
        for name, size in [("phi_hot", 36), ("phi_cold", 36), ("writing_phi", 36)]:
            p = analog_root / name
            if p.exists() and p.stat().st_size >= size * 8:
                arr = np.memmap(p, dtype=np.float64, mode="r", shape=(size,))
                bus[name] = arr.tolist()
        # pola float64[1]
        for name in ["temp", "resonance"]:
            p = analog_root / name
            if p.exists() and p.stat().st_size >= 8:
                arr = np.memmap(p, dtype=np.float64, mode="r", shape=(1,))
                bus[name] = float(arr[0])
        # writing_meta.json
        wm = analog_root / "writing_meta.json"
        if wm.exists():
            with open(wm) as f:
                bus["writing_meta"] = json.load(f)
        # tick
        tick_p = analog_root / "tick"
        if tick_p.exists() and tick_p.stat().st_size >= 8:
            arr = np.memmap(tick_p, dtype=np.uint64, mode="r", shape=(1,))
            bus["tick"] = int(arr[0])
        return bus
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py quiet except scope=_read_analog_bus reason=return {\"error\": str(e)}")
        return {"error": str(e)}

def _read_ciel_state() -> dict[str, Any]:
    """Czyta CIEL state JSON z surface."""
    try:
        path = SURFACE_ROOT / "ciel_state.json"
        if path.exists():
            with open(path) as f:
                return json.load(f)
        return {"error": "not found"}
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py quiet except scope=_read_ciel_state reason=return {\"error\": str(e)}")
        return {"error": str(e)}

def _read_agent_hint() -> dict[str, Any]:
    """Czyta agent_hint z surface."""
    try:
        path = SURFACE_ROOT / "agent_hint"
        if path.exists():
            raw = path.read_text()
            return json.loads(raw)
        return {"error": "not found"}
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py quiet except scope=_read_agent_hint reason=return {\"error\": str(e)}")
        return {"error": str(e)}

def _read_linux_load() -> float:
    """Czyta linux_load z surface."""
    try:
        import numpy as np
        path = SURFACE_ROOT / "linux_load"
        if path.exists() and path.stat().st_size >= 8:
            arr = np.memmap(path, dtype=np.float64, mode="r", shape=(1,))
            return float(arr[0])
        return 0.0
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py quiet except scope=_read_linux_load reason=return 0.0")
        return 0.0

_SKILLS_CATALOG_CACHE: dict[str, Any] = {"mtime": 0.0, "result": None}

def _skills_catalog_count() -> dict[str, Any]:
    """Policz prawdziwy katalog skilli z SKILLS.md (SK-XXX entries).

    Cache'owane po mtime pliku — SKILLS.md rośnie rzadko, nie ma potrzeby
    parsować 750+ linii przy każdym /api/status/summary.
    """
    path = NOEMA_ROOT / "SKILLS.md"
    if not path.exists():
        return {"total": 0, "error": "SKILLS.md not found"}
    mtime = path.stat().st_mtime
    if _SKILLS_CATALOG_CACHE["mtime"] == mtime and _SKILLS_CATALOG_CACHE["result"] is not None:
        return _SKILLS_CATALOG_CACHE["result"]

    import re
    seen: set[str] = set()
    by_type: dict[str, int] = {}
    by_status: dict[str, int] = {}
    row_re = re.compile(r"^\|\s*(SK-\d+)\s*\|\s*`([^`]+)`\s*\|\s*([A-Z]+)\s*\|.*\|\s*(stable|draft|referenced|stub)\s*\|")
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = row_re.match(line)
        if not m:
            continue
        sk_id = m.group(1)
        if sk_id in seen:
            continue
        seen.add(sk_id)
        typ = m.group(3)
        status = m.group(4)
        by_type[typ] = by_type.get(typ, 0) + 1
        by_status[status] = by_status.get(status, 0) + 1

    result = {"total": len(seen), "by_type": by_type, "by_status": by_status, "source": "SKILLS.md"}
    _SKILLS_CATALOG_CACHE["mtime"] = mtime
    _SKILLS_CATALOG_CACHE["result"] = result
    return result

def _read_cards_index() -> dict[str, Any]:
    """Czyta system_map_v2.json i zwraca karty/systemy NOEMA."""
    try:
        path = Path(__file__).resolve().parent.parent / "system_map_v2.json"
        if path.exists():
            with open(path) as f:
                data = json.load(f)
            systems = data.get("systems", [])
            return {
                "total_systems": len(systems),
                "total_daemons": data.get("total_daemons", 0),
                "total_connections": data.get("total_connections", 0),
                "systems": systems,
                "version": data.get("version", ""),
                "date": data.get("date", ""),
            }
        return {"error": "system_map_v2.json not found"}
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py quiet except scope=_read_cards_index reason=return {\"error\": str(e)}")
        return {"error": str(e)}

def _read_gravity() -> dict[str, float]:
    """Czyta gravity z mmap bezpośrednio (omija read_surface_state)."""
    try:
        grav = read_mmap_array("gravity")
        if grav and len(grav) >= 4:
            return {
                "semantic_density": float(grav[0]),
                "tau_dilation": float(grav[1]),
                "mass_total": float(grav[2]),
                "unruh_power": float(grav[3]),
            }
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py quiet except scope=_read_gravity reason=pass")
        pass
    return {"semantic_density": 0, "tau_dilation": 0, "mass_total": 0, "unruh_power": 0}

def _read_tick() -> int:
    """Czyta bieżący tick z surface["tick"] (uint64[1]). Współdzielony przez
    build_bloch_payload() i build_phasenav_state_payload()."""
    try:
        import numpy as np
        if surface:
            return int(np.asarray(surface.get("tick", [0]), dtype=np.uint64).ravel()[0])
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py quiet except scope=_read_tick reason=return -1")
    return -1

def _read_operator() -> str:
    """Czyta bieżący operator PhaseNav z /dev/shm/ciel_noema/operator.
    Współdzielony przez build_bloch_payload() i build_phasenav_state_payload()."""
    try:
        op_path = SURFACE_ROOT / "operator"
        if op_path.exists():
            return op_path.read_text().strip()
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py quiet except scope=_read_operator reason=return em-dash")
    return "—"

# Keep orbital read-back under the same canonical memory root as the database
# contracts; hardcoding a former mount name made this endpoint silently stale.
_ORBITAL_STATE_PATH = Path(str(_P.STATE.ORCH_PKL)).parent / "noema_orbital_state.json"

def _read_orbital_state() -> dict[str, Any]:
    """Read the shared strict state only after receipt verification."""
    if not _ORBITAL_STATE_PATH.exists():
        raise FileNotFoundError(f"orbital state not found: {_ORBITAL_STATE_PATH}")
    return summarize_verified_orbital_state(_ORBITAL_STATE_PATH)


def _unavailable_orbital_payload(error: str) -> dict[str, Any]:
    """Stable endpoint shape for a missing or unverifiable publication.

    Scientific fields remain null.  An HTTP consumer can distinguish missing
    science from a verified degraded publication by inspecting ``publication``.
    """
    return {
        "schema": "noema.orbital.topology-state/v1",
        "status": "error",
        "structural_status": None,
        "topology_status": None,
        "orbital_status": "unavailable",
        "inference_used": False,
        "fallback_used": False,
        "systems": None,
        "nodes": None,
        "edges": None,
        "orbits": None,
        "coherence": None,
        "primaries": None,
        "binaries": None,
        "multi_orbit_3plus": None,
        "top_phases": None,
        "view_ascii": None,
        "updated_at": None,
        "source": {
            "kind": "strict_orbital_state",
            "path": str(_ORBITAL_STATE_PATH),
            "status": "unavailable",
        },
        "scientific_unavailable": {
            "orbits": error,
            "coherence": error,
        },
        "metrics": {
            "coherence": {
                "value": None,
                "unit": None,
                "status": "unavailable",
                "definition": None,
                "source_pointer": None,
                "error": error,
            },
        },
        "publication": {
            "status": "unavailable",
            "state_path": str(_ORBITAL_STATE_PATH),
            "state_sha256": None,
            "receipt_path": None,
            "receipt_checks": None,
        },
        "error": error,
    }


def build_orbital_payload() -> dict[str, Any]:
    """Return strict orbital read-back without assuming optional collections."""
    try:
        return _read_orbital_state()
    except (FileNotFoundError, OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        return _unavailable_orbital_payload(str(exc))


def _first_present(mapping: dict[str, Any], *keys: str) -> Any:
    """Return the first explicitly present non-null value; never invent zero."""
    for key in keys:
        if key in mapping and mapping[key] is not None:
            return mapping[key]
    return None


def _round_optional(value: Any, digits: int) -> float | None:
    """Round an observed scalar while preserving an unavailable value."""
    return None if value is None else round(float(value), digits)


def build_surface_status_payload(snapshot: dict[str, Any] | None = None) -> dict[str, Any]:
    """Project surface status with nulls for measurements not in the snapshot."""
    snapshot = get_portal_snapshot() if snapshot is None else snapshot
    contract = portal_snapshot_contract(snapshot)
    state = snapshot.get("_state") if isinstance(snapshot.get("_state"), dict) else {}
    math_data = snapshot.get("math") if isinstance(snapshot.get("math"), dict) else {}
    closure = math_data.get("closure_eba") if isinstance(math_data.get("closure_eba"), dict) else {}
    gravity = snapshot.get("gravity") if isinstance(snapshot.get("gravity"), dict) else {}
    return {
        **contract,
        "alive": contract.get("status") != "error",
        "coherence": _first_present(state, "coherence_index", "coherence"),
        "phi_mean": _first_present(state, "phi_mean", "R_global"),
        "phi_std": _first_present(state, "phi_std"),
        "omega_mean": _first_present(state, "omega_mean"),
        "euler_residual": closure.get("value"),
        "tau_mean": _first_present(state, "tau_mean"),
        "gravity": copy.deepcopy(gravity),
    }

def _read_state_bundle() -> dict[str, Any]:
    """Bundle analog_bus + ciel_state + agent_hint — trzy niezależne, tanie
    odczyty ze /dev/shm zawsze pobierane razem przez payload-buildery
    (build_bloch_payload(), build_phasenav_state_payload())."""
    return {
        "analog_bus": _read_analog_bus(),
        "ciel_state": _read_ciel_state(),
        "agent_hint": _read_agent_hint(),
    }

def build_bloch_payload() -> dict[str, Any]:
    """Full 36D NOEMA state jako punkty na sferze Blocha — GRAFICZNY tryb
    kodowania PhaseNav (wektoryzacja wizualna), równorzędny wobec trybu
    tekstowo-semantycznego, nie ozdobnik. Backing /api/bloch. Skille: pełna
    teoria projekcji Blocha w `.claude/skills/phasenav-solver/`, pokrewny
    render dysku Poincarégo w `.claude/skills/poincare-disk/` i
    `.claude/skills/renderer-phasedisk/` (ta sama idea — punkt fazowy na
    rozmaitości — inna geometria docelowa).

    Używa helperów: _read_tick(), _read_operator(), _read_state_bundle()
    (analog_bus/ciel_state/agent_hint), _read_linux_load().

    Zwraca:
    - 36 nodes (phi, omega, tau, sensor, R_geom, psi_geom, Z_geom, dphi/dt)
    - 36×36 coupling matrix g (top 72 edges)
    - 6 flavor slots, 4 gravity, 7 holonomy
    - Analog bus (phi_hot, phi_cold, writing_phi)
    - CIEL state, agent_hint, linux_load
    - Operator PhaseNav, tick, metadata
    """
    import numpy as np
    from ciel_geometry.phasenav.operator_algebra import ALL_OPERATOR_IDS, VECTOR_COMPONENTS

    if surface is None:
        init_noema()
    if not surface:
        return {"status": "error", "error": "surface unavailable"}

    # ── 1. Wczytaj wszystkie surface arrays ──
    def _read_1d(name: str, n: int = 36) -> np.ndarray:
        try:
            arr = np.asarray(surface[name], dtype=np.float64).ravel()
            if len(arr) >= n:
                return arr[:n]
            return np.pad(arr, (0, n - len(arr)))
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py quiet except scope=build_bloch_payload._read_1d reason=return np.zeros(n, dtype=np.float64)")
            return np.zeros(n, dtype=np.float64)

    n = 36
    phi = _read_1d("phi", n)
    omega = _read_1d("omega", n)
    tau = _read_1d("tau", n)
    sensor = _read_1d("sensor_raw", n)
    r_geom = _read_1d("R_geom", n)
    psi_geom = _read_1d("psi_geom", n)
    Z_geom = _read_1d("Z_geom", n)

    # G (36×36)
    try:
        g = np.asarray(surface["g"], dtype=np.float64)[:n, :n]
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py quiet except scope=build_bloch_payload reason=assign_fallback")
        g = np.zeros((n, n), dtype=np.float64)

    # Flavor (6), Gravity (4), Holonomy (7)
    flavor = _read_1d("flavor", 6)
    gravity_arr = _read_1d("gravity", 4)
    holonomy_arr = _read_1d("holonomy", 7)

    # Tick
    tick_val = _read_tick()

    # ── 2. Wektoryzowane obliczenia Bloch (numpy, zero pętli) ──
    phase_diff = phi[None, :] - phi[:, None]                   # (36,36)
    coupling_flow = np.sum(g * np.sin(phase_diff), axis=1) / max(1, n)  # (36,)

    info_energy = np.abs(omega) + np.abs(coupling_flow) + 0.15 * np.abs(sensor)
    max_energy = max(float(np.max(info_energy)), 1e-12)
    energy_norm = np.clip(info_energy / max_energy, 0.0, 1.0)
    tau_norm = np.clip(tau, 0.0, 1.0)
    sensor_norm = np.tanh(np.abs(sensor))

    # Pozycje na sferze Blocha — wszystko wektorowo
    z = np.clip((tau_norm - 0.5) * 1.2 + np.tanh(coupling_flow) * 0.45 + sensor_norm * 0.20, -0.98, 0.98)
    radius_xy = np.sqrt(np.maximum(0.0, 1.0 - z * z))
    x = radius_xy * np.cos(phi)
    y = radius_xy * np.sin(phi)

    # Flow vectors (dφ/dt)
    dphi = omega + coupling_flow
    vx = -np.sin(phi) * dphi * 0.10
    vy = np.cos(phi) * dphi * 0.10
    vz = np.tanh(coupling_flow) * 0.08

    # ── 3. Krawędzie (top 72 z g) ──
    abs_g = np.abs(g.copy())
    np.fill_diagonal(abs_g, 0.0)
    flat_idx = np.argsort(abs_g.ravel())[::-1]
    edges = []
    seen: set[tuple[int, int]] = set()
    for idx in flat_idx:
        a = int(idx // n)
        b = int(idx % n)
        if a == b or (b, a) in seen:
            continue
        w = float(g[a, b])
        if abs(w) <= 1e-9:
            continue
        seen.add((a, b))
        edges.append({"from": a, "to": b, "weight": round(w, 6), "abs_weight": round(abs(w), 6)})
        if len(edges) >= 72:
            break

    # ── 4. Punkty + wektory + program (36 iteracji — OK dla 36, strukturalnie potrzebne) ──
    supergroups = ["M0_ID", "M1_AGENT", "M2_MEMORY", "M3_SEM", "M4_LOGIC", "M5_AFFECT", "M6_REL", "M7_TIME", "M8_META"]
    colors = ["#00d4ff", "#8844ff", "#44ff88", "#ffb347", "#ff4466", "#ff88cc", "#44ddff", "#aaff44", "#ffffff"]
    ch_indices = np.arange(n) // 4

    points = []
    vectors_ret = []
    program = []
    for i in range(n):
        sg = int(ch_indices[i])
        op = ALL_OPERATOR_IDS[i] if i < len(ALL_OPERATOR_IDS) else f"OP_{i}"
        comp = VECTOR_COMPONENTS[i] if i < len(VECTOR_COMPONENTS) else "v"

        points.append({
            "idx": i, "id": f"φ[{i:02d}]", "operator": op, "component": comp,
            "supergroup": supergroups[min(sg, len(supergroups)-1)], "ch": sg,
            "color": colors[min(sg, len(colors)-1)],
            "x": round(float(x[i]), 6), "y": round(float(y[i]), 6), "z": round(float(z[i]), 6),
            "phi": round(float(phi[i]), 6), "omega": round(float(omega[i]), 6),
            "tau": round(float(tau[i]), 6), "sensor": round(float(sensor[i]), 6),
            "coupling_flow": round(float(coupling_flow[i]), 6),
            "energy": round(float(energy_norm[i]), 6),
            "R": round(float(max(0.12, energy_norm[i])), 6),
            "r_geom": round(float(r_geom[i]), 6), "psi_geom": round(float(psi_geom[i]), 6),
            "Z_geom": round(float(Z_geom[i]), 6),
        })
        vectors_ret.append({
            "from": i,
            "x": round(float(vx[i]), 6), "y": round(float(vy[i]), 6), "z": round(float(vz[i]), 6),
            "magnitude": round(float(abs(dphi[i])), 6),
            "meaning": "dφ/dt = ω + Σ gᵢⱼ sin(φⱼ-φᵢ)",
        })
        program.append({
            "step": i, "op": op, "component": comp,
            "vector": [round(float(x[i]), 6), round(float(y[i]), 6), round(float(z[i]), 6)],
            "flow": [round(float(vx[i]), 6), round(float(vy[i]), 6), round(float(vz[i]), 6)],
            "exec": "PROJECT_BLOCH ∘ FLOW_FIELD ∘ PHASENAV_OPERATOR",
        })

    # ── 5-7. Analog bus + CIEL state + agent hint ──
    _bundle = _read_state_bundle()
    analog = _bundle["analog_bus"]
    ciel_state = _bundle["ciel_state"]
    agent_hint = _bundle["agent_hint"]

    # ── 8. Linux load ──
    linux_load_val = _read_linux_load()

    # ── 9. Operator ──
    operator_val = _read_operator()

    # ── 10. Składanie wyniku ──
    return {
        "status": "ok",
        "source": "NOEMA surface mmap (all 12 arrays) + analog bus + CIEL state",
        "representation": "PhaseNav vector program → Bloch information dynamics",
        "timestamp": time.time(),
        "tick": tick_val,
        "n": n, "dimensions": 36,
        "operator": operator_val,
        "linux_load": linux_load_val,

        # Koherencja — z CIEL state, z R_geom, z flavor[0]
        "coherence": {
            "r_global": float(np.mean(r_geom)) if r_geom.size > 0 else 0,
            "ciel_coherence_index": ciel_state.get("coherence_index", 0),
            "flavor_coherence": float(flavor[0]) if len(flavor) > 0 else 0,
        },
        "omega_mean": round(float(np.mean(omega)), 6),
        "tau_mean": round(float(np.mean(tau)), 6),
        "info_energy_mean": round(float(np.mean(energy_norm)), 6),
        "flow_rms": round(float(np.sqrt(np.mean(dphi * dphi))), 6),
        "sensor_mean": round(float(np.mean(sensor)), 6),
        "phi_var": round(float(np.var(phi)), 6),

        # 36 węzłów
        "points": points,
        # 72 krawędzie coupling
        "edges": edges,
        # Flow vectors
        "vectors": vectors_ret,
        # Program PhaseNav
        "program": program,

        # Dodatkowe atrybuty (NOWE — brakowało wcześniej)
        "flavor": {
            "coherence": float(flavor[0]) if len(flavor) > 0 else 0,
            "mem_pressure": float(flavor[1]) if len(flavor) > 1 else 0,
            "io_pressure": float(flavor[2]) if len(flavor) > 2 else 0,
            "mood": float(flavor[3]) if len(flavor) > 3 else 0,
            "entropy": float(flavor[4]) if len(flavor) > 4 else 0,
            "mode": float(flavor[5]) if len(flavor) > 5 else 0,
            "raw_vector": flavor.tolist(),
        },
        "gravity": {
            "semantic_density": float(gravity_arr[0]) if len(gravity_arr) > 0 else 0,
            "tau_dilation": float(gravity_arr[1]) if len(gravity_arr) > 1 else 0,
            "mass_total": float(gravity_arr[2]) if len(gravity_arr) > 2 else 0,
            "unruh_power": float(gravity_arr[3]) if len(gravity_arr) > 3 else 0,
            "raw_vector": gravity_arr.tolist(),
        },
        "holonomy": {
            "mean_conn": float(holonomy_arr[0]) if len(holonomy_arr) > 0 else 0,
            "gauge_rank": float(holonomy_arr[1]) if len(holonomy_arr) > 1 else 0,
            "closure_score": float(holonomy_arr[2]) if len(holonomy_arr) > 2 else 0,
            "surface_gamma": float(holonomy_arr[3]) if len(holonomy_arr) > 3 else 0,
            "max_conn": float(holonomy_arr[4]) if len(holonomy_arr) > 4 else 0,
            "winding": float(holonomy_arr[5]) if len(holonomy_arr) > 5 else 0,
            "curvature": float(holonomy_arr[6]) if len(holonomy_arr) > 6 else 0,
            "raw_vector": holonomy_arr.tolist(),
        },

        # Analog bus
        "analog_bus": analog,

        # CIEL state
        "ciel_state": ciel_state,

        # Agent hint
        "agent_hint": agent_hint,

        # Linux load
        "linux_load_detail": {"load": linux_load_val},

        # Etykieta
        "status_label": "REAL",
        "attributes_labels": ["phi","omega","tau","sensor","R_geom","psi_geom","Z_geom",
                               "flavor","gravity","holonomy","g","analog_bus","ciel_state"],
    }


def build_phasenav_graphics_payload(query: str = "NOEMA", scene_name: str = "surface") -> dict[str, Any]:
    """Multi-scene PhaseNav graphics bundle (relational/memory/operator maps)
    — GRAFICZNY tryb kodowania PhaseNav, na równi z trybem tekstowo-
    semantycznym (nie ozdobnik). Backing /api/phasenav/graphics. Deleguje
    faktyczną kompozycję scen do ciel_geometry.phasenav.graphics
    .build_phasenav_graphics_bundle() — ta funkcja jest tylko cienkim
    JSON-adapterem nad nią (wybór scene_name, fallback do "surface", error
    envelope). Crossref: `.claude/skills/phasenav-solver/` (teoria wektorów
    fazowych), `.claude/skills/poincare-disk/` i
    `.claude/skills/renderer-phasedisk/` (pokrewne wizualizacje na innych
    rozmaitościach). Zobacz też build_bloch_payload() (sfera Blocha,
    /api/bloch) i build_phasenav_state_payload() (lekki stan bez grafiki,
    /api/phasenav/state) — trzy różne payloady z tego samego surface."""
    try:
        from ciel_geometry.phasenav.graphics import build_phasenav_graphics_bundle
        bundle = build_phasenav_graphics_bundle(query=query, surface=surface)
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py quiet except scope=build_phasenav_graphics_payload reason=return error")
        return {"status": "error", "error": str(e), "query": query, "scene_name": scene_name}

    scenes = bundle.get("scenes", {})
    selected = scenes.get(scene_name) or scenes.get("surface") or {}
    return {
        "status": "ok",
        "source": "PhaseNav graphics composer",
        "query": bundle.get("query", query),
        "surface": bundle.get("surface", {}),
        "scene_name": scene_name,
        "scene_counts": bundle.get("scene_counts", {}),
        "scenes": scenes,
        "scene": selected,
    }


def cached_phasenav_graphics_payload(query: str, scene_name: str) -> dict[str, Any]:
    """Keep large graphics payload byte-stable between normal UI polls."""
    key = (query, scene_name)
    now = time.monotonic()
    with _PHASENAV_GRAPHICS_CACHE_LOCK:
        cached = _PHASENAV_GRAPHICS_CACHE.get(key)
        if cached and cached[0] > now:
            return copy.deepcopy(cached[1])
        payload = build_phasenav_graphics_payload(query=query, scene_name=scene_name)
        _PHASENAV_GRAPHICS_CACHE[key] = (now + 30.0, payload)
        return copy.deepcopy(payload)

def build_phasenav_state_payload() -> dict[str, Any]:
    """Lightweight current PhaseNav state — operator, tick, analog bus, CIEL
    state, agent hint. Backing /api/phasenav/state. Referenced by the portal
    manifest (phasenav card sources) since 2026-06 but never had a route
    until 2026-07-09; deliberately reuses the same helpers as
    build_bloch_payload() (_read_tick, _read_operator, _read_state_bundle)
    instead of that function's full 36x36 vectorized geometry, since callers
    here only need the operator/tick/bus summary, not the coupling matrix.
    See also build_phasenav_graphics_payload() (/api/phasenav/graphics) for
    the graphical-encoding sibling route."""
    try:
        if surface is None:
            init_noema()
        tick_val = _read_tick()
        operator_val = _read_operator()
        _bundle = _read_state_bundle()
        return {
            "status": "ok",
            "source": "NOEMA surface tick/operator + analog bus + CIEL state",
            "timestamp": time.time(),
            "tick": tick_val,
            "operator": operator_val,
            "analog_bus": _bundle["analog_bus"],
            "ciel_state": _bundle["ciel_state"],
            "agent_hint": _bundle["agent_hint"],
        }
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py quiet except scope=build_phasenav_state_payload reason=return error")
        return {"status": "error", "error": str(e)}

def _metric_entry(
    key: str,
    value: Any,
    *,
    label: str,
    unit: str = "",
    desc: str = "",
    source: str = "surface",
    group: str = "surface",
    direction: str = "neutral",
    good_range: list[float] | None = None,
    warn_range: list[float] | None = None,
    provenance: dict[str, Any] | None = None,
    status: str | None = None,
    error: str | None = None,
    source_timestamp: Any = None,
    receipt: dict[str, Any] | None = None,
) -> dict[str, Any]:
    rendered = float(value) if isinstance(value, (int, float)) else value
    return {
        "key": key,
        "label": label,
        "unit": unit,
        "desc": desc,
        "source": source,
        "group": group,
        "value": rendered,
        "direction": direction,
        "good_range": good_range,
        "warn_range": warn_range,
        "status": status or ("unavailable" if rendered is None else "available"),
        "error": error,
        "source_timestamp": source_timestamp,
        "receipt": copy.deepcopy(receipt),
        "provenance": provenance or {"source": source},
    }


def build_metrics_catalog(snapshot: dict[str, Any] | None = None) -> dict[str, Any]:
    """Kanoniczny katalog metryk wykorzystywany przez dashboard."""
    snapshot = get_portal_snapshot() if snapshot is None else snapshot
    contract = portal_snapshot_contract(snapshot)
    state = snapshot.get("_state") if isinstance(snapshot.get("_state"), dict) else {}
    gravity = snapshot.get("gravity") if isinstance(snapshot.get("gravity"), dict) else {}
    math_data = snapshot.get("math") if isinstance(snapshot.get("math"), dict) else {}
    closure_eba = math_data.get("closure_eba") if isinstance(math_data.get("closure_eba"), dict) else {}
    r_h = math_data.get("r_h") if isinstance(math_data.get("r_h"), dict) else {}
    orbital = build_orbital_payload()
    orbital_metrics = orbital.get("metrics") if isinstance(orbital.get("metrics"), dict) else {}
    orbital_coherence = orbital_metrics.get("coherence") if isinstance(orbital_metrics.get("coherence"), dict) else {}
    orbital_source = orbital.get("source") if isinstance(orbital.get("source"), dict) else {}
    orbital_publication = orbital.get("publication") if isinstance(orbital.get("publication"), dict) else {}
    orbital_unavailable = orbital.get("scientific_unavailable") if isinstance(orbital.get("scientific_unavailable"), dict) else {}
    daemons = scan_registry()
    active_daemons = sum(1 for d in daemons if d.get("alive"))
    portal_uptime_s = round(time.time() - start_time, 1) if start_time else 0.0
    observed_status = "stale" if contract.get("stale") else ("available" if contract.get("status") == "ok" else "error")
    observed_provenance = {
        "kind": "observed",
        "source_path": contract.get("source"),
        "source_timestamp_kind": contract.get("source_timestamp_kind"),
        "snapshot_id": contract.get("snapshot_id"),
        "inference_used": False,
        "fallback_used": False,
    }

    metrics = [
        _metric_entry("tick", snapshot.get("tick"), label="Tick", unit="tick",
                      desc="Bieżący cykl powierzchni", source="surface", group="surface", status=observed_status, provenance={**observed_provenance, "source_field": "tick"}),
        _metric_entry("coherence", _first_present(state, "coherence", "coherence_index"),
                      label="Koherencja", desc="Globalna synchronizacja układu", source="surface", group="surface",
                      direction="higher_better", good_range=[0.8, 1.0], warn_range=[0.5, 0.8], status=observed_status, provenance={**observed_provenance, "source_field": "coherence_index"}),
        _metric_entry("eba_closure_residual", closure_eba.get("value"),
                      label="EBA closure residual", unit="rad", desc="Kanoniczny defekt pętli EBA (niżej lepiej)", source=closure_eba.get("source", "unavailable"), group="surface",
                      direction="lower_better", good_range=[0.0, 0.1], warn_range=[0.1, 0.15], provenance={"source": closure_eba.get("source", "unavailable"), "implementation": closure_eba.get("implementation")}, status=closure_eba.get("status"), error=closure_eba.get("error"), source_timestamp=closure_eba.get("source_timestamp")),
        _metric_entry("R_H_raw", r_h.get("raw"),
                      label="R_H raw", unit="holonomic_cost", desc="Surowy defekt holonomiczny (niżej lepiej)", source=r_h.get("source", "unavailable"), group="surface",
                      direction="lower_better", provenance={"source": r_h.get("source", "unavailable"), "implementation": r_h.get("implementation")}, status=r_h.get("status"), error=r_h.get("error"), source_timestamp=r_h.get("source_timestamp")),
        _metric_entry("R_H_bounded_defect", r_h.get("bounded_defect"),
                      label="R_H bounded", unit="normalized_defect", desc="R_H/(N+R_H)", source=r_h.get("source", "unavailable"), group="surface",
                      direction="lower_better", good_range=[0.0, 0.3], warn_range=[0.3, 0.7], provenance={"source": r_h.get("source", "unavailable"), "implementation": r_h.get("implementation")}, status=r_h.get("status"), error=r_h.get("error"), source_timestamp=r_h.get("source_timestamp")),
        _metric_entry("R_H_coherence", r_h.get("coherence"),
                      label="R_H coherence", unit="normalized_score", desc="1 - bounded defect", source=r_h.get("source", "unavailable"), group="surface",
                      direction="higher_better", good_range=[0.7, 1.0], warn_range=[0.3, 0.7], provenance={"source": r_h.get("source", "unavailable"), "implementation": r_h.get("implementation")}, status=r_h.get("status"), error=r_h.get("error"), source_timestamp=r_h.get("source_timestamp")),
        _metric_entry("R_H_n_sectors", r_h.get("n_sectors"),
                      label="R_H N", unit="count", desc="Liczba sektorów użyta do normalizacji R_H", source=r_h.get("source", "unavailable"), group="surface", status=r_h.get("status"), error=r_h.get("error"), source_timestamp=r_h.get("source_timestamp")),
        _metric_entry("orbital_coherence", orbital.get("coherence"),
                      label="Koherencja orbitalna", unit=orbital_coherence.get("unit") or "", desc=orbital_coherence.get("definition") or "Koherencja z receipt-verified strict orbital publication", source=orbital_source.get("path", str(_ORBITAL_STATE_PATH)), group="orbital", direction="neutral", status=orbital_coherence.get("status") or "unavailable", error=orbital_coherence.get("error") or orbital_unavailable.get("coherence") or orbital.get("error"), source_timestamp=orbital.get("updated_at"), receipt=orbital_publication),
        _metric_entry("omega_mean", state.get("omega_mean"),
                      label="ω̄", unit="rad/s", desc="Średnia częstotliwość oscylatorów", source="surface", group="surface", status=observed_status, provenance={**observed_provenance, "source_field": "omega_mean"}),
        _metric_entry("tau_mean", state.get("tau_mean"),
                      label="τ̄", unit="s", desc="Średni czas życia / opóźnienie pamięci", source="surface", group="surface", status=observed_status, provenance={**observed_provenance, "source_field": "tau_mean"}),
        _metric_entry("semantic_density", gravity.get("semantic_density"),
                      label="ρ_sem", desc="Gęstość semantyczna powierzchni", source="surface", group="surface", status=observed_status, provenance={**observed_provenance, "source_field": "gravity[0]"}),
        _metric_entry("tau_dilation", gravity.get("tau_dilation"),
                      label="γ_τ", desc="Dylatacja czasu lokalnego", source="surface", group="surface", status=observed_status, provenance={**observed_provenance, "source_field": "gravity[1]"}),
        _metric_entry("mass_total", gravity.get("mass_total"),
                      label="Masa", desc="Całkowita masa semantyczna", source="surface", group="surface", status=observed_status, provenance={**observed_provenance, "source_field": "gravity[2]"}),
        _metric_entry("unruh_power", gravity.get("unruh_power"),
                      label="Unruh", desc="Moc Unruha / napór przyspieszeń", source="surface", group="surface", status=observed_status, provenance={**observed_provenance, "source_field": "gravity[3]"}),
        _metric_entry("mood", _first_present(state, "mood", "mood_normalized"),
                      label="Nastrój", desc="Kanał afektywny odczytany ze stanu powierzchni; nie utożsamiać z mood_scalar CIEL", source="surface", group="ciel", status=observed_status, provenance={**observed_provenance, "source_field": "ciel_state.mood"}),
        _metric_entry("ethical_score", state.get("ethical_score"),
                      label="Etyka", desc="Wynik wyprowadzony przez EthicalEngine; nie jest pomiarem fizycznym", source="ciel", group="ciel", status="derived" if state.get("ethical_score") is not None else "unavailable", provenance={"kind": "derived", "source": "EthicalEngine.evaluate", "formula": "tanh(wave_coherence * CQCL.emotional_intensity / NOEMA.gravity[2])", "fallback_used": False}),
        _metric_entry("soul_invariant", state.get("soul_invariant"),
                      label="Soul invariant", desc="Niezmiennik wyprowadzony przez SoulInvariant", source="ciel", group="ciel", status="derived" if state.get("soul_invariant") is not None else "unavailable", provenance={"kind": "derived", "source": "SoulInvariant.compute", "fallback_used": False}),
        _metric_entry("daemon_total", len(daemons),
                      label="Daemony", unit="count", desc="Liczba wykrytych daemonów", source="registry", group="system"),
        _metric_entry("daemon_active", active_daemons,
                      label="Aktywne daemony", unit="count", desc="Daemony żywe w registry", source="registry", group="system"),
        _metric_entry("portal_uptime_s", portal_uptime_s,
                      label="Uptime portalu", unit="s", desc="Czas pracy portalu", source="portal", group="portal"),
    ]

    groups: dict[str, list[dict[str, Any]]] = {}
    for metric in metrics:
        metric_source_timestamp = metric.get("source_timestamp")
        if metric_source_timestamp is None and metric["source"] in {"surface", "ciel"}:
            metric_source_timestamp = contract["source_timestamp"]
        metric["provenance"] = {
            **metric["provenance"],
            "snapshot_id": contract["snapshot_id"],
            "schema": contract["schema"],
            "source_timestamp": metric_source_timestamp,
        }
        groups.setdefault(metric["group"], []).append(metric)

    return {
        "status": contract["status"],
        "timestamp": contract["timestamp"],
        "surface_snapshot": contract,
        "metrics": metrics,
        "groups": groups,
        "summary": {
            "tick": snapshot.get("tick"),
            "gravity": copy.deepcopy(gravity),
            "coherence": _first_present(state, "coherence", "coherence_index"),
            "active_daemons": active_daemons,
            "total_daemons": len(daemons),
            "orbital": {
                "status": orbital.get("status"),
                "orbital_status": orbital.get("orbital_status"),
                "coherence": orbital.get("coherence"),
                "source": copy.deepcopy(orbital.get("source")),
                "publication": copy.deepcopy(orbital.get("publication")),
                "error": orbital.get("error") or orbital_unavailable.get("coherence"),
            },
        },
    }


def _load_system_map() -> dict[str, Any]:
    """Read the declared-system source without making runtime claims."""
    try:
        payload = json.loads(SYSTEM_MAP_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"systems": []}
    return payload if isinstance(payload, dict) else {"systems": []}


def build_portal_system_catalog(*, observed_at: str | None = None) -> dict[str, Any]:
    """Canonical logical-system catalogue plus every observed process."""
    return build_contract_system_catalog(
        _load_system_map(),
        scan_registry(),
        source="noema_registry",
        observed_at=observed_at,
    )


def build_portal_metric_catalog(snapshot: dict[str, Any] | None = None) -> dict[str, Any]:
    """Metric contract with explicit unavailable values; never substitute zero."""
    snapshot = get_portal_snapshot() if snapshot is None else snapshot
    contract = portal_snapshot_contract(snapshot)
    state = snapshot.get("_state") if isinstance(snapshot.get("_state"), dict) else {}
    # ethical_score lives in ciel_state.json, not in _state — read it directly
    _ciel_state_direct = _read_ciel_state()
    if isinstance(_ciel_state_direct, dict) and "ethical_score" in _ciel_state_direct:
        state = {**state, "ethical_score": _ciel_state_direct["ethical_score"]}
    gravity = snapshot.get("gravity") if isinstance(snapshot.get("gravity"), dict) else {}
    math_data = snapshot.get("math") if isinstance(snapshot.get("math"), dict) else {}
    eba = math_data.get("closure_eba") if isinstance(math_data.get("closure_eba"), dict) else {}
    rh = math_data.get("r_h") if isinstance(math_data.get("r_h"), dict) else {}
    orbital = build_orbital_payload()
    orbital_metrics = orbital.get("metrics") if isinstance(orbital.get("metrics"), dict) else {}
    orbital_coherence = orbital_metrics.get("coherence") if isinstance(orbital_metrics.get("coherence"), dict) else {}
    orbital_source = orbital.get("source") if isinstance(orbital.get("source"), dict) else {}
    orbital_publication = orbital.get("publication") if isinstance(orbital.get("publication"), dict) else {}
    orbital_unavailable = orbital.get("scientific_unavailable") if isinstance(orbital.get("scientific_unavailable"), dict) else {}
    observed_at = contract.get("timestamp")
    source_timestamp = contract.get("source_timestamp")
    surface_status = "stale" if contract.get("stale") else ("available" if contract.get("status") == "ok" else "error")
    surface_provenance = {
        "kind": "observed",
        "source_path": contract.get("source"),
        "source_timestamp_kind": contract.get("source_timestamp_kind"),
        "snapshot_id": contract.get("snapshot_id"),
        "inference_used": False,
        "fallback_used": False,
    }
    state_provenance = {
        **surface_provenance,
        "source_path": "/dev/shm/ciel_noema/ciel_state.json",
        "source_field": "ciel_state",
    }
    raw_metrics = [
        {"key": "tick", "label": "Tick", "value": snapshot.get("tick"), "unit": "tick", "source": "surface", "system_id": "noema:surface:mmap", "definition": "Bieżący tick powierzchni.", "status": surface_status, "provenance": {**surface_provenance, "source_field": "tick"}},
        {"key": "coherence", "label": "Koherencja", "value": state.get("coherence", state.get("coherence_index")), "source": "surface", "system_id": "noema:surface:mmap", "direction": "higher_better", "thresholds": {"good": None, "warning": None}, "definition": "Moduł średniej fazy z aktualnego snapshotu powierzchni.", "status": surface_status, "provenance": {**surface_provenance, "source_field": "coherence_index"}},
        {"key": "eba_closure_residual", "label": "EBA closure residual", "value": eba.get("value"), "unit": "rad", "source": eba.get("source", "unavailable"), "source_timestamp": eba.get("source_timestamp"), "system_id": "noema:surface:mmap", "direction": "lower_better", "formalism": "EBA", "definition": eba.get("meaning"), "status": eba.get("status"), "error": eba.get("error"), "provenance": {"kind": "derived_canonical", "implementation": eba.get("implementation"), "fallback_used": False}},
        {"key": "r_h_raw", "label": "R_H raw", "value": rh.get("raw"), "unit": "holonomic_cost", "source": rh.get("source", "unavailable"), "source_timestamp": rh.get("source_timestamp"), "system_id": "noema:surface:mmap", "direction": "lower_better", "formalism": "R_H", "definition": rh.get("meaning"), "status": rh.get("status"), "error": rh.get("error"), "provenance": {"kind": "derived_canonical", "implementation": rh.get("implementation"), "fallback_used": False}},
        {"key": "r_h_coherence", "label": "R_H coherence", "value": rh.get("coherence"), "unit": "normalized_score", "source": rh.get("source", "unavailable"), "source_timestamp": rh.get("source_timestamp"), "system_id": "noema:surface:mmap", "direction": "higher_better", "formalism": "R_H", "definition": "1 - R_H/(N+R_H); publikuj tylko razem z kanonicznym R_H i N.", "status": rh.get("status"), "error": rh.get("error"), "provenance": {"kind": "derived_canonical", "implementation": rh.get("implementation"), "fallback_used": False}},
        {"key": "orbital_coherence", "label": "Koherencja orbitalna", "value": orbital.get("coherence"), "unit": orbital_coherence.get("unit"), "source": orbital_source.get("path", str(_ORBITAL_STATE_PATH)), "source_timestamp": orbital.get("updated_at"), "system_id": "noema:orbital:strict", "direction": "neutral", "formalism": "strict_orbital_topology", "status": orbital_coherence.get("status") or "unavailable", "error": orbital_coherence.get("error") or orbital_unavailable.get("coherence") or orbital.get("error"), "receipt": orbital_publication, "provenance": {"inference_used": orbital.get("inference_used"), "fallback_used": orbital.get("fallback_used"), "publication_status": orbital_publication.get("status")}},
        {"key": "semantic_density", "label": "ρ_sem", "value": gravity.get("semantic_density"), "source": "surface", "system_id": "noema:surface:mmap", "definition": "Kanał gravity[0] odczytany z powierzchni NOEMA.", "status": surface_status, "provenance": {**surface_provenance, "source_field": "gravity[0]"}},
        {"key": "tau_dilation", "label": "γ_τ", "value": gravity.get("tau_dilation"), "source": "surface", "system_id": "noema:surface:mmap", "definition": "Kanał gravity[1] odczytany z powierzchni NOEMA.", "status": surface_status, "provenance": {**surface_provenance, "source_field": "gravity[1]"}},
        {"key": "mass_total", "label": "Masa semantyczna", "value": gravity.get("mass_total"), "source": "surface", "system_id": "noema:surface:mmap", "definition": "Kanał gravity[2] odczytany z powierzchni NOEMA; używany przez etykę CIEL.", "status": surface_status, "provenance": {**surface_provenance, "source_field": "gravity[2]"}},
        {"key": "unruh_power", "label": "Moc Unruha", "value": gravity.get("unruh_power"), "source": "surface", "system_id": "noema:surface:mmap", "definition": "Kanał gravity[3] odczytany z powierzchni NOEMA.", "status": surface_status, "provenance": {**surface_provenance, "source_field": "gravity[3]"}},
        {"key": "ethical_score", "label": "Etyka CIEL", "value": state.get("ethical_score"), "source": "ciel", "system_id": "noema:ciel_hub:001", "direction": "higher_better", "definition": "Wartość wyprowadzona przez EthicalEngine z koherencji symulacji, intencji CQCL i masy gravity[2]; nie jest pomiarem fizycznym.", "status": "derived" if state.get("ethical_score") is not None else "unavailable", "provenance": {**state_provenance, "kind": "derived", "formula": "tanh(coherence * intention / gravity[2])", "inputs": ["CQCL.emotional_intensity", "wave_simulation.coherence", "NOEMA.gravity[2]"], "fallback_used": False}},
        {"key": "soul_invariant", "label": "Soul invariant", "value": state.get("soul_invariant"), "source": "ciel", "system_id": "noema:ciel_hub:001", "direction": "higher_better", "definition": "Wartość stanu CIEL z pliku stanu; zero pozostaje zero tylko jeśli pole jest jawnie opublikowane.", "status": "derived" if state.get("soul_invariant") is not None else "unavailable", "provenance": {**state_provenance, "kind": "derived", "formula": "SoulInvariant.compute(intention_vector)", "inputs": ["CielEngine.intention_vector"], "fallback_used": False}},
    ]
    metrics = [
        normalize_metric(
            {
                **raw,
                "source_timestamp": raw.get("source_timestamp", source_timestamp),
            },
            observed_at=observed_at,
        )
        for raw in raw_metrics
    ]
    by_system: dict[str, list[dict[str, Any]]] = {}
    for metric in metrics:
        by_system.setdefault(str(metric.get("system_id") or "unassigned"), []).append(metric)
    return {
        "contract": "noema.metric-catalog/v1",
        "observed_at": observed_at,
        "snapshot": contract,
        "orbital": {
            "status": orbital.get("status"),
            "orbital_status": orbital.get("orbital_status"),
            "source": copy.deepcopy(orbital.get("source")),
            "publication": copy.deepcopy(orbital.get("publication")),
            "error": orbital.get("error"),
        },
        "metrics": metrics,
        "by_system": by_system,
    }


def operation_inventory() -> dict[str, Any]:
    return {
        "contract": "noema.operations/v1",
        "execution_enabled": OPERATIONS_ENABLED,
        "required_cycle": ["plan", "preview", "capability_confirmation", "execute", "read_back", "receipt"],
        "operations": [
            {"operation_id": key, **value, "status": "available" if OPERATIONS_ENABLED else "execution_disabled"}
            for key, value in _OPERATION_ALLOWLIST.items()
        ],
        "receipts": list(_OPERATION_RECEIPTS[-20:]),
    }


def plan_operation(body: dict[str, Any]) -> tuple[dict[str, Any], int]:
    operation_id = str(body.get("operation_id") or "")
    idempotency_key = str(body.get("idempotency_key") or "")
    if operation_id not in _OPERATION_ALLOWLIST:
        return {"status": "error", "error": "operation is not allowlisted"}, 400
    if len(idempotency_key) < 16:
        return {"status": "error", "error": "idempotency_key must contain at least 16 characters"}, 400
    plan_id = hashlib.sha256(f"{operation_id}:{idempotency_key}".encode()).hexdigest()[:24]
    plan = {
        "plan_id": plan_id, "operation_id": operation_id, "idempotency_key": idempotency_key,
        "created_at": time.time(), "status": "planned", "effect_preview": {"target": body.get("target"), "parameters": body.get("parameters", {})},
        "risk": _OPERATION_ALLOWLIST[operation_id]["risk"], "rollback": _OPERATION_ALLOWLIST[operation_id]["rollback"],
    }
    with _OPERATION_LOCK:
        _OPERATION_PLANS[plan_id] = plan
    return {"status": "ok", "plan": plan}, 200


def confirm_operation(body: dict[str, Any], authorization: str) -> tuple[dict[str, Any], int]:
    plan_id = str(body.get("plan_id") or "")
    with _OPERATION_LOCK:
        plan = _OPERATION_PLANS.get(plan_id)
        if plan is None:
            return {"status": "error", "error": "unknown plan"}, 404
        expected = f"Bearer {OPERATIONS_CAPABILITY_TOKEN}"
        if not OPERATIONS_CAPABILITY_TOKEN or not hmac.compare_digest(authorization, expected):
            return {"status": "error", "error": "capability confirmation denied"}, 403
        if not OPERATIONS_ENABLED:
            return {"status": "error", "error": "execution disabled by server policy", "plan": plan}, 409
        # Execution adapters are deliberately not implicit.  A configured adapter
        # must perform the action and read-back before this status can become executed.
        receipt = {"receipt_id": hashlib.sha256(f"{plan_id}:{time.time()}".encode()).hexdigest()[:24], "plan_id": plan_id, "status": "execution_adapter_missing", "created_at": time.time()}
        _append_operation_receipt(receipt)
        _OPERATION_RECEIPTS.append(receipt)
        return {"status": "error", "error": "no execution adapter configured", "receipt": receipt}, 501


def build_portal_manifest() -> dict[str, Any]:
    """Mapa architektury portalu i jego źródeł danych."""
    return {
        "status": "ok",
        "version": "portal-manifest/v1",
        "portal": {
            "name": "NOEMA Portal",
            "port": PORT,
            "root": str(SITE_ROOT),
            "description": "Żywy interfejs systemu NOEMA z dashboardem, stanem, pamięcią i CIELingo.",
        },
        "layers": [
            {
                "name": "Surface / Runtime",
                "role": "Bezpośrednie mmap i pamięć współdzielona",
                "sources": [f"{SURFACE_ROOT}/*"],
            },
            {
                "name": "Portal APIs",
                "role": "HTTP warstwa integracyjna portalu",
                "sources": ["/api/live", "/api/status/summary", "/api/metrics", "/api/modules", "/api/portal/manifest", "/api/phasenav/graphics"],
            },
            {
                "name": "Cognition",
                "role": "CIELingo, memory, agent backend, PhaseNav",
                "sources": ["/api/cielingo/chat", "/api/cielingo/thread", "/api/cielingo/analyze", "/api/phasenav/state", "/api/phasenav/graphics"],
            },
            {
                "name": "Knowledge / Tasks",
                "role": "Bazy wiedzy i planów",
                "sources": [_KNOWLEDGE_DB_PATH, _TASKPLAN_DB_PATH, "/api/knowledge/*", "/api/tasks", "/api/plans"],
            },
            {
                "name": "Visualization",
                "role": "Dashboard, status, systems, Bloch, architecture",
                "sources": ["/", "#dashboard", "#status", "#systems", "#memory", "#projects", "#bloch", "#architecture"],
            },
        ],
        "endpoints": [
            {"path": "/api/live", "purpose": "Live surface state"},
            {"path": "/api/metrics", "purpose": "Katalog metryk dla dashboardu"},
            {"path": "/api/metrics/catalog", "purpose": "Kanoniczny katalog metryk z null/stale/error i provenance"},
            {"path": "/api/metrics/system/:system_id", "purpose": "Metryki jednego systemu logicznego"},
            {"path": "/api/systems", "purpose": "Katalog systemów logicznych i oddzielnych instancji runtime"},
            {"path": "/api/systems/:system_id", "purpose": "Szczegóły systemu, instancje i jego metryki"},
            {"path": "/api/operations", "purpose": "Allowlista operacji Cockpitu i receipty"},
            {"path": "/api/operations/plan", "purpose": "Plan operacji z idempotency key"},
            {"path": "/api/operations/confirm", "purpose": "Capability confirmation; wykonanie wymaga adaptera"},
            {"path": "/api/modules", "purpose": "Daemon registry"},
            {"path": "/api/status/summary", "purpose": "Podsumowanie systemu"},
            {"path": "/api/portal/manifest", "purpose": "Mapa architektury portalu"},
            {"path": "/api/cielingo/chat", "purpose": "Czat z CIELingo"},
            {"path": "/api/bloch", "purpose": "Sfera Blocha i flow vectors"},
            {"path": "/api/phasenav/graphics", "purpose": "PhaseNav graphics bundle (surface, memory, relations, operators)"},
            {"path": "/api/knowledge/stats", "purpose": "Statystyki knowledge DB"},
            {"path": "/api/tasks", "purpose": "TaskPlan DB"},
        ],
        "pages": [
            {"route": "dashboard", "title": "Dashboard", "purpose": "Szybki widok live",
             "sources": ["/api/live", "/api/metrics/catalog", "/api/systems"],
             "notes": "Koło fazowe, metryki, daemon registry."},
            {"route": "metrics", "title": "Katalog metryk", "purpose": "Definicje, jednostki i provenance metryk",
             "sources": ["/api/metrics/catalog"], "notes": "Braki danych pozostają null/niedostępne."},
            {"route": "research", "title": "Research / Public", "purpose": "Badania i formalizmy bez danych operacyjnych",
             "sources": ["/api/metrics/catalog", "/api/knowledge/stats", "/api/phasenav/graphics"], "notes": "Brak PID-ów, portów i operacji."},
            {"route": "operations", "title": "Operacje Cockpitu", "purpose": "Planowanie kontrolowanych operacji",
             "sources": ["/api/operations", "/api/operations/plan", "/api/operations/confirm"], "notes": "Capability, potwierdzenie, read-back i receipt."},
            {"route": "cielingo-chat", "title": "CIELingo", "purpose": "Czat i frame analysis",
             "sources": ["/api/cielingo/chat", "/api/cielingo/thread", "/api/cielingo/analyze"],
             "notes": "Rozmowa z CIEL + pamięć sesji."},
            {"route": "status", "title": "Status", "purpose": "Stan systemu i infrastruktura",
             "sources": ["/api/status/summary", "/api/live", "/api/modules", "/api/ciel/state"],
             "notes": "Daemony, surface, CIEL state, IPC."},
            {"route": "systems", "title": "Systemy", "purpose": "Mapa systemów i modułów",
             "sources": ["/api/systems", "/api/systems/:system_id"],
             "notes": "System logiczny i każda instancja runtime osobno."},
            {"route": "memory", "title": "Memory", "purpose": "Kanały M0–M11 i wątki CIELingo",
             "sources": ["/api/live", "/api/cielingo/thread"],
             "notes": "Pamięć kanałowa + historia rozmów."},
            {"route": "projects", "title": "Projects", "purpose": "Projekty i zadania",
             "sources": ["/api/cards", "/api/tasks"],
             "notes": "Systemy NOEMA i taski DB."},
            {"route": "phasenav", "title": "PhaseNav", "purpose": "Operator algebra i wizualizacja",
             "sources": ["/api/live", "/api/phasenav/state", "/api/phasenav/graphics", "/api/bloch"],
             "notes": "Program fazowy + surface injection + graphics bundle."},
            {"route": "bloch", "title": "Bloch", "purpose": "Sfera Blocha i vektor programu",
             "sources": ["/api/bloch"],
             "notes": "36 punktów, coupling, flow vectors."},
            {"route": "knowledge", "title": "Knowledge", "purpose": "Graf i wyszukiwarka wiedzy",
             "sources": ["/api/knowledge/stats", "/api/knowledge/search", "/api/knowledge/coverage"],
             "notes": "TF-IDF, affinity, coverage."},
            {"route": "monograph", "title": "Monografia", "purpose": "Dokumentacja i rozdziały monografii",
             "sources": ["/api/knowledge/stats"], "notes": "Przegląd materiałów monografii."},
            {"route": "graph", "title": "Graf wiedzy", "purpose": "Statystyki i relacje wiedzy",
             "sources": ["/api/knowledge/stats", "/api/status/summary"], "notes": "Relacyjny widok wiedzy."},
            {"route": "science", "title": "Nauka", "purpose": "Naukowe kontrakty i stan badań",
             "sources": ["/api/knowledge/stats", "/api/portal/manifest", "/api/status/summary"], "notes": "Widok naukowy."},
            {"route": "engineering", "title": "Inżynieria", "purpose": "Moduły, zadania i skille",
             "sources": ["/api/modules", "/api/status/summary", "/api/tasks/queue", "/api/skills/stats"], "notes": "Widok inżynieryjny."},
            {"route": "simulations", "title": "Symulacje", "purpose": "Sceny symulacyjne PhaseNav",
             "sources": ["/api/phasenav/graphics"], "notes": "Wizualizacje scen PhaseNav."},
            {"route": "decision-tree", "title": "Drzewo decyzji", "purpose": "Rejestr decyzji",
             "sources": ["/api/decisions"], "notes": "Decyzje TaskPlan."},
            {"route": "preferences", "title": "Preferencje", "purpose": "Konfiguracja i stan CIEL",
             "sources": ["/api/settings", "/api/ciel/state"], "notes": "Preferencje runtime."},
            {"route": "architecture", "title": "Architecture", "purpose": "Mapa przepływu danych",
             "sources": ["/api/portal/manifest", "/api/status/summary"],
             "notes": "Warstwy, zależności, dataflow."},
        ],
        "pipelines": [
            {"from": f"{SURFACE_ROOT}/*", "to": "/api/live", "label": "surface → live cards"},
            {"from": _TASKPLAN_DB_PATH, "to": "/api/status/summary", "label": "TaskPlan timeline"},
            {"from": _KNOWLEDGE_DB_PATH, "to": "/api/knowledge/*", "label": "Knowledge search"},
            {"from": f"{SURFACE_ROOT}/agent_hint", "to": "/api/cielingo/chat", "label": "CIELingo hint loop"},
        ],
    }

# PhaseNav 12-kanałowy display-name mapping dla /api/embeddings. UWAGA: to
# NIE jest ten sam obiekt co CHANNEL_MAP w PortalHandler.do_GET (/api/live) —
# nazwy dwóch kanałów się różnią (M5_Affective vs M5_Affective_Ethical,
# M7_Braid vs M7_Braid_Invariant), więc scalenie w jedną stałą modułową
# zmieniłoby zwracane klucze JSON w jednym z dwóch route'ów. Zostawione
# osobno świadomie — false-positive z audytu, nie duplikat do usunięcia.
_EMBEDDINGS_CHANNEL_NAMES = [
    "M0_Perceptual", "M1_Working", "M2_Episodic", "M3_Semantic",
    "M4_Procedural", "M5_Affective", "M6_Identity", "M7_Braid",
    "M8_Meta", "M9_Temporal", "M10_Imaginal", "M11_Quantum",
]

def build_embeddings_payload(query_str: str, top_k: int = 10) -> dict[str, Any]:
    """Knowledge DB embeddings — 36D PhaseNav document vectors (12 kanałów ×
    3 oscylatory). Backing /api/embeddings. Bez query_str: statystyki R_global
    po całym korpusie. Z query_str: dopasowanie słów kluczowych → 12D wagi
    kanałów → 36D wektor fazowy zapytania → cosine similarity w przestrzeni
    fazowej (nie euklidesowej) względem embeddingów dokumentów."""
    import numpy as np
    embeddings, index = _get_embeddings()
    if embeddings is None:
        return {"status": "error", "error": "embeddings not found, run ciel_noema_doc_embedder.py --rebuild"}

    entries = index["entries"]
    n_docs = len(entries)

    if not query_str:
        R_vals = [e.get("R_global", 0) for e in entries]
        return {
            "status": "ok",
            "n_docs": n_docs,
            "n_dimensions": 36,
            "n_channels": 12,
            "mean_R": round(float(np.mean(R_vals)), 4) if R_vals else 0,
            "min_R": round(float(np.min(R_vals)), 4) if R_vals else 0,
            "max_R": round(float(np.max(R_vals)), 4) if R_vals else 0,
            "channels": _EMBEDDINGS_CHANNEL_NAMES,
            "sample_docs": [{"idx": e["idx"], "filename": e["filename"], "R_global": e.get("R_global", 0)} for e in entries[:5]],
        }

    # Keyword→channel weights
    ch_keywords = (
        (["percept","sensor","obserw","widz","postrzeg","zmysł","perception","sense","light","sound","image","pattern","shape","color"],),
        (["operator","logik","składnia","struktur","funkcj","proces","algorithm","compute","syntax","grammar","logic","function","process","operation"],),
        (["kontekst","epizod","zdarzen","scen","sytuacj","pamięć","context","episode","event","scene","memory","experience","place","time"],),
        (["znaczen","semantyk","definicj","pojęci","rozumien","wiedza","meaning","semantic","concept","knowledge","understanding","define","term"],),
        (["procedur","działan","umiejętnoś","metoda","technik","krok","skill","procedure","action","method","technique","step","practice"],),
        (["emocj","uczuci","nastrój","afekt","wartoś","etyk","moral","emotion","feeling","mood","affect","value","ethical","moral","love","fear"],),
        (["tożsamoś","osoba","podmiot","autor","ja","self","identity","soul","ego","author","subject","person","character"],),
        (["relacj","powiązan","sieć","graf","łącz","relation","connection","network","graph","link","braid","weave"],),
        (["meta","refleksj","abstrakcj","model","teori","reflection","abstract","model","theory","paradigm","cognition"],),
        (["czas","przeszłoś","przyszłoś","teraz","chwil","moment","time","past","future","present","temporal","duration"],),
        (["wyobraźn","kreatywnoś","imaginacj","symbol","metafor","imagination","creative","vision","symbol","metaphor","dream","myth"],),
        (["kwant","niepewnoś","potencjał","superpozycj","probabilist","quantum","uncertain","potential","superposition","entangle","probability"],),
    )
    query_terms = query_str.lower().split()
    q_w = np.zeros(12, dtype=np.float64)
    for ch_idx, kw_list in enumerate(ch_keywords):
        for t in query_terms:
            for kw in kw_list[0]:
                if kw in t or t in kw:
                    q_w[ch_idx] += 1.0
                    break
    max_w = max(float(np.max(q_w)), 1e-12)
    if max_w > 0:
        q_w /= max_w

    # 36D query phase vector (wektoryzowane)
    osc_phase = np.array([0.0, 2*np.pi/3, 4*np.pi/3])
    q_phi = (np.repeat(q_w, 3) * np.pi + np.tile(osc_phase, 12)) % (2*np.pi)

    # Cosine similarity w przestrzeni fazowej
    diff = np.angle(np.exp(1j * (embeddings[:n_docs] - q_phi)))
    scores = np.mean(np.cos(diff), axis=1)
    top_idx = np.argsort(scores)[::-1][:top_k]

    results = []
    for i in top_idx:
        entry = entries[i]
        results.append({
            "rank": len(results) + 1,
            "idx": entry["idx"],
            "filename": entry["filename"],
            "similarity": round(float(scores[i]), 4),
            "R_global": entry.get("R_global", 0),
            "essence": entry.get("essence", "")[:500],
        })
    return {
        "status": "ok",
        "query": query_str,
        "n_docs": n_docs,
        "results": results,
        "n_channels": 12,
        "n_dimensions": 36,
    }

# ─── HTTP Handler ───────────────────────────────────────────────────────

MIME_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
}

class PortalHandler(http.server.BaseHTTPRequestHandler):
    """HTTP handler dla NOEMA Portal Daemon."""

    def _parse_qs(self) -> dict[str, list[str]]:
        """Parsuje query string z self.path. Zastępuje 11 identycznych
        `from urllib.parse import urlparse, parse_qs; parse_qs(urlparse(self.path).query)`
        rozrzuconych po do_GET/do_POST/do_PUT/do_DELETE."""
        from urllib.parse import urlparse, parse_qs
        return parse_qs(urlparse(self.path).query)

    def _read_body(self) -> dict[str, Any]:
        """Czyta i parsuje JSON body żądania po Content-Length. Zastępuje ~10
        identycznych bloków w route'ach POST/PUT tego handlera. Brak body
        (Content-Length: 0) zwraca {} — dokładnie zachowanie wszystkich
        oryginalnych call site'ów (żaden nie traktował pustego body jako
        twardego błędu)."""
        length = int(self.headers.get("Content-Length", 0))
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        if not raw:
            return {}
        return json.loads(raw)

    def do_GET(self):
        path = self.path.split("?")[0].rstrip("/")

        # ── Streaming chat (SSE) ──
        # Delivers an already-computed ciel_headless_daemon response in small
        # sentence-sized pieces instead of one blob, per Adrian's request that
        # CIEL "speak in steps ... small wavelets of meaning, not a tsunami".
        # This does not regenerate content incrementally (ciel_speaker/
        # autonomous_response are template/retrieval-based, not a token-by-
        # token decoder) -- it paces delivery of the real, complete answer
        # using the same sentence-boundary split response_budget.py already
        # used for clipping (now exposed as SENTENCE_BOUNDARY, no longer
        # clipping anything -- see git history for the length-cap removal).
        # GET (not POST) because the browser's native EventSource only issues
        # GET requests.
        if path == "/api/cielingo/chat/stream" and self.command == "GET":
            from urllib.parse import unquote
            qs = self._parse_qs()
            message = unquote(qs.get("message", [""])[0])
            session_id = unquote(qs.get("session_id", [""])[0]).strip()
            if not message.strip() or not session_id:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "message and session_id are required"}).encode("utf-8"))
                return

            resp_text, frame_data, headless_error = request_ciel_headless(message, session_id)

            if isinstance(resp_text, str) and resp_text.strip():
                t = threading.Thread(
                    target=_ingest_headless_turn,
                    args=(message, resp_text, session_id),
                    daemon=True,
                )
                t.start()

            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("X-Accel-Buffering", "no")
            self.end_headers()

            if not isinstance(resp_text, str):
                error_payload = json.dumps(
                    {"error": headless_error or "no response from ciel_headless_daemon"}, ensure_ascii=False
                )
                try:
                    self.wfile.write(f"event: error\ndata: {error_payload}\n\n".encode("utf-8"))
                    self.wfile.flush()
                except (BrokenPipeError, ConnectionResetError):
                    pass
                return

            from cielingo_core.response_budget import SENTENCE_BOUNDARY
            compact = " ".join(resp_text.split())
            chunks = SENTENCE_BOUNDARY.split(compact) if compact else []
            if not chunks:
                chunks = [compact]
            try:
                for i, chunk in enumerate(chunks):
                    payload = json.dumps(
                        {"chunk": chunk, "index": i, "final": i == len(chunks) - 1}, ensure_ascii=False
                    )
                    self.wfile.write(f"data: {payload}\n\n".encode("utf-8"))
                    self.wfile.flush()
                    if i < len(chunks) - 1:
                        time.sleep(0.6)
                done_payload = json.dumps({"frame": frame_data}, ensure_ascii=False)
                self.wfile.write(f"event: done\ndata: {done_payload}\n\n".encode("utf-8"))
                self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                pass
            return

        # ── API endpoints ──
        if path == "/api/health" and self.command == "GET":
            snapshot = get_portal_snapshot()
            snapshot_contract = portal_snapshot_contract(snapshot)
            orbital = build_orbital_payload()
            return self._json({
                "status": snapshot_contract["status"],
                "status_scope": "portal_surface",
                "pid": os.getpid(),
                "uptime_s": round(time.time() - start_time, 1),
                "surface_alive": snapshot_contract["status"] != "error",
                "surface": snapshot_contract,
                "orbital": {
                    "status": orbital.get("status"),
                    "orbital_status": orbital.get("orbital_status"),
                    "coherence": orbital.get("coherence"),
                    "source": orbital.get("source"),
                    "publication": orbital.get("publication"),
                    "error": orbital.get("error"),
                },
            })

        if path == "/api/live" and self.command == "GET":
            """Live dashboard data — Kuramoto order parameter per channel, flavor, gravity, CIEL."""
            import numpy as np
            snapshot = get_portal_snapshot()
            snapshot_contract = portal_snapshot_contract(snapshot)
            if snapshot["status"] == "error":
                return self._json({
                    "status": "error",
                    "error": snapshot["error"],
                    "surface_snapshot": snapshot_contract,
                    "tick": None,
                    "gravity": copy.deepcopy(snapshot["gravity"]),
                    **snapshot["gravity"],
                })

            def _get_arr(name, n=36):
                try:
                    return np.asarray(surface[name], dtype=np.float64).ravel()
                except Exception:
                    _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py quiet except scope=PortalHandler.do_GET._get_arr reason=return np.zeros(n)")
                    return np.zeros(n)

            tick_val = snapshot["tick"]
            phi_v = _get_arr("phi")
            omega_v = _get_arr("omega")
            tau_v = _get_arr("tau")
            flavor_v = _get_arr("flavor", 6)
            sensor_v = _get_arr("sensor_raw")

            # ── Kuramoto global coherence = flavor[0] ──
            kuramoto_coherence = float(flavor_v[0]) if len(flavor_v) > 0 else None

            # ── Channel coh: Kuramoto order parameter per channel (12 channels × 3) ──
            # R_ch = |(1/N) Σ exp(i·φ_j)| dla j w kanale
            CHANNEL_MAP = {
                "M0_Perceptual":        (0,1,2),
                "M1_Working":           (3,4,5),   # AGENT attractor
                "M2_Episodic":          (6,7,8),
                "M3_Semantic":          (9,10,11),
                "M4_Procedural":        (12,13,14),
                "M5_Affective_Ethical": (15,16,17),
                "M6_Identity":          (18,19,20),
                "M7_Braid_Invariant":   (21,22,23),
                "M8_Meta":              (24,25,26),
                "M9_Temporal":          (27,28,29),
                "M10_Imaginal":         (30,31,32),
                "M11_Quantum":          (33,34,35),
            }
            channel_coh = {}
            for ch_name, idxs in CHANNEL_MAP.items():
                phis = phi_v[list(idxs)]
                # R = |mean(exp(i·φ))|
                complex_mean = np.mean(np.exp(1j * phis))
                channel_coh[ch_name] = round(float(np.abs(complex_mean)), 6)

            # AGENT coherence = M1
            agent_coh = channel_coh.get("M1_Working")

            # ── Flavor bars ──
            # flavor[0]=R_coherence, [1]=mem_pressure, [2]=io_pressure, [3]=mood, [4]=entropy, [5]=mode
            # Was FLAVOR_LABELS = ["cp","coh","mood","open","Λ","D_f"] — positionally
            # mapped 1:1 onto f_raw, so "mood" showed raw io_pressure (near-zero on an
            # idle disk) and "open" showed the real mood value. A dashboard user
            # would see contradictory mood readings between this panel and the real
            # mood metric elsewhere on the same page. Fixed 2026-07-08 to label each
            # slot by what it actually is, per FLAVOR_CONTRACT in noema_surface_mmap.py.
            FLAVOR_LABELS = ["cp", "mem", "io", "mood", "Λ", "D_f"]
            flavor_bars = {}
            f_raw = flavor_v.tolist()[:6]
            for i, label in enumerate(FLAVOR_LABELS):
                flavor_bars[label] = round(float(f_raw[i]), 6) if i < len(f_raw) else None

            # ── Omega / Tau / Phi stats ──
            omega_mean = float(np.mean(omega_v)) if omega_v.size > 0 else None
            tau_mean = float(np.mean(tau_v)) if tau_v.size > 0 else None
            phi_mean = float(np.mean(phi_v)) if phi_v.size > 0 else None
            phi_var = float(np.var(phi_v)) if phi_v.size > 0 else None

            # ── Gravity ──
            grav = snapshot["gravity"]
            gamma_val = grav["tau_dilation"]
            mass_val = grav["mass_total"]
            unruh_val = grav["unruh_power"]
            density_val = grav["semantic_density"]

            # ── Sensor ──
            sensor_mean = float(np.mean(sensor_v)) if sensor_v.size > 0 else None

            # ── CIEL/Ω pipeline state (ethical_score, soul_invariant, etc.) ──
            _cs = _read_ciel_state()
            _ethical_score = _cs.get("ethical_score") if isinstance(_cs, dict) else None
            _soul_invariant = _cs.get("soul_invariant") if isinstance(_cs, dict) else None
            _coherence_index = _cs.get("coherence_index") if isinstance(_cs, dict) else None
            _dominant_emotion = _cs.get("dominant_emotion") if isinstance(_cs, dict) else None
            _operating_mode = _cs.get("operating_mode") if isinstance(_cs, dict) else None
            # ciel_state.json stores the value as "closure_penalty_raw"; fall
            # back to legacy "closure_penalty" for forward compat.
            _closure_penalty = (
                _cs.get("closure_penalty") or _cs.get("closure_penalty_raw")
            ) if isinstance(_cs, dict) else None

            # Canonical EBA closure is computed by the memory holonomy runtime
            # and adapted from its report in the shared PortalSnapshot.
            euler_res = snapshot["math"]["closure_eba"].get("value")

            # Backward-compat arrays for dashboard.js (expects array)
            flavor_array = [flavor_bars.get(l) for l in FLAVOR_LABELS[:8]]
            ch_labels_sorted = sorted(channel_coh.keys(), key=lambda x: int(x.split("_")[0][1:]) if x.startswith("M") else 0)
            ch_array = [channel_coh.get(k) for k in ch_labels_sorted]

            return self._json({
                "status": snapshot_contract["status"],
                "timestamp": snapshot_contract["timestamp"],
                "source_timestamp": snapshot_contract["source_timestamp"],
                "age_s": snapshot_contract["age_s"],
                "stale": snapshot_contract["stale"],
                "surface_snapshot": snapshot_contract,
                "tick": tick_val,

                # Primary metrics (dashboard.js compatible)
                "coherence": _round_optional(kuramoto_coherence if (kuramoto_coherence is not None and kuramoto_coherence > 0) else agent_coh, 6),
                "agent_coherence": _round_optional(agent_coh, 6),
                "phi_coh": _round_optional(kuramoto_coherence, 6),  # dashboard.js uses phi_coh for euler card
                "euler_residual": round(euler_res, 6) if euler_res is not None else None,
                "eba_closure_residual": round(euler_res, 6) if euler_res is not None else None,
                "phi_mean": _round_optional(phi_mean, 6),
                "phi_var": _round_optional(phi_var, 6),
                "omega_mean": _round_optional(omega_mean, 6),
                "tau_mean": _round_optional(tau_mean, 6),
                "sensor_mean": _round_optional(sensor_mean, 6),

                # Gravity
                "gamma": round(gamma_val, 4),
                "mass": round(mass_val, 4),
                "tau_dilation": gamma_val,
                "mass_total": mass_val,
                "unruh_power": round(unruh_val, 6),
                "semantic_density": round(density_val, 6),

                # Mood
                "mood": round(float(f_raw[3]), 4),

                # Flavor — dict + backward-compat array (8 fields)
                "flavor": flavor_bars,
                "flavor_raw": f_raw,
                "flavor_array": flavor_array,

                # Channel coherence — dict + backward-compat array (sorted M0-M11)
                "channel_coh": channel_coh,
                "channel_list": ch_labels_sorted,
                "channel_coh_array": ch_array,

                # Full gravity dict
                "gravity": grav,

                # CIEL/Ω ethics + identity
                "ethical_score": _round_optional(_ethical_score, 6),
                "soul_invariant": _round_optional(_soul_invariant, 6),
                "coherence_index": _round_optional(_coherence_index, 6),
                "dominant_emotion": _dominant_emotion,
                "operating_mode": _operating_mode,
                "closure_penalty": _round_optional(_closure_penalty, 6),
            })

        # ── Metrics / manifest / status (self-describing portal metadata) ──
        if path == "/api/metrics" and self.command == "GET":
            return self._json(build_metrics_catalog())

        if path == "/api/systems" and self.command == "GET":
            return self._json(build_portal_system_catalog())

        if path.startswith("/api/systems/") and self.command == "GET":
            system_id = path.removeprefix("/api/systems/")
            catalog = build_portal_system_catalog()
            system = next((item for item in catalog["systems"] if item["system_id"] == system_id), None)
            if system is None:
                return self._json({"status": "not_found", "error": "system not found", "system_id": system_id}, 404)
            metric_catalog = build_portal_metric_catalog()
            return self._json({
                "contract": "noema.system-detail/v1",
                "observed_at": catalog["observed_at"],
                "system": system,
                "instances": [item for item in catalog["instances"] if item["system_id"] == system_id],
                "metrics": metric_catalog["by_system"].get(system_id, []),
            })

        if path == "/api/metrics/catalog" and self.command == "GET":
            return self._json(build_portal_metric_catalog())

        if path == "/api/operations" and self.command == "GET":
            return self._json(operation_inventory())

        if path.startswith("/api/metrics/system/") and self.command == "GET":
            system_id = path.removeprefix("/api/metrics/system/")
            catalog = build_portal_metric_catalog()
            return self._json({
                "contract": "noema.system-metrics/v1",
                "observed_at": catalog["observed_at"],
                "system_id": system_id,
                "metrics": catalog["by_system"].get(system_id, []),
            })

        if path == "/api/portal/manifest" and self.command == "GET":
            return self._json(build_portal_manifest())

        if path == "/api/hub/contracts" and self.command == "GET":
            """Kontrakty API huba dla strony Architektura — pochodne z manifestu portalu.
            architecture.js oczekuje {endpoints: [{path, summary}]}; poprzednio 404,
            bo ten endpoint nigdy nie został dodany mimo że frontend go wywołuje."""
            manifest = build_portal_manifest()
            endpoints = [
                {"path": e.get("path", ""), "summary": e.get("purpose", "")}
                for e in manifest.get("endpoints", [])
            ]
            return self._json({"status": "ok", "endpoints": endpoints, "source": "portal_manifest"})

        if path == "/api/modules" and self.command == "GET":
            """Lista daemonów/modules — alias dla dashboardu."""
            daemons = scan_registry()
            modules = []
            for d in daemons:
                alive = d.get("alive")
                modules.append({
                    "name": d.get("name", "?"),
                    "status": d.get("status", "unknown"),
                    "alive": alive,
                    "pid": d.get("pid"),
                    "systemd": "active" if alive is True else "inactive" if alive is False else "unknown",
                    "uptime": d.get("uptime") if d.get("uptime") is not None else d.get("uptime_s"),
                })
            return self._json({
                "status": "ok",
                "modules": modules,
                "count": len(modules),
            })

        if path == "/api/status" and self.command == "GET":
            daemons = scan_registry()
            snapshot = get_portal_snapshot()
            snapshot_contract = portal_snapshot_contract(snapshot)
            orbital = build_orbital_payload()
            return self._json({
                "status": snapshot_contract["status"],
                "status_scope": "portal_surface",
                "timestamp": time.time(),
                "portal": {
                    "pid": os.getpid(),
                    "port": PORT,
                    "uptime_s": round(time.time() - start_time, 1),
                    "surface_alive": snapshot_contract["status"] != "error",
                },
                "surface": build_surface_status_payload(snapshot),
                "orbital": orbital,
                "daemons": daemons,
            })

        if path == "/api/status/summary" and self.command == "GET":
            """Live podsumowanie systemu: baza + daemony + surface."""
            daemons = scan_registry()
            snapshot = get_portal_snapshot()
            snapshot_contract = portal_snapshot_contract(snapshot)
            state = snapshot.get("_state", {})
            summary = {
                "status": snapshot_contract["status"],
                "status_scope": "portal_surface",
                "timestamp": snapshot_contract["timestamp"],
                "timestamp_iso": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(snapshot_contract["timestamp"])),
                "epoch": snapshot_contract["timestamp"],
                "surface_snapshot": snapshot_contract,
                "portal": {
                    "pid": os.getpid(),
                    "port": PORT,
                    "uptime_s": round(time.time() - start_time, 1),
                    "surface_alive": snapshot_contract["status"] != "error",
                },
                "daemons": {
                    "count": len(daemons),
                    "list": daemons,
                },
            }
            # TaskPlan DB
            try:
                from ciel_geometry.taskplan_db import TaskPlanDB
                tp = TaskPlanDB()
                summary["taskplan"] = tp.stats()
                # dodaj count skilli i decyzji
                import sqlite3
                conn = sqlite3.connect(_TASKPLAN_DB_PATH)
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM skill_registry")
                summary["taskplan"]["skills"] = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM decisions")
                summary["taskplan"]["decisions"] = cur.fetchone()[0]
                # ostatnie 5 decyzji z timestampami do timeline
                cur.execute("SELECT lp, title, decision_type, status, created_at, updated_at FROM decisions ORDER BY updated_at DESC LIMIT 5")
                rows = cur.fetchall()
                summary["taskplan"]["recent_decisions"] = [
                    {"lp": r[0], "title": r[1], "decision_type": r[2], "status": r[3], "created_at": r[4], "updated_at": r[5]}
                    for r in rows
                ]
                conn.close()
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py quiet except scope=PortalHandler.do_GET reason=assign_fallback")
                summary["taskplan"] = {"error": str(e)}
            # Skills catalog (SKILLS.md) — separate from taskplan.skills, which
            # only counts skills registered via noema_skill_merger.py's merge
            # workflow (legitimately 0 until that tool is used). This field
            # reports the real catalog size so the dashboard isn't misleading.
            try:
                summary["skills_catalog"] = _skills_catalog_count()
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py:skills_catalog failed: %s" % e)
                summary["skills_catalog"] = {"error": str(e)}
            # The tiered-memory snapshot owns runtime initialization and may
            # write its surface.  A portal request is observation only: do not
            # invoke that lifecycle while the daemon-owned surface is absent
            # or structurally invalid.
            if snapshot_contract["status"] != "ok":
                summary["memory"] = {
                    "status": "unavailable",
                    "error": "tiered memory was not queried because the daemon-owned surface is unavailable",
                }
            else:
                try:
                    from ciel_omega.memory import tiered_health, tiered_snapshot
                    mem_health = tiered_health()
                    mem_snap = tiered_snapshot()
                    summary["memory"] = {
                        "status": "available",
                        "health": mem_health,
                        "bootstrap": mem_snap.memory_bootstrap,
                        "cycle_index": mem_snap.cycle_index,
                        "identity_phase": mem_snap.identity_phase,
                    }
                except Exception as e:
                    _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py memory snapshot failed")
                    summary["memory"] = {"status": "error", "error": str(e)}
            # Knowledge DB
            try:
                conn2 = sqlite3.connect(_KNOWLEDGE_DB_PATH)
                cur2 = conn2.cursor()
                cur2.execute("SELECT COUNT(*) FROM doc_analysis")
                docs = cur2.fetchone()[0]
                cur2.execute("SELECT COUNT(*) FROM term_index")
                terms = cur2.fetchone()[0]
                cur2.execute("SELECT COUNT(*) FROM semantic_affinity")
                aff = cur2.fetchone()[0]
                conn2.close()
                summary["knowledge"] = {"documents": docs, "terms": terms, "affinity_pairs": aff}
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py quiet except scope=PortalHandler.do_GET reason=assign_fallback")
                summary["knowledge"] = {"error": str(e)}
            # Surface live
            summary["surface"] = build_surface_status_payload(snapshot)
            # Orbital model (v3) — teraz dorównuje pełnej wersji /api/orbital
            # (view_ascii + top_phases[:10]) przez wspólny _read_orbital_state().
            summary["orbital"] = build_orbital_payload()
            return self._json(summary)

        # ── Settings (config file read/write, no module import — L-026) ──
        if path == "/api/settings" and self.command == "GET":
            """Ustawienia systemowe NOEMA — czyta JSON bez importu modułu (L-026)."""
            try:
                # Szukaj pliku konfiguracyjnego
                config_paths = [
                    NOEMA_ROOT / "noema_config.json",
                    Path(os.environ.get("NOEMA_CONFIG", "")),
                ]
                cfg = None
                for p in config_paths:
                    if p and p.exists():
                        cfg = json.loads(p.read_text())
                        break
                if cfg is None:
                    # fallback do starej ścieżki
                    from pathlib import Path as _P
                    _noema_root = os.environ.get("NOEMA_ROOT", str(Path(__file__).resolve().parent.parent))
                    fallback = _P(_noema_root) / "noema_config.json"
                    if fallback.exists():
                        cfg = json.loads(fallback.read_text())
                return self._json({
                    "status": "ok",
                    "source": "noema_config.json (file read, no module import)",
                    "settings": cfg or {},
                })
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py quiet except scope=PortalHandler.do_GET reason=return self._json({\"status\": \"error\", \"error\": str(e)})")
                return self._json({"status": "error", "error": str(e)})

        # ── Combined kuramoto/surface/daemon metrics (superset of /api/metrics) ──
        if path == "/api/metrics/all" and self.command == "GET":
            snapshot = get_portal_snapshot()
            snapshot_contract = portal_snapshot_contract(snapshot)
            state = snapshot.get("_state", {})
            daemons = scan_registry()
            active_d = sum(1 for d in daemons if d.get("alive"))
            return self._json({
                "status": snapshot_contract["status"],
                "timestamp": snapshot_contract["timestamp"],
                "surface_snapshot": snapshot_contract,
                "kuramoto": {
                    "coherence": _first_present(state, "coherence", "coherence_index"),
                    "euler_residual": (snapshot.get("math") or {}).get("closure_eba", {}).get("value"),
                    "mean_omega": _first_present(state, "omega_mean"),
                    "tick": snapshot.get("tick"),
                },
                "surface": {
                    **snapshot_contract,
                    "phi_mean": _first_present(state, "phi_mean", "R_global"),
                    "phi_std": _first_present(state, "phi_std"),
                    "tau_mean": _first_present(state, "tau_mean"),
                    "gravity": copy.deepcopy(snapshot.get("gravity") or {}),
                },
                "orbital": build_orbital_payload(),
                "daemons": {
                    "total": len(daemons),
                    "active": active_d,
                    "list": daemons,
                },
                "portal": {
                    "pid": os.getpid(),
                    "port": PORT,
                    "uptime_s": round(time.time() - start_time, 1),
                },
            })

        # ── PhaseNav graficzne/wektorowe kodowanie (Bloch sphere + graphics + state) ──
        if path == "/api/bloch" and self.command == "GET":
            # Deleguje do build_bloch_payload() — sfera Blocha, graficzny tryb PhaseNav.
            try:
                return self._json(build_bloch_payload())
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py quiet except scope=PortalHandler.do_GET reason=return self._json({\"status\": \"error\", \"error\": str(e), \"points\": [], \"edges\": [], \"vectors\": [], \"program\": []}, 500)")
                return self._json({"status": "error", "error": str(e), "points": [], "edges": [], "vectors": [], "program": []}, 500)

        if path == "/api/phasenav/state" and self.command == "GET":
            # Deleguje do build_phasenav_state_payload() — lekki odpowiednik /api/bloch.
            try:
                return self._json(build_phasenav_state_payload())
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py:PortalHandler.do_GET quiet except scope=/api/phasenav/state reason=return error")
                return self._json({"status": "error", "error": str(e)}, 500)

        if path == "/api/phasenav/graphics" and self.command == "GET":
            # Deleguje do build_phasenav_graphics_payload() — multi-scene graficzny tryb PhaseNav.
            qs = self._parse_qs()
            query = qs.get("q", ["NOEMA"])[0]
            scene_name = qs.get("scene", ["surface"])[0]
            try:
                return self._json_cached(cached_phasenav_graphics_payload(query=query, scene_name=scene_name))
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py quiet except scope=PortalHandler.do_GET reason=return self._json({\"status\": \"error\", \"error\": str(e)})")
                return self._json({"status": "error", "error": str(e), "query": query, "scene_name": scene_name}, 500)

        # ── Orbital API (PhaseNav JSON, nie import modułu — L-026) ──
        if path == "/api/orbital" and self.command == "GET":
            return self._json(build_orbital_payload())

        # ── Raw surface arrays (single-field mmap reads) ──
        if path == "/api/surface/phi" and self.command == "GET":
            data = read_mmap_array("phi")
            return self._json({"status": "ok", "phi": data} if data else {"status": "error"})

        if path == "/api/surface/omega" and self.command == "GET":
            data = read_mmap_array("omega")
            return self._json({"status": "ok", "omega": data} if data else {"status": "error"})

        if path == "/api/surface/g" and self.command == "GET":
            data = read_mmap_array("g")
            return self._json({"status": "ok", "g": data} if data else {"status": "error"})

        # ── Knowledge API ──
        if path == "/api/knowledge/stats" and self.command == "GET":
            try:
                import sqlite3
                conn = sqlite3.connect(_KNOWLEDGE_DB_PATH)
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM doc_analysis")
                docs = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM term_index")
                terms = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM semantic_affinity")
                aff = cur.fetchone()[0]
                conn.close()
                return self._json({"status": "ok", "stats": {
                    "documents": docs, "terms": terms, "affinity_pairs": aff,
                    "db_path": _KNOWLEDGE_DB_PATH
                }})
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py quiet except scope=PortalHandler.do_GET reason=return self._json({\"status\": \"error\", \"error\": str(e)})")
                return self._json({"status": "error", "error": str(e)})

        if path.startswith("/api/knowledge/search") and self.command == "GET":
            q = self._parse_qs().get("q", [""])[0]
            if not q:
                return self._json({"status": "error", "error": "missing ?q="})
            try:
                from cielingo_core.bridge.knowledge_bridge import query
                results = query(q, top_n=5)
                return self._json({"status": "ok", "query": q, "results": results})
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py quiet except scope=PortalHandler.do_GET reason=return self._json({\"status\": \"error\", \"error\": str(e)})")
                return self._json({"status": "error", "error": str(e)})

        if path.startswith("/api/knowledge/coverage") and self.command == "GET":
            q = self._parse_qs().get("q", [""])[0]
            if not q:
                return self._json({"status": "error", "error": "missing ?q="})
            try:
                from cielingo_core.bridge.knowledge_bridge import check_coverage
                cov = check_coverage(q)
                return self._json({"status": "ok", "query": q, "coverage": cov})
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py quiet except scope=PortalHandler.do_GET reason=return self._json({\"status\": \"error\", \"error\": str(e)})")
                return self._json({"status": "error", "error": str(e)})

        # ── TaskPlan API (tasks / plans / lessons) — _get_tp() is now a
        # module-level singleton, see definition near _get_embeddings() ──

        # ── Tasks ──
        if path == "/api/tasks" and self.command == "GET":
            qs = self._parse_qs()
            db = _get_tp()
            return self._json({"status": "ok", "tasks": db.list_tasks(
                status=qs.get("status", [""])[0],
                category=qs.get("category", [""])[0],
                limit=int(qs.get("limit", ["50"])[0])
            )})

        # ── Task Queue (NOEMA/task_queue.noema.json) — przed generycznym /api/tasks/ ──
        if path == "/api/tasks/queue" and self.command == "GET":
            queue_path = NOEMA_ROOT / "NOEMA" / "task_queue.noema.json"
            try:
                with open(queue_path, 'r') as f:
                    queue_data = json.load(f)
                items = queue_data.get("queue", [])
                pending = [i for i in items if i.get("status") == "pending"]
                done = [i for i in items if i.get("status") == "done"]
                high_prio = [i for i in pending if "HIGH" in (i.get("priority") or "")]
                return self._json({
                    "status": "ok",
                    "total": len(items),
                    "pending": len(pending),
                    "done": len(done),
                    "high_priority": len(high_prio),
                    "items": items,
                    "pending_items": pending,
                    "high_priority_items": high_prio,
                    "path": str(queue_path)
                })
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py quiet except scope=PortalHandler.do_GET reason=return self._json({\"status\": \"error\", \"error\": str(e)})")
                return self._json({"status": "error", "error": str(e)})

        if path.startswith("/api/tasks/") and self.command == "GET":
            tid = int(path.split("/")[-1])
            db = _get_tp()
            t = db.get_task(tid)
            return self._json(t if t else {"status": "error", "error": "not found"})

        # ── Plans ──
        if path == "/api/plans" and self.command == "GET":
            qs = self._parse_qs()
            db = _get_tp()
            return self._json({"status": "ok", "plans": db.list_plans(
                status=qs.get("status", [""])[0],
                limit=int(qs.get("limit", ["20"])[0])
            )})

        # ── Lessons ──
        if path == "/api/lessons" and self.command == "GET":
            qs = self._parse_qs()
            db = _get_tp()
            return self._json({"status": "ok", "lessons": db.list_lessons(
                category=qs.get("category", [""])[0],
                limit=int(qs.get("limit", ["50"])[0])
            )})

        # ── Decisions ──
        if path == "/api/decisions" and self.command == "GET":
            qs = self._parse_qs()
            db = _get_tp()
            parent = qs.get("parent_id", [None])[0]
            return self._json({"status": "ok", "decisions": db.list_decisions(
                decision_type=qs.get("type", [""])[0],
                parent_id=int(parent) if parent else None,
                status=qs.get("status", [""])[0],
                limit=int(qs.get("limit", ["100"])[0])
            )})

        if path == "/api/decisions/tree" and self.command == "GET":
            qs = self._parse_qs()
            db = _get_tp()
            root = qs.get("root", [None])[0]
            return self._json({"status": "ok", "tree": db.get_decision_tree(
                root_id=int(root) if root else None
            )})

        if path.startswith("/api/decisions/") and "/skills" in path and self.command == "GET":
            # /api/decisions/:id/skills
            parts = path.split("/")
            did = int(parts[3])
            db = _get_tp()
            return self._json({"status": "ok", "skills": db.get_skills_for_decision(did)})

        if path.startswith("/api/decisions/") and self.command == "GET":
            did = int(path.split("/")[-1])
            db = _get_tp()
            d = db.get_decision(did)
            return self._json(d if d else {"status": "error", "error": "not found"})

        # ── Skills ──
        if path == "/api/skills" and self.command == "GET":
            qs = self._parse_qs()
            db = _get_tp()
            return self._json({"status": "ok", "skills": db.list_skills(
                category=qs.get("category", [""])[0],
                merge_group=qs.get("merge_group", [""])[0],
                limit=int(qs.get("limit", ["300"])[0])
            )})

        if path == "/api/skills/stats" and self.command == "GET":
            db = _get_tp()
            return self._json({"status": "ok", "stats": db.get_skill_stats()})

        if path.startswith("/api/skills/") and self.command == "GET":
            # /api/skills/:id
            sid = int(path.split("/")[-1])
            db = _get_tp()
            # zwróć skill + decyzje dla niego
            skills = db.list_skills(limit=300)
            skill = next((s for s in skills if s['id'] == sid), None)
            if not skill:
                return self._json({"status": "error", "error": "not found"})
            decisions = db.get_decisions_for_skill(sid)
            skill["decisions"] = decisions
            return self._json({"status": "ok", "skill": skill})

        # ── Registry stats ──
        if path == "/api/tp/stats" and self.command == "GET":
            db = _get_tp()
            return self._json({"status": "ok", "stats": db.stats()})

        # ── PhaseNav Analog Bus ──
        if path == "/api/analog" and self.command == "GET":
            return self._json({
                "status": "ok",
                "source": f"NOEMA analog bus {SURFACE_ROOT / 'analog'}/",
                "timestamp": time.time(),
                "bus": _read_analog_bus(),
            })

        # ── CIEL State ──
        if path == "/api/ciel/state" and self.command == "GET":
            return self._json({
                "status": "ok",
                "source": str(SURFACE_ROOT / "ciel_state.json"),
                "timestamp": time.time(),
                "state": _read_ciel_state(),
            })

        # ── Agent Hint ──
        if path == "/api/agent/hint" and self.command == "GET":
            return self._json({
                "status": "ok",
                "source": str(SURFACE_ROOT / "agent_hint"),
                "timestamp": time.time(),
                "hint": _read_agent_hint(),
            })

        # ── Linux Load ──
        if path == "/api/linux/load" and self.command == "GET":
            return self._json({
                "status": "ok",
                "source": str(SURFACE_ROOT / "linux_load"),
                "timestamp": time.time(),
                "load": _read_linux_load(),
            })

        # ── CIELingo Thread Memory ──
        if path == "/api/cielingo/thread" and self.command == "GET":
            try:
                include_content = self._parse_qs().get("include_content", [""])[0].lower() in {"1", "true", "yes"}
                if include_content:
                    if not THREAD_CONTENT_CAPABILITY_TOKEN:
                        return self._json({
                            "status": "error",
                            "error": "diagnostic thread content capability disabled",
                            "diagnostic_content": "disabled",
                        }, 403)
                    authorization = self.headers.get("Authorization", "")
                    expected = f"Bearer {THREAD_CONTENT_CAPABILITY_TOKEN}"
                    if not hmac.compare_digest(authorization, expected):
                        return self._json({
                            "status": "error",
                            "error": "invalid diagnostic thread content capability",
                            "diagnostic_content": "denied",
                        }, 403)

                if THREAD_MEMORY_PATH.exists():
                    lines = THREAD_MEMORY_PATH.read_text(encoding="utf-8").strip().split("\n")
                    entries = [json.loads(l) for l in lines if l.strip()]
                    response_entries = entries[-20:] if include_content else [_public_thread_entry(entry) for entry in entries[-20:]]
                    return self._json({
                        "status": "ok",
                        "source": str(THREAD_MEMORY_PATH),
                        "count": len(entries),
                        "diagnostic_content": "enabled" if include_content else "redacted",
                        "entries": response_entries,
                    })
                return self._json({"status": "error", "error": "thread memory not found"})
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py quiet except scope=PortalHandler.do_GET reason=return self._json({\"status\": \"error\", \"error\": str(e)})")
                return self._json({"status": "error", "error": str(e)})

        # ── CIELingo Writing Registry ──
        
        if path == "/api/cielingo/analyze" and self.command == "GET":
            """CIELingo semantic analysis via build_lingo_frame."""
            q = self._parse_qs().get("q", [""])[0]
            if not q:
                return self._json({"status": "error", "error": "Missing ?q=..."})
            try:
                from ciel_sot_agent.cielingo_bridge import build_lingo_frame
                frame = build_lingo_frame(q)
                return self._json({"status": "ok", "query": q, "frame": frame})
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py quiet except scope=PortalHandler.do_GET reason=return self._json({\"status\": \"error\", \"error\": str(e)})")
                return self._json({"status": "error", "error": str(e)})

        if path == "/api/cielingo/writings" and self.command == "GET":
            try:
                reg_path = Path(__file__).resolve().parent.parent / "cards" / "writings" / "registry.json"
                if reg_path.exists():
                    with open(reg_path) as f:
                        reg = json.load(f)
                    cards = reg.get("cards", reg.get("writings", reg.get("registry", [])))
                    return self._json({
                        "status": "ok",
                        "source": str(reg_path),
                        "count": len(cards),
                        "total_cards": reg.get("total_cards", len(cards)),
                        "last_updated": reg.get("last_updated"),
                        "writings": cards,
                    })
                return self._json({"status": "error", "error": "writings registry not found"})
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py quiet except scope=PortalHandler.do_GET reason=return self._json({\"status\": \"error\", \"error\": str(e)})")
                return self._json({"status": "error", "error": str(e)})

        # ── NOEMA Cards / System Map ──
        if path == "/api/cards" and self.command == "GET":
            cards = _read_cards_index()
            return self._json_cached({
                "status": "ok",
                "source": "system_map_v2.json",
                **cards,
            })

        if path == "/api/embeddings" and self.command == "GET":
            """Deleguje do build_embeddings_payload()."""
            _qs = self._parse_qs()
            query_str = _qs.get("q", [""])[0]
            top_k = int(_qs.get("top_k", ["10"])[0])
            return self._json(build_embeddings_payload(query_str, top_k))

        # ── Pliki statyczne ──
        if path == "" or path == "/":
            path = "/index.html"
        filepath = SITE_ROOT / path.lstrip("/")
        try:
            filepath = filepath.resolve()
            if not str(filepath).startswith(str(SITE_ROOT.resolve())):
                return self._json({"error": "forbidden"}, 403)
        except (ValueError, OSError):
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py quiet except scope=PortalHandler.do_GET reason=return self._json({\"error\": \"forbidden\"}, 403)")
            return self._json({"error": "forbidden"}, 403)

        if filepath.is_file():
            ext = filepath.suffix.lower()
            ctype = MIME_TYPES.get(ext, "application/octet-stream")
            try:
                data = filepath.read_bytes()
                etag = self._etag(data)
                if self.headers.get("If-None-Match") == etag:
                    self.send_response(304)
                    self.send_header("ETag", etag)
                    self.send_header("Cache-Control", "no-cache" if filepath.name == "index.html" else "public, max-age=3600, must-revalidate")
                    self.end_headers()
                    return
                self.send_response(200)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(data)))
                self.send_header("ETag", etag)
                self._send_same_origin_cors()
                self.send_header("Cache-Control", "no-cache" if filepath.name == "index.html" else "public, max-age=3600, must-revalidate")
                self.end_headers()
                self.wfile.write(data)
            except OSError as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py quiet except scope=PortalHandler.do_GET reason=Expr")
                self._json({"error": f"read error: {e}"}, 500)
        else:
            self._json({"error": f"not found: {path}"}, 404)

    # ── helpers ──

    def _json(self, data: dict, status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._send_same_origin_cors()
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, default=str).encode())

    @staticmethod
    def _etag(data: bytes) -> str:
        return '"' + hashlib.sha256(data).hexdigest() + '"'

    def _json_cached(self, data: dict) -> None:
        payload = json.dumps(data, ensure_ascii=False, default=str, sort_keys=True).encode()
        etag = self._etag(payload)
        if self.headers.get("If-None-Match") == etag:
            self.send_response(304)
            self.send_header("ETag", etag)
            self.send_header("Cache-Control", "private, max-age=1, must-revalidate")
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("ETag", etag)
        self.send_header("Cache-Control", "private, max-age=1, must-revalidate")
        self._send_same_origin_cors()
        self.end_headers()
        self.wfile.write(payload)

    def _same_origin(self) -> str | None:
        """Return Origin only when it exactly matches this HTTP endpoint."""
        origin = self.headers.get("Origin")
        host = self.headers.get("Host")
        if not origin or not host:
            return None
        expected = f"http://{host}"
        return origin if origin.rstrip("/") == expected else None

    def _send_same_origin_cors(self) -> None:
        origin = self._same_origin()
        if origin:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")

    def log_message(self, fmt: str, *args: Any) -> None:
        t = time.strftime("%H:%M:%S")
        safe = " ".join(str(a) for a in args) if args else fmt
        sys.stderr.write(f"[portal] {t} {safe}\n")

    def _method_not_allowed(self, path: str) -> None:
        return self._json({
            "status": "method_not_allowed",
            "error": "direct mutation route is disabled",
            "method": self.command,
            "path": path,
            "required_flow": [
                "/api/operations/plan",
                "/api/operations/confirm",
            ],
        }, 405)

    def do_POST(self):
        path = self.path.split("?")[0].rstrip("/")

        if path == "/api/operations/plan":
            payload, status = plan_operation(self._read_body())
            return self._json(payload, status)

        if path == "/api/operations/confirm":
            payload, status = confirm_operation(self._read_body(), self.headers.get("Authorization", ""))
            return self._json(payload, status)

        if path == "/api/cielingo/chat":
            try:
                body = self._read_body()
                message = body.get("message")
                session_id = body.get("session_id")

                if not isinstance(message, str) or not message.strip():
                    return self._json({"ok": False, "status": "invalid_request", "errors": ["message must be a nonempty string"]}, 400)
                if not isinstance(session_id, str) or not session_id.strip():
                    return self._json({"ok": False, "status": "invalid_request", "errors": ["session_id must be supplied as a nonempty string"]}, 400)
                session_id = session_id.strip()
                if len(session_id) > 128:
                    return self._json({"ok": False, "status": "invalid_request", "errors": ["session_id exceeds 128 characters"]}, 400)

                resp_text, frame_data, headless_error = request_ciel_headless(message, session_id)

                if not isinstance(resp_text, str):
                    return self._json({"ok": False, "status": "backend_unavailable", "errors": [headless_error or "no response from ciel_headless_daemon"]}, 503)

                if resp_text.strip():
                    threading.Thread(
                        target=_ingest_headless_turn,
                        args=(message, resp_text, session_id),
                        daemon=True,
                    ).start()

                # Read CIEL's emotional state
                ciel_state = _read_ciel_state()
                try:
                    from ciel_geometry.noema_surface_mmap import open_surface, read_surface_state
                    # An empty headless frame and empty CIEL state mean that
                    # this response has no coupled diagnostic snapshot.  Do
                    # not attach an unrelated/stale shared surface to it.
                    # This keeps missing diagnostics explicitly unavailable
                    # instead of manufacturing a partial chat context.
                    if isinstance(frame_data, dict) and frame_data or ciel_state:
                        sf = open_surface(mode="r")
                        sf_state = read_surface_state(sf) if sf else {}
                    else:
                        sf_state = {}
                except Exception:
                    sf_state = {}

                # Always use the headless response (it's CIEL's cognitive output)
                response_text = resp_text
                diagnostics = build_chat_diagnostics(sf_state, ciel_state, frame_data)

                # Save to thread memory
                ts = time.time()
                try:
                    context_metadata = _bounded_context_metadata(diagnostics)
                    _append_thread_journal([
                        _thread_journal_entry(
                            timestamp=ts,
                            session_id=session_id,
                            role="user",
                            content=message,
                            context_metadata=context_metadata,
                        ),
                        _thread_journal_entry(
                            timestamp=ts + 0.001,
                            session_id=session_id,
                            role="assistant",
                            content=response_text,
                            context_metadata=context_metadata,
                        ),
                    ])
                except Exception:
                    _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py quiet except scope=terminal_monitor_write reason=append_failed")

                cielingo_frame = copy.deepcopy(diagnostics)
                for key in ("coherence", "soul", "ethics", "mood"):
                    cielingo_frame[key] = _round_optional(cielingo_frame[key], 4)

                return self._json({
                    "ok": True,
                    "data": {
                        "response": response_text,
                        "cielingo_frame": cielingo_frame,
                        "ciel_state": ciel_state,
                    }
                })
            except Exception as e:
                return self._json({"ok": False, "status": "error", "errors": [str(e)]}, 500)

        if path == "/api/settings":
            try:
                body = self._read_body()
                patch = body.get("patch", {})
                if not isinstance(patch, dict):
                    return self._json({"ok": False, "errors": ["patch must be an object"]}, 400)
                config_path = NOEMA_ROOT / "noema_config.json"
                if not config_path.exists():
                    return self._json({"ok": False, "errors": ["noema_config.json not found"]}, 404)
                cfg = json.loads(config_path.read_text(encoding="utf-8"))
                # Deep merge: only update leaves that exist in the config
                def deep_merge(base, updates):
                    for k, v in updates.items():
                        if k in base and isinstance(base[k], dict) and isinstance(v, dict):
                            deep_merge(base[k], v)
                        elif k in base:
                            base[k] = v
                deep_merge(cfg, patch)
                config_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
                return self._json({"ok": True, "saved": True, "source": str(config_path)})
            except Exception as e:
                return self._json({"ok": False, "errors": [str(e)]}, 500)

        if path == "/api/daemon/control":
            try:
                body = self._read_body()
                action = body.get("action", "")
                service = body.get("service", "")
                ALLOWED_ACTIONS = {"start", "stop", "restart", "start_all", "stop_all", "status_all"}
                ALLOWED_SERVICES = {
                    "noema-agent-backend", "noema-analog-blend", "noema-archiver",
                    "noema-cielingo-sync", "noema-codex-fifo-bridge", "noema-consolidator",
                    "noema-doctor", "noema-headless", "noema-kuramoto", "noema-linux-sensor",
                    "noema-neutrino", "noema-nonlocal-proxy", "noema-phasenav-hot",
                    "noema-portal", "noema-resonance", "noema-subconscious",
                    "noema-surface-init", "noema-watchdog", "noema-web-research",
                }
                ALL_ORDERED = [
                    "noema-surface-init", "noema-kuramoto", "noema-nonlocal-proxy",
                    "noema-resonance", "noema-analog-blend", "noema-neutrino",
                    "noema-subconscious", "noema-consolidator", "noema-archiver",
                    "noema-linux-sensor", "noema-phasenav-hot", "noema-cielingo-sync",
                    "noema-codex-fifo-bridge", "noema-agent-backend", "noema-web-research",
                    "noema-headless", "noema-portal", "noema-doctor", "noema-watchdog",
                ]
                if action not in ALLOWED_ACTIONS:
                    return self._json({"ok": False, "errors": [f"unknown action: {action}"]}, 400)
                import subprocess as _sp
                results = []
                if action in ("start_all", "stop_all"):
                    svcs = ALL_ORDERED if action == "start_all" else list(reversed(ALL_ORDERED))
                    for svc in svcs:
                        act = "start" if action == "start_all" else "stop"
                        r = _sp.run(["systemctl", "--user", act, svc], capture_output=True, text=True)
                        results.append({"service": svc, "rc": r.returncode, "stderr": r.stderr.strip()})
                    return self._json({"ok": True, "action": action, "results": results})
                if action == "status_all":
                    for svc in ALL_ORDERED:
                        r = _sp.run(["systemctl", "--user", "is-active", svc], capture_output=True, text=True)
                        results.append({"service": svc, "active": r.stdout.strip()})
                    return self._json({"ok": True, "services": results})
                if service not in ALLOWED_SERVICES:
                    return self._json({"ok": False, "errors": [f"unknown service: {service}"]}, 400)
                r = _sp.run(["systemctl", "--user", action, service], capture_output=True, text=True)
                return self._json({"ok": r.returncode == 0, "service": service, "action": action,
                                   "rc": r.returncode, "stderr": r.stderr.strip()})
            except Exception as e:
                return self._json({"ok": False, "status": "error", "errors": [str(e)]}, 500)

        return self._method_not_allowed(path)

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_same_origin_cors()
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Max-Age", "86400")
        self.end_headers()

    def do_PUT(self):
        path = self.path.split("?")[0].rstrip("/")
        return self._method_not_allowed(path)

    def do_DELETE(self):
        path = self.path.split("?")[0].rstrip("/")
        return self._method_not_allowed(path)

# ─── Registry helpers ───────────────────────────────────────────────────

def scan_registry() -> list[dict[str, Any]]:
    """Składa daemon registry.

    Źródło prawdy: NoemaRegistry na /dev/shm/ciel_noema/registry/*.json (nreg,
    ten sam rejestr, do którego ten portal sam wysyła heartbeat — patrz
    heartbeat_loop). Timeout 400s pokrywa też daemony z rzadkim heartbeatem
    (phasenav-cold bije co 300s wg NoemaRegistry.cleanup docstring).

    Legacy ciel_geometry.daemon_registry.Registry (mmap w /tmp) jest osobnym,
    w większości opuszczonym mechanizmem — prawie nic już do niego nie pisze,
    stąd pokazywał count=1 (tylko dual-sync). Dołączamy go jako dodatkowe
    źródło (deduplikowane po pid), żeby nie zgubić daemonów, które z jakiegoś
    powodu wciąż używają starego API, ale primary jest nreg.
    """
    now = time.time()
    seen_pids: set[int] = set()
    results: list[dict[str, Any]] = []

    try:
        for payload in nreg.list_active(timeout=400.0):
            pid = int(payload.get("pid", 0))
            if pid <= 0 or pid in seen_pids:
                continue
            seen_pids.add(pid)
            started_at = float(payload.get("started_at", now))
            heartbeat_at = float(payload.get("heartbeat_at", now))
            results.append({
                "name": payload.get("name", "?"),
                "pid": pid,
                "status": "running" if (now - heartbeat_at) < 30.0 else "stale",
                "alive": (now - heartbeat_at) < 400.0,
                "uptime": round(now - started_at, 1),
                "surface_claims": payload.get("surface_claims", []),
                "source": "noema_registry",
            })
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py:scan_registry nreg source failed: %s" % e)

    try:
        from ciel_geometry.daemon_registry import Registry
        with Registry() as reg:
            for d in reg.scan():
                if d.pid <= 0 or d.pid in seen_pids:
                    continue
                seen_pids.add(d.pid)
                results.append({
                    "name": d.name, "pid": d.pid, "status": d.status,
                    "alive": d.alive, "uptime": round(d.uptime, 1) if hasattr(d, 'uptime') else 0,
                    "surface_claims": [],
                    "source": "legacy_mmap_registry",
                })
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py:scan_registry legacy source failed: %s" % e)

    if not results:
        return [{"error": "no daemons found in either registry"}]
    return results

def heartbeat_loop(interval: float = 10.0) -> None:
    """Heartbeat w tle — co interval sekund."""
    while True:
        time.sleep(interval)
        try:
            nreg.heartbeat(reg_token)
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py quiet except scope=heartbeat_loop reason=pass")
            pass  # registry nie jest krytyczny

# ─── Daemon ─────────────────────────────────────────────────────────────

class PortalHTTPServer(http.server.ThreadingHTTPServer):
    """Concurrent portal transport; request workers never hold process exit."""

    allow_reuse_address = True
    daemon_threads = True

def run_daemon(port: int = PORT, host: str = HOST) -> None:
    global start_time, surface
    start_time = time.time()

    # Init surface
    init_noema()

    # The portal is a read-only observer.  Registry writes belong to the
    # daemon that owns a runtime instance, not to an HTTP request server.
    reg_token = None
    print("[portal] registry registration skipped: read-only observer", file=sys.stderr)

    # HTTP server
    server = PortalHTTPServer((host, port), PortalHandler)
    server.server_name = "noema_portal"
    server.server_port = port
    print(f"[portal] listening on {host}:{port}", file=sys.stderr)
    print(f"[portal] serving static from {SITE_ROOT}", file=sys.stderr)

    running = True

    def _stop(signum, frame):
        nonlocal running
        print(f"[portal] stopping (signal {signum})", file=sys.stderr)
        running = False

    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)

    server.timeout = 0.5
    try:
        while running:
            server.handle_request()
    except KeyboardInterrupt:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py quiet except scope=run_daemon reason=assign_fallback")
        running = False
    except Exception as e:
        print(f"[portal] error in loop: {e}", file=sys.stderr)
    finally:
        if reg_token is not None:
            try:
                nreg.unregister("portal")
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_portal_daemon.py registry unregister failed")
        server.server_close()
        print("[portal] stopped", file=sys.stderr)

if __name__ == "__main__":
    port = PORT
    host = HOST
    for i, a in enumerate(sys.argv):
        if a == "--port" and i + 1 < len(sys.argv):
            port = int(sys.argv[i + 1])
        elif a == "--host" and i + 1 < len(sys.argv):
            host = sys.argv[i + 1]
    run_daemon(port, host)
