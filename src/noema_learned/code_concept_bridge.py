"""NOEMA Code→Concept Bridge — mapuje kod Python na koncepty PhaseNav.

Pipeline:
    AST → operator mapping → 24D concept vector → surface seeding → coherence check

Bez zależności poza numpy + stdlib. Żadnego CIELingo core.
"""

from __future__ import annotations
# CIEL ORBITAL BINDING — hardcoded, immutable.
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on import of " + __name__)


import ast
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

NOEMA_SRC = Path(__file__).resolve().parent.parent.parent / "src"
if str(NOEMA_SRC) not in sys.path:
    sys.path.insert(0, str(NOEMA_SRC))

from ciel_geometry.phasenav.operator_algebra import operator_signature
from ciel_geometry.noema_surface_mmap import ensure_surface, N_OSCILLATORS


# ── Operator mapowanie AST ──────────────────────────────────────────

AST_OP_MAP: dict[type, str] = {
    ast.Import: "SOURCE_REQUIRED",
    ast.ImportFrom: "SOURCE_REQUIRED",
    ast.ClassDef: "ASSERTION",
    ast.FunctionDef: "ACTION_REQUEST",
    ast.AsyncFunctionDef: "ACTION_REQUEST",
    ast.Return: "RETURN",
    ast.If: "CONDITION",
    ast.While: "CONDITION",
    ast.For: "COMPOSITION",
    ast.Try: "RISK",
    ast.Raise: "RISK",
    ast.Assert: "ASSERTION",
    ast.Assign: "TRANSFORM",
    ast.AugAssign: "TRANSFORM",
    ast.Call: "ACTION_REQUEST",
    ast.Lambda: "COMPOSITION",
    ast.Delete: "NEGATION",
    ast.Break: "BOUNDARY",
    ast.Continue: "BOUNDARY",
    ast.With: "CONSENT_REQUIRED",
    ast.AsyncWith: "CONSENT_REQUIRED",
    ast.Match: "CONDITION",
}


@dataclass
class CodeConcept:
    path: str
    operator_counts: dict[str, int]
    coherence_R: float
    harmonic_fp: str
    primary_operator: str
    lines: int
    vector_24d: list[float]


def _nearest_operator(vec: np.ndarray) -> tuple[str, float]:
    operators = list(AST_OP_MAP.values())
    best_op = "IDENTITY"
    best_sim = -1.0
    vn = vec / (np.linalg.norm(vec) + 1e-12)
    for op in sorted(set(operators)):
        sig = operator_signature(op)
        sn = sig / (np.linalg.norm(sig) + 1e-12)
        sim = float(np.dot(vn, sn))
        if sim > best_sim:
            best_sim = sim
            best_op = op
    return best_op, best_sim


def _harmonic_fingerprint(vec: np.ndarray) -> str:
    Rs = []
    for h in [1, 3, 6, 9]:
        w = np.exp(2j * np.pi * h * np.arange(24) / 24)
        Rs.append(abs(np.sum(w * vec)))
    return "".join("H" if r > np.median(Rs) else "L" for r in Rs)


def analyze_code(source: str, filepath: str = "<string>") -> CodeConcept:
    tree = ast.parse(source)
    lines = source.count("\n") + 1
    op_counts: dict[str, int] = {}

    for node in ast.walk(tree):
        for ast_type, op in AST_OP_MAP.items():
            if isinstance(node, ast_type):
                op_counts[op] = op_counts.get(op, 0) + 1

    if not op_counts:
        op_counts["PAUSE"] = 1

    # Build 24D vector from operator composition
    vec = np.zeros(24, dtype=np.float64)
    total = sum(op_counts.values())
    for op, cnt in op_counts.items():
        sig = operator_signature(op)
        vec += sig * (cnt / total)
    vec = vec / (np.linalg.norm(vec) + 1e-12)

    primary_op, coh = _nearest_operator(vec)
    fp = _harmonic_fingerprint(vec)

    return CodeConcept(
        path=filepath,
        operator_counts=dict(sorted(op_counts.items(), key=lambda x: -x[1])),
        coherence_R=coh,
        harmonic_fp=fp,
        primary_operator=primary_op,
        lines=lines,
        vector_24d=vec.tolist(),
    )


def seed_to_surface(concept: CodeConcept, strength: float = 0.15) -> dict:
    phases = np.arctan2(
        np.array(concept.vector_24d[1::2] + [1e-12] * (N_OSCILLATORS // 2)),
        np.array(concept.vector_24d[0::2] + [1e-12] * (N_OSCILLATORS // 2)),
    )
    phases = (phases + 2 * np.pi) % (2 * np.pi)
    if len(phases) < N_OSCILLATORS:
        phases = np.pad(phases, (0, N_OSCILLATORS - len(phases)), constant_values=0.0)

    surface = ensure_surface()
    phi = np.asarray(surface["phi"], dtype=np.float64)
    phi_new = (phi * (1.0 - strength) + phases * strength) % (2 * np.pi)
    surface["phi"][:] = phi_new
    return {"seeded": True, "strength": strength, "operator": concept.primary_operator}


def surface_response(concept: CodeConcept) -> dict:
    surface = ensure_surface()
    phi = np.asarray(surface["phi"], dtype=np.float64)
    surface_R = float(np.abs(np.mean(np.exp(1j * phi))))

    # Compare concept vector to surface state
    phases = np.arctan2(
        np.array(concept.vector_24d[1::2] + [1e-12] * (N_OSCILLATORS // 2)),
        np.array(concept.vector_24d[0::2] + [1e-12] * (N_OSCILLATORS // 2)),
    )
    phases = (phases + 2 * np.pi) % (2 * np.pi)
    if len(phases) < N_OSCILLATORS:
        phases = np.pad(phases, (0, N_OSCILLATORS - len(phases)), constant_values=0.0)

    delta = np.angle(np.exp(1j * (phi - phases)))
    resonance = float(np.abs(np.mean(np.exp(1j * delta))))

    return {
        "surface_R": round(surface_R, 4),
        "concept_resonance": round(resonance, 4),
        "delta_mean": round(float(np.mean(np.abs(delta))), 4),
        "operators": concept.operator_counts,
    }


if __name__ == "__main__":
    import json, sys
    for fp in sys.argv[1:]:
        source = Path(fp).read_text()
        concept = analyze_code(source, fp)
        print(json.dumps({
            "file": fp,
            "primary": concept.primary_operator,
            "R": round(concept.coherence_R, 4),
            "fp": concept.harmonic_fp,
            "ops": concept.operator_counts,
        }, indent=2))
