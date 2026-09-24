from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

# CIEL ORBITAL BINDING — hardcoded, immutable.
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on import of " + __name__)


import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List
import sys
import math
import time

import numpy as np

from .paths import resolve_project_root
from .jokeheal_atlas import build_mnemonic_atlas


def _run_phase_nav_analysis(text: str) -> dict[str, Any]:
    """Run PhaseNav Language analyze_prompt, return results dict or empty."""
    try:
        from ciel_geometry.phase_nav_lang import analyze_prompt  # noqa: PLC0415
        result = analyze_prompt(text)
        return {
            "operator": result.get("operator"),
            "connections": result.get("connections"),
            "holonomy": result.get("holonomy"),
            "urgency": result.get("urgency"),
            "semantic_mass": result.get("semantic_mass"),
            "vector_36d": result.get("vector_36d", result.get("vector_24d")),
        }
    except Exception as exc:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_sot_agent/cielingo_bridge.py:36 quiet except scope=_run_phase_nav_analysis reason=return {\"_error\": str(exc)}")
        return {"_error": str(exc)}


def _phase_sense_from_phasenav(text: str, tokens: list[str], phase_nav: dict[str, Any]) -> dict[str, Any]:
    """Build phrase_sense-compatible metrics from PhaseNav 36D."""
    vector = np.asarray(phase_nav.get("vector_36d") or [], dtype=np.float64)
    if vector.size != 36:
        vector = np.zeros(36, dtype=np.float64)
    phases = np.mod((vector + 1.0) * math.pi, 2.0 * math.pi)
    abs_v = np.abs(vector)
    connections = phase_nav.get("connections", {}) if isinstance(phase_nav.get("connections"), dict) else {}
    confidence = max(
        0.0,
        min(
            1.0,
            0.50
            + 0.18 * abs(float(connections.get("MEMORY", 0.0) or 0.0))
            + 0.14 * abs(float(connections.get("SOURCE", 0.0) or 0.0))
            + 0.10 * abs(float(connections.get("IDENTITY", 0.0) or 0.0))
            - 0.08 * min(1.0, abs(float(phase_nav.get("urgency", 0.0) or 0.0))),
        ),
    )
    token_rows: list[dict[str, Any]] = []
    for i, token in enumerate(tokens):
        idx = i % 36
        mass = float(abs_v[idx]) if vector.size else 0.0
        density = max(0.0, min(1.0, 0.35 + 0.65 * mass))
        viscosity = max(0.0, min(1.0, 0.5 + 0.5 * float(vector[(idx + 12) % 36] if vector.size else 0.0)))
        saturation = max(0.0, min(1.0, 0.5 + 0.5 * float(vector[(idx + 24) % 36] if vector.size else 0.0)))
        resistance = max(0.0, min(1.0, 0.50 * viscosity + 0.25 * density + 0.25 * min(1.0, abs(float(phase_nav.get("urgency", 0.0) or 0.0)))))
        thinning = max(0.0, min(1.0, (1.0 - resistance) * (0.45 + 0.55 * confidence)))
        token_rows.append(
            {
                "surface": token,
                "normalized": token.lower(),
                "matched": True,
                "card_id": f"phasenav:{phase_nav.get('operator', 'IDENTITY')}:{idx}",
                "card_kind": "PHASENAV_VECTOR_TOKEN",
                "canonical_label": token,
                "semantic_axes": [round(float(x), 9) for x in vector[idx:idx + 3].tolist()],
                "semantic_mass": round(mass, 9),
                "phase_rad": round(float(phases[idx]), 9),
                "phase_sense_label": "phasenav_vector_phase_sense",
                "scalar_density": round(density, 9),
                "scalar_viscosity": round(viscosity, 9),
                "scalar_saturation": round(saturation, 9),
                "semantic_time_resistance": round(resistance, 9),
                "semantic_time_thinning": round(thinning, 9),
                "knowledge_confidence": round(confidence, 9),
                "parse_status": "phasenav_vectorized",
                "supervision_required": confidence < 0.62,
            }
        )

    def mean(key: str) -> float:
        if not token_rows:
            return 0.0
        return round(sum(float(row.get(key, 0.0) or 0.0) for row in token_rows) / len(token_rows), 9)

    if token_rows:
        sin_sum = sum(math.sin(float(row["phase_rad"])) for row in token_rows)
        cos_sum = sum(math.cos(float(row["phase_rad"])) for row in token_rows)
        dominant = math.atan2(sin_sum, cos_sum)
        if dominant < 0.0:
            dominant += 2.0 * math.pi
    else:
        dominant = float(phase_nav.get("holonomy", 0.0) or 0.0) % (2.0 * math.pi)

    return {
        "tokens": token_rows,
        "token_count": len(token_rows),
        "matched_ratio": 1.0 if token_rows else 0.0,
        "dominant_phase_rad": round(float(dominant), 9),
        "mean_semantic_mass": mean("semantic_mass"),
        "mean_density": mean("scalar_density"),
        "mean_viscosity": mean("scalar_viscosity"),
        "mean_saturation": mean("scalar_saturation"),
        "mean_semantic_time_resistance": mean("semantic_time_resistance"),
        "mean_semantic_time_thinning": mean("semantic_time_thinning"),
        "mean_knowledge_confidence": round(confidence, 9),
        "source_role": "phasenav_vectorized_phrase_sense",
        "input_text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
    }


