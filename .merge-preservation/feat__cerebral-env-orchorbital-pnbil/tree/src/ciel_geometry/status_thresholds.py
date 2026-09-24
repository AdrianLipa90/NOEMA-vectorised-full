"""CIEL Portal — status classification thresholds. Single source of truth.

Every dashboard surface (serve_portal.py's embedded JS, generate_site.py's
Python renderer, gui/routes.py's JSON API) used to define its own copy of
these band edges, and they disagreed with each other for the same physical
quantity — e.g. EBA defect was "ok below 0.07" in one file and "ok below
0.15" in another, health was "reduced below 0.3" in one and "below 0.35" in
another. Same system state, different color depending which file rendered
it. Import from here instead of re-guessing a number.

Provenance:
  - CLOSURE_* thresholds ARE the real EBA consolidation gate values from
    ciel_omega.memory.holonomy (EBA_COHERENT_THRESHOLD / EBA_CONSOLIDATION_
    THRESHOLD) — they aren't just display bands, they're the thresholds
    that actually decide whether a memory loop is allowed to consolidate.
  - ETHICAL_* and HEALTH_* thresholds are NOT derived from any formula or
    statistical model. They are heuristic "traffic light" cutoffs with no
    first-principles justification in the codebase or the Metatime
    monograph. Keep them, but do not present them as more rigorous than
    they are — this module exists to make that fact visible and auditable,
    not to hide it behind duplicated magic numbers.
"""
from __future__ import annotations

import sys
from pathlib import Path

# ciel_omega lives under src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega, one level
# deeper than src/ciel_geometry — not on sys.path by default (same fix as
# scripts/noema_portal_daemon.py).
_CIEL_OMEGA_PARENT = Path(__file__).resolve().parents[1] / "CIEL_OMEGA_COMPLETE_SYSTEM"
if _CIEL_OMEGA_PARENT.is_dir() and str(_CIEL_OMEGA_PARENT) not in sys.path:
    sys.path.insert(0, str(_CIEL_OMEGA_PARENT))

from ciel_omega.memory.holonomy import (
    EBA_COHERENT_THRESHOLD,
    EBA_CONSOLIDATION_THRESHOLD,
)

# ── Ethical score bands (heuristic, undocumented origin) ──────────────────
ETHICAL_OK: float = 0.6
ETHICAL_WARN: float = 0.4

# ── System health bands (heuristic, undocumented origin) ──────────────────
HEALTH_WARM: float = 0.5
HEALTH_REDUCED: float = 0.3

# ── Closure/EBA-defect bands — anchored to the real consolidation gate ────
CLOSURE_COHERENT: float = EBA_COHERENT_THRESHOLD      # 0.1
CLOSURE_CONSOLIDATABLE: float = EBA_CONSOLIDATION_THRESHOLD  # 0.15


def ethical_class(score: float) -> str:
    if score >= ETHICAL_OK:
        return "ok"
    if score >= ETHICAL_WARN:
        return "warn"
    return "crit"


def health_class(score: float) -> str:
    if score >= HEALTH_WARM:
        return "warm"
    if score >= HEALTH_REDUCED:
        return "reduced"
    return "critical"


def closure_class(defect: float) -> str:
    if defect < CLOSURE_COHERENT:
        return "ok"
    if defect < CLOSURE_CONSOLIDATABLE:
        return "warn"
    return "crit"
