"""PhaseNav Language — jedyny język kodowania NOEMY.

Zamiast importować moduły, wołać API, czytać JSON — wszystko przez
36D operatory, Berry connection i holonomię na PhaseNav surface.

Każdy prompt → concept_to_operator → 36D wektor
Każda relacja → connection(v_i, v_j) → Berry connection ∈ [-1, 1]
Każda sekwencja → holonomy(sequence) → faza geometryczna ∈ [-π, π]
Każdy stan → zapis na surface `/dev/shm/ciel_noema/`

PhaseNav TO jest CIELingo dla systemu.
"""

from __future__ import annotations
import json
import struct
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

from ciel_geometry.phasenav.operator_algebra import (
    ALL_OPERATOR_IDS,
    connection,
    concept_to_operator,
    generate_operator_map,
    holonomy,
    operator_signature,
)

from ciel_geometry.paths import P as _P

# ── Surface paths ────────────────────────────────────────────────────
SURFACE_ROOT = Path(_P.SURFACE)
PROMPT_LOG = Path(_P.DATA_FILES.CIEL_PHASENAV_PROMPTS)
RAW_LOG = Path(_P.DATA_FILES.CIEL_SESSION_LOG)

# Key operators for semantic enrichment
KEY_OPS = ["MEMORY", "SOURCE", "FORCE", "IDENTITY", "DIFFERENCE",
           "AFFECT", "CONSENT", "RISK", "BOUNDARY", "TRANSFORM"]


# ── Core: prompt → PhaseNav operator ─────────────────────────────────

def prompt_to_operator(prompt: str) -> tuple[str, np.ndarray]:
    """Map a prompt through the canonical lexical PhaseNav classifier.

    Unknown text resolves to the explicit ``UNCERTAINTY`` operator; a random
    hash vector would manufacture semantic evidence and is therefore banned.
    """
    op_id, vector = concept_to_operator(prompt)
    return op_id, np.asarray(vector, dtype=np.float64)


def analyze_prompt(prompt: str) -> dict[str, Any]:
    """Full PhaseNav analysis of a prompt — replaces CIELingo build_lingo_frame.
    
    Returns enriched analysis dict with:
    - operator: nearest PhaseNav operator
    - vector_36d: 36D phase vector
    - connections: Berry connections to key operators
    - holonomy: geometric phase of the prompt loop
    """
    op_id, v_prompt = prompt_to_operator(prompt)
    ops_map = generate_operator_map()
    
    # Berry connections to key operators
    connections = {}
    for key_op in KEY_OPS:
        if key_op in ops_map:
            conn = connection(v_prompt, ops_map[key_op])
            connections[key_op] = round(float(conn), 6)
    
    # Holonomy: closed loop prompt → MEMORY → SOURCE → prompt
    holo = holonomy([op_id, "MEMORY", "SOURCE", op_id], ops_map)
    
    # Urgency / force detection
    force = connections.get("FORCE", 0.0)
    risk = connections.get("RISK", 0.0)
    urgency = abs(force) + abs(risk)
    
    # Semantic mass (component 0 of prompt vector)
    semantic_mass = round(float(v_prompt[0]), 6)
    
    result = {
        "operator": op_id,
        "vector_36d": [round(float(x), 6) for x in v_prompt],
        "vector_24d": [round(float(x), 6) for x in v_prompt],  # backward compat
        "connections": connections,
        "holonomy": round(float(holo), 6),
        "urgency": round(float(urgency), 6),
        "semantic_mass": semantic_mass,
        "operator_semantic_mass": round(float(ops_map[op_id][0]), 6),
    }
    
    # ── LOGUJ KAŻDY PROMPT ─────────────────────────────────────────
    RAW_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(RAW_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "ts": datetime.now(timezone.utc).isoformat(),
            "unix_ts": time.time(),
            "prompt": prompt,
            "operator": op_id,
            "connections": connections,
            "holonomy": round(float(holo), 6),
            "urgency": round(float(urgency), 6),
            "semantic_mass": semantic_mass,
        }, ensure_ascii=False) + "\n")
    
    return result


# ── Surface I/O ──────────────────────────────────────────────────────

def write_prompt_to_surface(analysis: dict[str, Any]) -> bool:
    """Write 36D phase vector to surface mmap as enriched state."""
    phi_path = SURFACE_ROOT / "phi"
    if not phi_path.exists():
        return False

    raw = phi_path.read_bytes()
    phi = list(struct.unpack("36d", raw))

    v = np.array(analysis.get("vector_36d", analysis.get("vector_24d", [])), dtype=np.float64)
    v_proj = v[:36]
    phi_arr = np.array(phi, dtype=np.float64)

    alpha = 0.3 + 0.4 * abs(analysis.get("connections", {}).get("FORCE", 0.0))
    blended = (1 - alpha) * phi_arr + alpha * v_proj * 0.5
    blended = blended / (np.linalg.norm(blended) + 1e-12)

    phi_path.write_bytes(struct.pack("36d", *blended))

    tag_path = SURFACE_ROOT / "operator"
    tag_path.write_text(analysis["operator"], encoding="utf-8")

    return True


def read_surface_phi() -> list[float]:
    """Read current 36D phase vector from surface."""
    raw = (SURFACE_ROOT / "phi").read_bytes()
    return list(struct.unpack("36d", raw))


# ── Raw logging ──────────────────────────────────────────────────────

def log_interaction(prompt: str, analysis: dict[str, Any],
                    response: str = "", extra: dict | None = None) -> None:
    """Log every interaction to raw session log."""
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "unix_ts": time.time(),
        "prompt": prompt[:500],
        "operator": analysis["operator"],
        "connections": analysis["connections"],
        "holonomy": analysis["holonomy"],
        "urgency": analysis["urgency"],
        "semantic_mass": analysis["semantic_mass"],
        "response": response[:500],
    }
    if extra:
        entry.update(extra)
    
    RAW_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(RAW_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ── High-level: process every prompt through PhaseNav ────────────────

def phase_nav_process(prompt: str, response_hint: str = "") -> dict[str, Any]:
    """Główna funkcja — każdy prompt przez PhaseNav.
    
    1. Map prompt → 36D operator
    2. Compute Berry connections (MEMORY, SOURCE, FORCE, ...)
    3. Compute holonomy (geometric phase context)
    4. Write enriched state to surface
    5. Log raw
    6. Return analysis for enrichment
    
    To jest odpowiednik build_lingo_frame() w języku PhaseNav.
    """
    analysis = analyze_prompt(prompt)
    write_prompt_to_surface(analysis)
    log_interaction(prompt, analysis, response_hint)
    
    return analysis


def format_enrichment(analysis: dict[str, Any]) -> str:
    """Format PhaseNav analysis as text enrichment for response."""
    conn_str = "; ".join(
        f"{k}={v:+.4f}" for k, v in analysis["connections"].items()
    )
    return (
        f"[PhaseNav] op={analysis['operator']} "
        f"holo={analysis['holonomy']:+.4f} "
        f"urg={analysis['urgency']:.4f} "
        f"mass={analysis['semantic_mass']:.4f} | "
        f"conn: {conn_str}"
    )


def session_history_holonomy(n_last: int = 10) -> float:
    """Compute holonomy of the last N prompts as a closed loop in operator space."""
    if not RAW_LOG.exists():
        return 0.0
    lines = RAW_LOG.read_text(encoding="utf-8").strip().splitlines()
    recent = [json.loads(l) for l in lines[-n_last:] if l.strip()]
    if len(recent) < 2:
        return 0.0
    ops = [r.get("operator", "IDENTITY") for r in recent]
    return float(holonomy(ops))