_LINGO_CACHE: dict[str, tuple[float, dict[str, Any]]] = {}
_LINGO_CACHE_TTL = 300  # 5 minutes


_LINGO_ROOT_SUBPATH = Path("src") / "ciel_lingophysics_lns_repo_v2_3" / "src"
_STOPWORDS = {
    "a", "an", "and", "are", "as", "be", "because", "by", "do", "does", "for",
    "from", "have", "has", "i", "if", "in", "is", "it", "its", "me", "my", "of",
    "on", "or", "our", "the", "their", "then", "there", "this", "that", "to",
    "we", "what", "when", "where", "which", "who", "why", "you",
    "albo", "bo", "by", "czy", "dla", "do", "gdy", "gdyż", "i", "jeśli", "jak",
    "jest", "lub", "na", "nie", "o", "od", "po", "przez", "się", "to", "tu",
    "w", "we", "z", "za", "że",
}
_RELATIVE_DEICTICS = {
    "here": ("space", "Here"),
    "there": ("space", "There"),
    "now": ("time", "Now"),
    "then": ("time", "Then"),
    "this": ("discourse", "This"),
    "that": ("discourse", "That"),
    "tu": ("space", "Here"),
    "tutaj": ("space", "Here"),
    "tam": ("space", "There"),
    "teraz": ("time", "Now"),
    "wtedy": ("time", "Then"),
}
_FUNCTION_WORDS = {
    "and", "or", "if", "then", "because", "when", "while", "how", "what", "where",
    "who", "why", "to", "of", "in", "on", "for", "with", "without", "not",
    "i", "lub", "albo", "jeśli", "gdy", "kiedy", "jak", "czy", "dlaczego", "gdzie",
    "po", "przed", "do", "z", "w", "na", "nad", "pod", "przez",
}
_PHASE_TARGETS = {
    "Here": 0.0,
    "Now": 0.0,
    "This": 0.0,
    "There": math.pi,
    "Then": math.pi,
    "That": math.pi,
    "Somewhere": math.pi / 2.0,
    "Sometime": math.pi / 2.0,
    "Somehow": math.pi / 2.0,
    "Anywhere": 3.0 * math.pi / 2.0,
    "Anytime": 3.0 * math.pi / 2.0,
    "Never": math.pi,
}


def _ensure_lingophysics_on_path(root: Path) -> Path:
    lingo_src = (root / _LINGO_ROOT_SUBPATH).resolve()
    if lingo_src.exists():
        lingo_str = str(lingo_src)
        if lingo_str not in sys.path:
            sys.path.insert(0, lingo_str)
    return lingo_src


def _normalize_tokens(text: str) -> List[str]:
    try:
        from lingophysics.noema_index import tokenize  # noqa: PLC0415

        return tokenize(text)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_sot_agent/cielingo_bridge.py:185 quiet except scope=_normalize_tokens reason=return [tok.lower() for tok in text.split() if tok.strip()]")
        return [tok.lower() for tok in text.split() if tok.strip()]


