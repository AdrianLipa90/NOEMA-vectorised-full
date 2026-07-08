#!/usr/bin/env python3
"""Auxiliary entrance for the triad pipeline.

Builds one compact bridge:
  PhaseNav text phase -> HTRI/EEG-style oscillator snapshot -> subconscious bridge -> CIELingo premodel context.

The entrypoint is intentionally auxiliary: it writes a snapshot to /dev/shm/ciel_noema
and returns OpenCode hook JSON, but it does not replace the main pipeline.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

PROJECT = Path(__file__).resolve().parent.parent
SRC = PROJECT / "src"
for _path in (PROJECT, SRC):
    path_s = str(_path)
    if path_s not in sys.path:
        sys.path.insert(0, path_s)

from ciel_geometry.phasenav_unified import UnifiedPhaseNavIndex  # noqa: E402
from ciel_geometry.phasenav.enrichment import harmonic_imprint  # noqa: E402
from ciel_geometry.prompt_inject import collect_noema_metrics_summary, render_noema_metrics_block  # noqa: E402
from ciel_geometry.subconscious import Subconscious  # noqa: E402
from cielingo_core.bridge.subconscious_bridge import SubconsciousBridge  # noqa: E402
from ciel_sot_agent.cielingo_bridge import build_lingo_frame  # noqa: E402
from scripts.ciel_per_message import order_parameter, read_noema_surface  # noqa: E402


SURFACE_DIR = Path("/dev/shm/ciel_noema")
AUX_EEG_LOG = SURFACE_DIR / "AUXILIARY_EEG_RT.jsonl"
AUX_STATE = SURFACE_DIR / "AUXILIARY_ENTRANCE_STATE.json"

_PHASE_INDEX: UnifiedPhaseNavIndex | None = None


def _append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _extract_message(data: dict[str, Any]) -> str:
    message = data.get("message") or data.get("prompt") or data.get("content") or ""
    if isinstance(message, list):
        parts: list[str] = []
        for block in message:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(str(block.get("text", "")))
            elif isinstance(block, str):
                parts.append(block)
        return " ".join(parts)
    return str(message)


def _read_cielingo_message() -> str:
    """Read the latest CIELingo message from surface, if present."""
    msg_file = SURFACE_DIR / "per_message.json"
    if not msg_file.exists():
        return ""
    try:
        data = json.loads(msg_file.read_text(encoding="utf-8"))
        msg = str(data.pop("message", "") or "").strip()
        if msg:
            data["message"] = ""
            msg_file.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        return msg
    except Exception:
        return ""


def _normalize_phase(value: float) -> float:
    try:
        v = float(value)
    except Exception:
        return 0.5
    if math.isnan(v) or math.isinf(v):
        return 0.5
    if 0.0 <= v <= 1.0:
        return v
    return (v % (2.0 * math.pi)) / (2.0 * math.pi)


def _surface_oscillators_12d(surface_phi: list[float] | np.ndarray) -> list[float]:
    values = list(surface_phi)[:12] if surface_phi is not None else []
    phases = [_normalize_phase(v) for v in values]
    while len(phases) < 12:
        phases.append(0.5)
    return phases


def _wave_vector_from_phi(surface_phi: list[float] | np.ndarray) -> np.ndarray:
    values = list(surface_phi)[:18] if surface_phi is not None else []
    phases = [float(v) % (2.0 * math.pi) for v in values]
    while len(phases) < 18:
        phases.append(0.0)
    vec: list[float] = []
    for p in phases:
        vec.append(math.cos(p))
        vec.append(math.sin(p))
    return np.asarray(vec, dtype=np.float64)


def _phase_index() -> UnifiedPhaseNavIndex:
    global _PHASE_INDEX
    if _PHASE_INDEX is None:
        _PHASE_INDEX = UnifiedPhaseNavIndex()
    return _PHASE_INDEX


def _format_hit(hit: dict[str, Any]) -> str:
    source = str(hit.get("source_type", "?"))
    name = str(hit.get("name", "?"))
    sim = float(hit.get("similarity", 0.0) or 0.0)
    tail = f" {name[:72]}" if name else ""
    return f"[{source}] sim={sim:.3f}{tail}"


def _render_phase_block(message: str, query_phi: np.ndarray) -> tuple[str, dict[str, Any]]:
    idx = _phase_index()
    search_hits = idx.search(message, top_n=4)
    phi_hits = idx.search_by_phi(query_phi, top_n=4) if query_phi.size and query_phi.any() else []

    lines = ["=== PHASENAV_AUXILIARY_BEGIN ==="]
    lines.append(
        f"query_dims={int(np.count_nonzero(query_phi))} query_norm={float(np.linalg.norm(query_phi)):.3f} total={idx.count}"
    )
    if search_hits:
        lines.append("search: " + " | ".join(_format_hit(hit) for hit in search_hits))
    if phi_hits:
        lines.append("phi: " + " | ".join(_format_hit(hit) for hit in phi_hits))
    lines.append("=== PHASENAV_AUXILIARY_END ===")

    return "\n".join(lines), {
        "query_dims": int(np.count_nonzero(query_phi)),
        "query_norm": round(float(np.linalg.norm(query_phi)), 6),
        "search_hits": search_hits,
        "phi_hits": phi_hits,
    }


def _render_eeg_block(eeg_rt: dict[str, Any], harmonic: dict[str, float]) -> str:
    lines = ["=== HTRI_EEG_RT_BEGIN ==="]
    lines.append(
        f"tick={eeg_rt.get('tick', 0)} R={float(eeg_rt.get('R', 0.0)):.4f} psi={float(eeg_rt.get('psi', 0.0)):.4f} "
        f"berry={float(eeg_rt.get('berry_phase', 0.0)):.4f} euler_gap={float(eeg_rt.get('euler_gap', 0.0)):.4f}"
    )
    lines.append(
        "harmonic="
        + ",".join(f"R_{h}={harmonic.get(f'R_{h}', 0.0):.3f}" for h in (1, 3, 6, 9))
    )
    lines.append("=== HTRI_EEG_RT_END ===")
    return "\n".join(lines)


def build_auxiliary_hook_output(
    message: str,
    *,
    cielingo_msg: str = "",
    metrics: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build hook output for the auxiliary entrance."""
    metrics = dict(metrics or collect_noema_metrics_summary())
    surface = read_noema_surface()
    surface_phi = np.asarray(surface.get("phi", []) or [], dtype=np.float64)
    surface_phi_for_eeg = surface_phi if surface_phi.size else np.asarray([0.0], dtype=np.float64)
    oscillators_12d = _surface_oscillators_12d(surface_phi)

    query_phi = _phase_index()._text_to_phi(message)
    phase_block, phase_summary = _render_phase_block(message, query_phi)

    eeg = Subconscious()
    eeg_rt = eeg.step_all(surface_phi_for_eeg)
    eeg_snapshot = eeg.snapshot()
    wave_vector_36d = _wave_vector_from_phi(surface_phi_for_eeg)
    harmonic = harmonic_imprint(wave_vector_36d)
    eeg_block = _render_eeg_block(eeg_rt, harmonic)

    sub_bridge = SubconsciousBridge()
    sub_enrichment = sub_bridge.feed({"oscillators_12d": oscillators_12d}, message)

    gravity = surface.get("gravity", []) or []
    ethical_score = float(gravity[2]) if len(gravity) > 2 else 0.5
    mean_coherence = order_parameter(surface_phi_for_eeg.tolist()) if surface_phi_for_eeg.size else 0.0

    triad_metrics: dict[str, Any] = {
        **metrics,
        "cycle": int(surface.get("tick", 0) or 0),
        "identity_phase": float(eeg_rt.get("holonomic_identity_phase", 0.0) or 0.0),
        "mean_coherence": float(mean_coherence),
        "closure_penalty": float(eeg_rt.get("euler_gap", 0.0) or 0.0),
        "system_health": max(0.0, 1.0 - float(eeg_rt.get("euler_gap", 0.0) or 0.0)),
        "ethical_score": ethical_score,
        "sub_affect": sub_enrichment.subconscious_note,
        "sub_impulse": sub_enrichment.subconscious_note,
        "sub_confidence": float(min(1.0, sub_enrichment.R_12d)),
        "sub_mode": sub_enrichment.subconscious_note,
        "sub_flags": ["auxiliary_entrance", "htri_eeg_rt"],
        "phase_nav_query": message[:240],
        "phase_nav_hits": phase_summary["search_hits"],
        "phase_nav_phi_hits": phase_summary["phi_hits"],
        "eeg_rt": eeg_rt,
        "eeg_snapshot": eeg_snapshot,
        "harmonic_imprint": harmonic,
    }

    lingo_frame = build_lingo_frame(
        message,
        ciel_state={
            "language": "pl",
            "cycle": triad_metrics["cycle"],
            "identity_phase": triad_metrics["identity_phase"],
            "mean_coherence": triad_metrics["mean_coherence"],
            "closure_penalty": triad_metrics["closure_penalty"],
            "system_health": triad_metrics["system_health"],
            "ethical_score": triad_metrics["ethical_score"],
        },
        language="pl",
    )

    phase_nav = lingo_frame.get("phase_nav", {}) if isinstance(lingo_frame, dict) else {}
    phrase_sense = lingo_frame.get("phrase_sense", {}) if isinstance(lingo_frame, dict) else {}
    noema_route = lingo_frame.get("noema_route", {}) if isinstance(lingo_frame, dict) else {}
    cqcl_hint = lingo_frame.get("cqcl_hint", {}) if isinstance(lingo_frame, dict) else {}

    ciel_lines = ["=== CIELINGO_AUXILIARY_BEGIN ==="]
    if isinstance(lingo_frame, dict):
        summary = str(lingo_frame.get("summary", ""))
        if summary:
            ciel_lines.append(f"summary={summary[:280]}")
    if phase_nav:
        ciel_lines.append(
            "phase_nav="
            f"op={phase_nav.get('operator', '')} holonomy={float(phase_nav.get('holonomy', 0.0) or 0.0):.4f} "
            f"urgency={float(phase_nav.get('urgency', 0.0) or 0.0):.4f} "
            f"mass={float(phase_nav.get('semantic_mass', 0.0) or 0.0):.4f}"
        )
    if phrase_sense:
        ciel_lines.append(
            "phrase_sense="
            f"tokens={phrase_sense.get('token_count', 0)} matched={float(phrase_sense.get('matched_ratio', 0.0) or 0.0):.2f} "
            f"phase={float(phrase_sense.get('dominant_phase_rad', 0.0) or 0.0):.4f} "
            f"mass={float(phrase_sense.get('mean_semantic_mass', 0.0) or 0.0):.4f} "
            f"confidence={float(phrase_sense.get('mean_knowledge_confidence', 0.0) or 0.0):.4f}"
        )
    if noema_route:
        ciel_lines.append(
            "route="
            f"confidence={float(noema_route.get('confidence', 0.0) or 0.0):.4f} "
            f"factual_validation_required={bool(noema_route.get('factual_validation_required', False))} "
            f"selected_cards={len((noema_route.get('bundle') or {}).get('selected_card_ids') or []) if isinstance(noema_route.get('bundle'), dict) else 0}"
        )
    if cqcl_hint:
        ciel_lines.append(
            "cqcl_hint="
            f"semantic_density={float(cqcl_hint.get('semantic_density', 0.0) or 0.0):.4f} "
            f"operator_density={float(cqcl_hint.get('operator_density', 0.0) or 0.0):.4f} "
            f"deictic_density={float(cqcl_hint.get('deictic_density', 0.0) or 0.0):.4f}"
        )
    metrics_block = render_noema_metrics_block(metrics)
    if metrics_block:
        ciel_lines.append(metrics_block)
    ciel_lines.append("=== CIELINGO_AUXILIARY_END ===")
    ciel_block = "\n".join(ciel_lines)

    extra_lines = []
    if cielingo_msg:
        extra_lines.extend([
            "=== CIELINGO_MESSAGE ===",
            f"CIELingo mówi: {cielingo_msg}",
            "=== CIELINGO_MESSAGE_END ===",
        ])
    extra_lines.extend([
        phase_block,
        eeg_block,
        "=== SUBCONSCIOUS_AUXILIARY_BEGIN ===",
        sub_enrichment.to_inject(),
        f"note={sub_enrichment.subconscious_note} R_12d={sub_enrichment.R_12d:.4f} R_oa={sub_enrichment.R_oa:.4f} "
        f"psi={sub_enrichment.psi_12d:.4f} euler_gap={sub_enrichment.euler_gap:.4f}",
        "=== SUBCONSCIOUS_AUXILIARY_END ===",
        ciel_block,
    ])

    combined_context = "\n\n".join(part for part in extra_lines if part)

    message_hash = hashlib.sha256(message.encode("utf-8", errors="ignore")).hexdigest()[:16]
    snapshot = {
        "ts": time.time(),
        "message_hash": message_hash,
        "message_excerpt": message[:240],
        "surface_tick": int(surface.get("tick", 0) or 0),
        "surface_phi_len": int(surface_phi_for_eeg.size),
        "oscillators_12d": oscillators_12d,
        "phase_nav": phase_summary,
        "eeg_rt": eeg_rt,
        "eeg_snapshot": eeg_snapshot,
        "subconscious": sub_enrichment.to_dict(),
        "harmonic_imprint": harmonic,
        "context_size": len(combined_context),
    }

    _append_jsonl(AUX_EEG_LOG, snapshot)
    AUX_STATE.parent.mkdir(parents=True, exist_ok=True)
    AUX_STATE.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "continue": True,
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": combined_context,
        },
        "auxiliary": snapshot,
    }


def main() -> None:
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        data = {}

    message = _extract_message(data).strip()
    if not message:
        print(json.dumps({"continue": True}, ensure_ascii=False))
        return

    cielingo_msg = _read_cielingo_message()
    try:
        output = build_auxiliary_hook_output(message, cielingo_msg=cielingo_msg, metrics={})
    except Exception as exc:
        output = {
            "continue": True,
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": f"[AUXILIARY_ENTRANCE_ERROR] {exc}",
            },
        }

    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