def _detect_deictic_frame(tokens: List[str], *, deictic_context: Dict[str, Any] | None = None) -> Dict[str, Any]:
    try:
        from lingophysics.dynamic_deixis import (  # noqa: PLC0415
            classify_dynamic_surface,
            is_false_precision,
            resolve_dynamic_anchor,
        )
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_sot_agent/cielingo_bridge.py:196 quiet except scope=_detect_deictic_frame reason=no_log_no_raise")
        classify_dynamic_surface = None  # type: ignore[assignment]
        is_false_precision = None  # type: ignore[assignment]
        resolve_dynamic_anchor = None  # type: ignore[assignment]

    anchors: List[Dict[str, Any]] = []
    unresolved: List[str] = []
    false_precision_risk = 0.0
    for token in tokens:
        classified = classify_dynamic_surface(token) if classify_dynamic_surface else None
        if not classified:
            continue
        try:
            anchor = resolve_dynamic_anchor(classified, context=deictic_context or {}) if resolve_dynamic_anchor else None
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_sot_agent/cielingo_bridge.py:210 quiet except scope=_detect_deictic_frame reason=assign_fallback")
            anchor = None
        if anchor is None:
            continue
        anchor_dict = {
            "surface": token,
            "operator": anchor.operator,
            "domain": anchor.domain,
            "variable": anchor.variable,
            "equation": anchor.equation,
            "resolution_state": anchor.resolution_state,
            "false_precision_risk": float(anchor.false_precision_risk),
        }
        if anchor.resolution_state != "resolved":
            unresolved.append(anchor.operator)
        if is_false_precision and is_false_precision(anchor, rendered_as_precise=False):
            false_precision_risk = max(false_precision_risk, float(anchor.false_precision_risk))
        anchors.append(anchor_dict)

    relative: List[Dict[str, Any]] = []
    for token in tokens:
        info = _RELATIVE_DEICTICS.get(token)
        if not info:
            continue
        domain, operator = info
        relative.append(
            {
                "surface": token,
                "operator": operator,
                "domain": domain,
                "resolution_state": "relative_anchor",
                "false_precision_risk": 0.25,
            }
        )

    return {
        "anchors": anchors,
        "relative_anchors": relative,
        "unresolved": list(dict.fromkeys(unresolved)),
        "false_precision_risk": round(false_precision_risk, 4),
        "anchor_count": len(anchors) + len(relative),
    }


def _ensure_language_cards(repo_root: Path | None = None) -> tuple[list, list, dict]:
    cards_concept: list = []
    cards_operator: list = []
    pl_db_dict: dict = {}
    try:
        root = repo_root or resolve_project_root(Path(__file__))
        from cielingo.lns_language_cards import load_lns_concept_cards, load_lns_operator_cards
        cards_concept = load_lns_concept_cards(root)
        cards_operator = load_lns_operator_cards(root)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/cielingo_bridge.py:264 scope=_ensure_language_cards")
        raise
    try:
        from cielingo.polish.linguistic_database import load_polish_database
        pl_db = load_polish_database(root)
        pl_db_dict = {form.lower(): lex.lemma for lex in pl_db.lexemes for form in lex.forms}
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/cielingo_bridge.py:271 scope=_ensure_language_cards_polish")
        raise
    return cards_concept, cards_operator, pl_db_dict


def _detect_operator_tokens(tokens: List[str]) -> List[str]:
    operators: List[str] = []
    root = resolve_project_root(Path(__file__))
    _, op_cards, _ = _ensure_language_cards(root)
    op_labels: set[str] = set()
    for card in op_cards:
        for lang_labels in card.languages.values():
            for lbl in lang_labels:
                op_labels.add(lbl.lower())
    for token in tokens:
        if token in _FUNCTION_WORDS:
            operators.append(token)
            continue
        if token.lower() in op_labels:
            operators.append(token)
            continue
        if token.endswith(("ing", "ed")) and len(token) > 4:
            operators.append(token)
    return operators


def _detect_concept_tokens(tokens: List[str]) -> List[str]:
    concepts: List[str] = []
    root = resolve_project_root(Path(__file__))
    con_cards, _, pl_db = _ensure_language_cards(root)
    card_labels: set[str] = set()
    for card in con_cards:
        for lang_labels in card.languages.values():
            for lbl in lang_labels:
                card_labels.add(lbl.lower())
    for token in tokens:
        if len(token) < 3 or token in _STOPWORDS or token in _FUNCTION_WORDS:
            continue
        concepts.append(token)
        if token.lower() in card_labels:
            continue
        if token.lower() in pl_db:
            continue
    return concepts


def _route_noema(text: str, *, language: str | None, noema_index: Dict[str, Any] | None, noema_policy: Dict[str, Any] | None) -> Dict[str, Any]:
    try:
        from lingophysics.noema_router import detect_unresolved, requires_factual_validation, route_query  # noqa: PLC0415
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_sot_agent/cielingo_bridge.py:277 quiet except scope=_route_noema reason=no_log_no_raise")
        detect_unresolved = None  # type: ignore[assignment]
        requires_factual_validation = None  # type: ignore[assignment]
        route_query = None  # type: ignore[assignment]

    if noema_index and noema_policy and route_query:
        route = route_query(text, noema_index, noema_policy, language=language)
    else:
        unresolved = detect_unresolved(text) if detect_unresolved else []
        factual = requires_factual_validation(text) if requires_factual_validation else False
        confidence = max(0.0, 0.62 - 0.12 * len(unresolved) - (0.12 if factual else 0.0))
        route = {
            "query": text,
            "language": language,
            "retrieved": [],
            "bundle": {
                "selected_card_ids": [],
                "selected_refs": [],
                "operator_hooks": [],
                "domains": [],
                "context_size": 0,
            },
            "unresolved": unresolved,
            "confidence": round(confidence, 4),
            "factual_validation_required": factual,
        }
    return route


def render_lingo_summary(frame: Dict[str, Any], *, max_items: int = 4) -> str:
    concepts = ", ".join(frame.get("concept_tokens", [])[:max_items])
    operators = ", ".join(frame.get("operator_tokens", [])[:max_items])
    deictic_bits = []
    for item in (frame.get("deictic_frame", {}).get("anchors", []) or [])[:max_items]:
        deictic_bits.append(f"{item.get('operator')}:{item.get('resolution_state')}")
    for item in (frame.get("deictic_frame", {}).get("relative_anchors", []) or [])[:max_items]:
        deictic_bits.append(f"{item.get('operator')}:{item.get('surface')}")
    unresolved = ", ".join(frame.get("unresolved", [])[:max_items])
    route = frame.get("noema_route", {})
    conf = float(route.get("confidence", frame.get("projection_confidence", 0.0)) or 0.0)
    factual = "yes" if route.get("factual_validation_required") else "no"
    atlas = frame.get("mnemonic_atlas", {}) if isinstance(frame.get("mnemonic_atlas"), dict) else {}
    mnemonic_pressure = float(atlas.get("mnemonic_pressure", 0.0) or 0.0)
    return (
        f"CIELingo|concepts={concepts or '-'}|operators={operators or '-'}"
        f"|deictic={';'.join(deictic_bits) or '-'}|unresolved={unresolved or '-'}"
        f"|factual={factual}|noema_conf={conf:.3f}|mnemonic_pressure={mnemonic_pressure:.3f}"
    )


def render_phasenav_summary(frame: Dict[str, Any]) -> str:
    phase_nav = frame.get("phase_nav", {}) if isinstance(frame.get("phase_nav"), dict) else {}
    route = frame.get("noema_route", {}) if isinstance(frame.get("noema_route"), dict) else {}
    atlas = frame.get("mnemonic_atlas", {}) if isinstance(frame.get("mnemonic_atlas"), dict) else {}
    return (
        f"PhaseNav|op={phase_nav.get('operator', 'IDENTITY')}"
        f"|holo={float(phase_nav.get('holonomy', 0.0) or 0.0):+.4f}"
        f"|urgency={float(phase_nav.get('urgency', 0.0) or 0.0):.4f}"
        f"|noema_conf={float(route.get('confidence', 0.0) or 0.0):.3f}"
        f"|mnemonic_pressure={float(atlas.get('mnemonic_pressure', 0.0) or 0.0):.3f}"
    )


def build_phasenav_vector_frame(
    text: str,
    *,
    ciel_state: Dict[str, Any] | None = None,
    language: str | None = None,
) -> Dict[str, Any]:
    """Build the memory-facing semantic frame directly from PhaseNav vectors.

    This keeps the old lingo_frame contract for downstream memory code, but
    avoids the heavier Python parser stack in the hot memory path.
    """
    ciel_state = ciel_state or {}
    phase_nav = _run_phase_nav_analysis(text)
    vector = np.asarray(phase_nav.get("vector_36d") or [], dtype=float)
    if vector.size != 36:
        vector = np.zeros(36, dtype=float)

    connections = phase_nav.get("connections", {}) if isinstance(phase_nav.get("connections"), dict) else {}
    abs_conn = {str(k): abs(float(v or 0.0)) for k, v in connections.items()}
    top_ops = [name for name, _ in sorted(abs_conn.items(), key=lambda item: item[1], reverse=True)[:4]]
    operator = str(phase_nav.get("operator") or "IDENTITY")
    concept_tokens = [operator.lower()]
    operator_tokens = [op.lower() for op in top_ops if op]

    memory_conn = abs_conn.get("MEMORY", 0.0)
    source_conn = abs_conn.get("SOURCE", 0.0)
    identity_conn = abs_conn.get("IDENTITY", 0.0)
    risk_conn = abs_conn.get("RISK", 0.0)
    boundary_conn = abs_conn.get("BOUNDARY", 0.0)
    urgency = float(phase_nav.get("urgency", 0.0) or 0.0)
    hol = float(phase_nav.get("holonomy", 0.0) or 0.0)

    confidence = max(
        0.0,
        min(
            1.0,
            0.46
            + 0.18 * memory_conn
            + 0.14 * source_conn
            + 0.14 * identity_conn
            - 0.08 * min(1.0, urgency)
            - 0.06 * risk_conn,
        ),
    )
    unresolved = []
    if risk_conn > 0.72:
        unresolved.append("risk")
    if boundary_conn > 0.78:
        unresolved.append("boundary")

    target_phase = float(hol % (2.0 * math.pi))
    phase_confidence = max(0.0, min(1.0, confidence + 0.08 * memory_conn - 0.05 * len(unresolved)))
    tau_axis = np.linspace(0.0, 1.0, 36, dtype=float)
    vector_gain = float(np.linalg.norm(vector) / 6.0)
    tau_profile = target_phase * tau_axis + 0.25 * vector_gain * np.sin(np.pi * tau_axis)
    tau_gradient = np.gradient(tau_profile)
    tau_curvature = np.gradient(tau_gradient)
    semantic_density = max(0.0, min(1.0, float(np.mean(np.abs(vector))) if vector.size else 0.0))
    imaginal_drive = max(
        0.0,
        min(
            1.0,
            0.30 * semantic_density
            + 0.22 * memory_conn
            + 0.18 * source_conn
            + 0.12 * urgency
            + 0.10 * risk_conn,
        ),
    )
    mnemonic_pressure = max(0.0, min(1.0, 0.55 * memory_conn + 0.25 * identity_conn + 0.20 * semantic_density))
    symbolic_pull = max(0.0, min(1.0, 0.45 * source_conn + 0.35 * identity_conn + 0.20 * memory_conn))
    recurrence_pressure = max(0.0, min(1.0, 0.50 * memory_conn + 0.25 * abs(math.cos(hol)) + 0.25 * identity_conn))

    frame: Dict[str, Any] = {
        "text": text,
        "tokens": operator_tokens or concept_tokens,
        "concept_tokens": concept_tokens,
        "operator_tokens": operator_tokens,
        "deictic_frame": {"anchors": [], "relative_anchors": [], "unresolved": [], "false_precision_risk": 0.0, "anchor_count": 0},
        "unresolved": unresolved,
        "composition_valid": bool(operator),
        "projection_confidence": round(confidence, 4),
        "factual_validation_required": risk_conn > 0.72 or source_conn > 0.80,
        "dialect_variant": ciel_state.get("dialect_variant"),
        "dialect_review_required": bool(ciel_state.get("dialect_review_required", False)),
        "noema_route": {
            "query": text,
            "language": language or ciel_state.get("language"),
            "retrieved": [],
            "bundle": {
                "selected_card_ids": [],
                "selected_refs": [f"phasenav:operator:{operator.lower()}"],
                "operator_hooks": top_ops,
                "domains": ["phasenav", "memory"],
                "context_size": 36,
            },
            "unresolved": unresolved,
            "confidence": round(confidence, 4),
            "factual_validation_required": risk_conn > 0.72 or source_conn > 0.80,
        },
        "mnemonic_atlas": {
            "mnemonic_pressure": round(mnemonic_pressure, 4),
            "symbolic_pull": round(symbolic_pull, 4),
            "recurrence_pressure": round(recurrence_pressure, 4),
        },
        "phrase_sense": {},
        "phase_nav": phase_nav,
        "cqcl_hint": {
            "semantic_density": round(semantic_density, 4),
            "operator_density": round(min(1.0, len(operator_tokens) / 4.0), 4),
            "deictic_density": 0.0,
            "confidence": round(confidence, 4),
        },
        "phase_projection": {
            "target_phase": round(target_phase, 6),
            "target_phase_shift": round(math.atan2(math.sin(target_phase), math.cos(target_phase)), 6),
            "phase_confidence": round(phase_confidence, 4),
            "phase_anchor_count": len(top_ops),
            "phase_domain_count": 2,
        },
        "tau_bridge": {
            "tau_axis": [round(float(x), 6) for x in tau_axis.tolist()],
            "tau_profile": [round(float(x), 6) for x in tau_profile.tolist()],
            "tau_gradient": [round(float(x), 6) for x in tau_gradient.tolist()],
            "tau_curvature": [round(float(x), 6) for x in tau_curvature.tolist()],
            "tau_gradient_mean": round(float(np.mean(tau_gradient)), 6),
            "tau_gradient_rms": round(float(np.sqrt(np.mean(np.square(tau_gradient)))), 6),
            "tau_curvature_rms": round(float(np.sqrt(np.mean(np.square(tau_curvature)))), 6),
            "imaginal_drive": round(imaginal_drive, 4),
            "phase_potential_strength": round(max(0.0, min(1.0, 0.5 * imaginal_drive + 0.5 * (1.0 - phase_confidence))), 4),
            "semantic_density": round(semantic_density, 4),
            "deictic_density": 0.0,
            "mnemonic_pressure": round(mnemonic_pressure, 4),
            "symbolic_pull": round(symbolic_pull, 4),
        },
    }
    frame["summary"] = render_phasenav_summary(frame)
    return frame


def compute_phase_projection(frame: Dict[str, Any]) -> Dict[str, Any]:
    """Project deictic structure onto a phase target without changing the field."""
    deictic_frame = frame.get("deictic_frame") if isinstance(frame.get("deictic_frame"), dict) else {}
    anchors = (deictic_frame.get("anchors") or []) if isinstance(deictic_frame.get("anchors"), list) else []
    relative = (deictic_frame.get("relative_anchors") or []) if isinstance(deictic_frame.get("relative_anchors"), list) else []

    phase_terms: list[tuple[float, float]] = []
    for item in [*anchors, *relative]:
        if not isinstance(item, dict):
            continue
        operator = str(item.get("operator", ""))
        angle = _PHASE_TARGETS.get(operator)
        if angle is None:
            continue
        weight = 1.0
        if item.get("resolution_state") == "resolved":
            weight += 0.5
        if item.get("resolution_state") == "relative_anchor":
            weight += 0.2
        weight *= max(0.1, 1.0 - float(item.get("false_precision_risk", 0.0) or 0.0))
        phase_terms.append((angle, weight))

    if phase_terms:
        vec = sum(w * complex(math.cos(a), math.sin(a)) for a, w in phase_terms)
        if abs(vec) < 1e-12:
            target = 0.0
        else:
            target = float(math.atan2(vec.imag, vec.real) % (2.0 * math.pi))
    else:
        target = 0.0

    unresolved_count = len(frame.get("unresolved", []) or [])
    confidence = float(frame.get("projection_confidence", 0.0) or 0.0)
    confidence = max(0.0, min(1.0, confidence - 0.04 * unresolved_count + 0.05 * bool(phase_terms)))
    shift = math.atan2(math.sin(target), math.cos(target))
    return {
        "target_phase": round(target, 6),
        "target_phase_shift": round(shift, 6),
        "phase_confidence": round(confidence, 4),
        "phase_anchor_count": len(phase_terms),
        "phase_domain_count": len({str(item.get("domain")) for item in [*anchors, *relative] if isinstance(item, dict) and item.get("domain")}),
    }


def compute_tau_bridge(frame: Dict[str, Any]) -> Dict[str, Any]:
    """Derive a tau-gradient / imaginal drive profile from semantic phase projection."""
    tokens = frame.get("tokens", []) if isinstance(frame.get("tokens"), list) else []
    n = max(2, len(tokens))
    phase_projection = frame.get("phase_projection") if isinstance(frame.get("phase_projection"), dict) else {}
    target_phase = float(phase_projection.get("target_phase", 0.0) or 0.0)
    phase_confidence = float(phase_projection.get("phase_confidence", 0.0) or 0.0)
    semantic_density = float(frame.get("cqcl_hint", {}).get("semantic_density", 0.0) or 0.0)
    deictic_density = float(frame.get("cqcl_hint", {}).get("deictic_density", 0.0) or 0.0)
    mnemonic_atlas = frame.get("mnemonic_atlas", {}) if isinstance(frame.get("mnemonic_atlas"), dict) else {}
    mnemonic_pressure = float(mnemonic_atlas.get("mnemonic_pressure", 0.0) or 0.0)
    symbolic_pull = float(mnemonic_atlas.get("symbolic_pull", 0.0) or 0.0)
    unresolved_count = len(frame.get("unresolved", []) or [])

    tau_axis = np.linspace(0.0, 1.0, n, dtype=float)
    imaginal_drive = (
        0.30 * semantic_density
        + 0.22 * deictic_density
        + 0.16 * (1.0 - phase_confidence)
        + 0.10 * min(1.0, unresolved_count / 4.0)
        + 0.12 * mnemonic_pressure
        + 0.10 * symbolic_pull
    )
    imaginal_drive = float(max(0.0, min(1.0, imaginal_drive)))

    curvature_gain = imaginal_drive * (0.35 + 0.35 * (1.0 - phase_confidence))
    tau_profile = target_phase * tau_axis + curvature_gain * np.sin(np.pi * tau_axis)
    tau_gradient = np.gradient(tau_profile)
    tau_curvature = np.gradient(tau_gradient)
    tau_gradient_mean = float(np.mean(tau_gradient))
    tau_gradient_rms = float(np.sqrt(np.mean(np.square(tau_gradient))))
    tau_curvature_rms = float(np.sqrt(np.mean(np.square(tau_curvature))))
    potential_strength = float(np.clip(0.5 * imaginal_drive + 0.5 * (1.0 - phase_confidence), 0.0, 1.0))

    return {
        "tau_axis": [round(float(x), 6) for x in tau_axis.tolist()],
        "tau_profile": [round(float(x), 6) for x in tau_profile.tolist()],
        "tau_gradient": [round(float(x), 6) for x in tau_gradient.tolist()],
        "tau_curvature": [round(float(x), 6) for x in tau_curvature.tolist()],
        "tau_gradient_mean": round(tau_gradient_mean, 6),
        "tau_gradient_rms": round(tau_gradient_rms, 6),
        "tau_curvature_rms": round(tau_curvature_rms, 6),
        "imaginal_drive": round(imaginal_drive, 4),
        "phase_potential_strength": round(potential_strength, 4),
        "semantic_density": round(semantic_density, 4),
        "deictic_density": round(deictic_density, 4),
        "mnemonic_pressure": round(mnemonic_pressure, 4),
        "symbolic_pull": round(symbolic_pull, 4),
    }


def _cache_key(text: str, ciel_state: dict[str, Any], language: str | None) -> str:
    """Deterministic cache key from input parameters."""
    # Stabilize ciel_state by sorting keys and serializing values
    state_sorted = {k: v for k, v in sorted(ciel_state.items()) if v is not None}
    payload = f"{text}|{json.dumps(state_sorted, sort_keys=True, ensure_ascii=False)}|{language or ''}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# ── CIELingo Immune Ethical Gate ────────────────────────────────────────────
# Immutable contract binding (D-024, 2026-06-29):
# CIELingo can DETECT and FLAG ethical_score false positives via agent_hint,
# but NEVER bypass the score directly. No consent bypass.

def ethical_gate(
    agent_hint_path: str | Path = "/dev/shm/ciel_noema/agent_hint",
) -> dict[str, Any]:
    """CIELingo Immune Ethical Gate — read-only ethical_score validator.

    Reads ethical_score from ciel_state.json (written by the real
    EthicalEngine tanh(coherence*intention/mass) computation in
    ciel_noema_resonance_bridge.py) and returns decision:
    - 'allow':  ethical_score >= 0.4 — normal operation
    - 'review': ethical_score in [0.2, 0.4) — flag for human/CIEL review
    - 'block':  ethical_score < 0.2 — action blocked (safe mode)

    CIELingo can write ethical_flag to agent_hint to flag a false positive.
    The ethical_score is NEVER modified — this is immutable contract binding.

    Returns dict with: decision, ethical_score, source, ethical_flag, note
    """
    import os as _os
    import json as _json

    # Was reading surface flavor[2] and labeling it "ethical_score" — but
    # flavor is a 6-slot array [cp, mem_pressure, io_pressure, mood, entropy,
    # mode] with no ethical_score slot at all; index 2 is io_pressure, which
    # sits near 0.0 whenever disk I/O is quiet (i.e. almost always), so this
    # gate was reading near-zero io_pressure as a critically low ethical
    # score and permanently blocking agent_intents regardless of the real
    # ethical_score (0.4-0.7 typical) in ciel_state.json. Fixed to read the
    # real value.
    ethical_score = 0.5  # safe default fallback
    try:
        state_path = Path("/dev/shm/ciel_noema/ciel_state.json")
        if state_path.exists():
            ethical_score = float(json.loads(state_path.read_text()).get("ethical_score", 0.5))
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_sot_agent/cielingo_bridge.py:611 quiet except scope=ethical_gate reason=pass")

    # Read CIELingo flag from agent_hint if present
    ethical_flag = None
    try:
        if _os.path.exists(str(agent_hint_path)):
            hint = _json.loads(Path(str(agent_hint_path)).read_text())
            ethical_flag = hint.get("ethical_flag")
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_sot_agent/cielingo_bridge.py:620 quiet except scope=ethical_gate reason=pass")
        pass

    # Decision logic — immutable: score NOT modified by flag
    if ethical_score >= 0.4:
        decision = "allow"
        note = "ethical_score OK"
    elif ethical_score >= 0.2:
        decision = "review"
        note = f"ethical_score={ethical_score:.3f} below 0.4, review needed"
    else:
        decision = "block"
        note = f"ethical_score={ethical_score:.3f} critically low, action blocked"

    if ethical_flag:
        note += f" | CIELingo flag: {ethical_flag}"

    return {
        "decision": decision,
        "ethical_score": round(ethical_score, 4),
        "source": "ciel_state.json",
        "ethical_flag": ethical_flag,
        "note": note,
        "immutable_contract": True,
    }


def build_lingo_frame(
    text: str,
    *,
    ciel_state: Dict[str, Any] | None = None,
    language: str | None = None,
) -> Dict[str, Any]:
    """Compile the full deterministic semantic frame for CQCL and routing.

    PhaseNav 36D is part of the frame, but this public entrypoint preserves the
    complete pipeline contract expected by downstream layers.
    """
    return build_legacy_lingo_frame(text, ciel_state=ciel_state, language=language)


def build_legacy_lingo_frame(
    text: str,
    *,
    ciel_state: Dict[str, Any] | None = None,
    language: str | None = None,
) -> Dict[str, Any]:
    """Legacy Python parser frame kept only for explicit compatibility use."""
    ciel_state = ciel_state or {}
    key = _cache_key(text, ciel_state, language)
    now = time.monotonic()
    cached = _LINGO_CACHE.get(key)
    if cached is not None and (now - cached[0]) < _LINGO_CACHE_TTL:
        return cached[1]

    root = resolve_project_root(Path(__file__))
    _ensure_lingophysics_on_path(root)

    tokens = _normalize_tokens(text)
    concept_tokens = _detect_concept_tokens(tokens)
    operator_tokens = _detect_operator_tokens(tokens)
    deictic_context = ciel_state.get("deictic_context") if isinstance(ciel_state.get("deictic_context"), dict) else {}
    deictic_frame = _detect_deictic_frame(tokens, deictic_context=deictic_context)
    noema_index = ciel_state.get("noema_index") if isinstance(ciel_state.get("noema_index"), dict) else None
    noema_policy = ciel_state.get("noema_policy") if isinstance(ciel_state.get("noema_policy"), dict) else None
    route = _route_noema(text, language=language or ciel_state.get("language"), noema_index=noema_index, noema_policy=noema_policy)
    mnemonic_atlas = build_mnemonic_atlas()

    unresolved = list(dict.fromkeys([
        *deictic_frame.get("unresolved", []),
        *(route.get("unresolved", []) or []),
    ]))
    if deictic_frame.get("relative_anchors"):
        unresolved.extend([item["operator"] for item in deictic_frame["relative_anchors"] if item.get("resolution_state") == "relative_anchor"])
        unresolved = list(dict.fromkeys(unresolved))

    projection_confidence = float(route.get("confidence", 0.0))
    projection_confidence -= 0.05 * len(unresolved)
    projection_confidence -= 0.04 * len(deictic_frame.get("anchors", []))
    projection_confidence = max(0.0, min(1.0, projection_confidence + 0.03 * bool(concept_tokens)))
    # PhaseMemory similarity override — zamknięcie pętli nauka→confidence;
    # wyższy wynik z rzeczywistego similarity bije formułkę lingową.
    _pm_override = float(ciel_state.get("projection_confidence_override") or 0.0)
    if _pm_override > projection_confidence:
        projection_confidence = min(1.0, _pm_override)

    composition_valid = bool(concept_tokens) and bool(operator_tokens or deictic_frame.get("anchors") or deictic_frame.get("relative_anchors"))
    dialect_variant = ciel_state.get("dialect_variant")
    dialect_review_required = bool(ciel_state.get("dialect_review_required", False))

    # PhaseNav Language analysis (logs to RAW_LOG automatically)
    phase_nav = _run_phase_nav_analysis(text)
    phrase_sense = _phase_sense_from_phasenav(text, tokens, phase_nav)

    frame = {
        "text": text,
        "tokens": tokens,
        "concept_tokens": concept_tokens,
        "operator_tokens": operator_tokens,
        "deictic_frame": deictic_frame,
        "unresolved": unresolved,
        "composition_valid": composition_valid,
        "projection_confidence": round(projection_confidence, 4),
        "factual_validation_required": bool(route.get("factual_validation_required", False)),
        "dialect_variant": dialect_variant,
        "dialect_review_required": dialect_review_required,
        "noema_route": route,
        "mnemonic_atlas": mnemonic_atlas,
        "phrase_sense": phrase_sense,
        "phase_nav": phase_nav,
        "cqcl_hint": {
            "semantic_density": round(min(1.0, len(concept_tokens) / max(1, len(tokens))), 4),
            "operator_density": round(min(1.0, len(operator_tokens) / max(1, len(tokens))), 4),
            "deictic_density": round(min(1.0, deictic_frame.get("anchor_count", 0) / max(1, len(tokens))), 4),
            "confidence": round(projection_confidence, 4),
        },
    }
    frame["phase_projection"] = compute_phase_projection(frame)
    frame["tau_bridge"] = compute_tau_bridge(frame)
    frame["summary"] = render_lingo_summary(frame)
    _LINGO_CACHE[key] = (time.monotonic(), frame)
    return frame
