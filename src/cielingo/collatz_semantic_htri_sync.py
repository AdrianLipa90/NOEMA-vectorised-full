"""Synchronize CIELingo Collatz routing, semantic cards and HTRI phases.

This is a deterministic planning/diagnostic surface.  It does not run primary
NOEMA inference and it does not claim physical HTRI entrainment.  It maps local
language-card phases/masses onto a 120-oscillator 7.83 Hz reference grid so the
runtime can see where semantic routing is synchronized or congested.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import math
from pathlib import Path
from typing import Any, Iterable

from .lns_language_cards import LNSLanguageCard, load_all_language_cards, search_language_cards
from .semantic_collatz import route_summary, semantic_collatz_route, semantic_seed

BASE_FREQUENCY_HZ = 7.83
DEFAULT_OSCILLATORS = 36


@dataclass(frozen=True)
class CardSyncState:
    card_id: str
    card_kind: str
    canonical_label: str
    oscillator_id: int
    base_frequency_hz: float
    omega0_rad_s: float
    semantic_mass: float
    semantic_phase_rad: float
    oscillator_phase_rad: float
    phase_alignment: float
    collatz_seed: int
    collatz_steps: int
    reduce_count: int
    expand_count: int
    collatz_mode_bias: float
    sync_pressure: float
    recommended_action: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _stable_oscillator(card_id: str, n_oscillators: int) -> int:
    digest = hashlib.sha256(card_id.encode("utf-8")).hexdigest()
    return int(digest[:16], 16) % n_oscillators


def _angle_delta(a: float, b: float) -> float:
    return abs(math.atan2(math.sin(a - b), math.cos(a - b)))


def _card_seed(card: LNSLanguageCard) -> int:
    payload = f"{card.card_id}|{card.canonical_label}|{card.source_path}"
    return semantic_seed(hashlib.sha256(payload.encode("utf-8")).hexdigest())


def synchronize_card(
    card: LNSLanguageCard,
    *,
    n_oscillators: int = DEFAULT_OSCILLATORS,
    base_frequency_hz: float = BASE_FREQUENCY_HZ,
    max_collatz_steps: int = 32,
) -> CardSyncState:
    seed = _card_seed(card)
    route = semantic_collatz_route(seed, max_steps=max_collatz_steps)
    summary = route_summary(route)
    steps = max(1, int(summary["steps"]))
    reduce_count = int(summary["reduce_count"])
    expand_count = int(summary["expand_count"])
    mode_bias = (expand_count - reduce_count) / steps

    osc = _stable_oscillator(card.card_id, n_oscillators)
    osc_phase = 2.0 * math.pi * (osc / max(1, n_oscillators))
    phase = float(card.phase_rad) % (2.0 * math.pi)
    delta = _angle_delta(phase, osc_phase)
    phase_alignment = max(0.0, 1.0 - delta / math.pi)
    mass = max(0.0, float(card.semantic_mass))
    # Pressure rises when semantically heavy cards have low phase alignment or
    # when Collatz expansion dominates.  No arbitrary canon threshold is hidden:
    # the action labels below expose the current heuristic boundary.
    sync_pressure = min(1.0, mass * (1.0 - phase_alignment) + max(0.0, mode_bias))

    if sync_pressure >= 0.66:
        action = "quarantine_for_semantic_htri_resync"
    elif phase_alignment < 0.45 and mode_bias > 0.0:
        action = "expand_then_rephase"
    elif phase_alignment >= 0.70 and reduce_count >= expand_count:
        action = "reduce_to_identity_cluster"
    else:
        action = "observe_reference_surface"

    return CardSyncState(
        card_id=card.card_id,
        card_kind=card.card_kind,
        canonical_label=card.canonical_label,
        oscillator_id=osc,
        base_frequency_hz=base_frequency_hz,
        omega0_rad_s=2.0 * math.pi * base_frequency_hz,
        semantic_mass=round(mass, 6),
        semantic_phase_rad=round(phase, 6),
        oscillator_phase_rad=round(osc_phase, 6),
        phase_alignment=round(phase_alignment, 6),
        collatz_seed=seed,
        collatz_steps=steps,
        reduce_count=reduce_count,
        expand_count=expand_count,
        collatz_mode_bias=round(mode_bias, 6),
        sync_pressure=round(sync_pressure, 6),
        recommended_action=action,
    )


def synchronization_report(
    repo_root: str | Path = ".",
    *,
    query: str = "language semantic collatz htri",
    limit: int = 24,
    n_oscillators: int = DEFAULT_OSCILLATORS,
) -> dict[str, Any]:
    hits = search_language_cards(query, repo_root, limit=limit)
    if hits:
        hit_ids = {(h["card_id"], h["source_path"]) for h in hits}
        cards = [c for c in load_all_language_cards(repo_root) if (c.card_id, c.source_path) in hit_ids]
    else:
        cards = load_all_language_cards(repo_root)[:limit]

    states = [synchronize_card(card, n_oscillators=n_oscillators) for card in cards]
    if states:
        mean_alignment = sum(s.phase_alignment for s in states) / len(states)
        mean_pressure = sum(s.sync_pressure for s in states) / len(states)
    else:
        mean_alignment = 0.0
        mean_pressure = 0.0
    actions: dict[str, int] = {}
    for state in states:
        actions[state.recommended_action] = actions.get(state.recommended_action, 0) + 1

    return {
        "schema": "cielingo/collatz-semantic-htri-sync/v0.1",
        "source_role": "local_noema_lns_surface_reference",
        "epistemic_status": "diagnostic synchronization plan only; no primary NOEMA inference or physical HTRI claim",
        "query": query,
        "base_frequency_hz": BASE_FREQUENCY_HZ,
        "omega0_rad_s": 2.0 * math.pi * BASE_FREQUENCY_HZ,
        "n_oscillators": n_oscillators,
        "card_count": len(states),
        "mean_phase_alignment": round(mean_alignment, 6),
        "mean_sync_pressure": round(mean_pressure, 6),
        "actions": dict(sorted(actions.items())),
        "states": [s.as_dict() for s in states],
    }


__all__ = [
    "BASE_FREQUENCY_HZ",
    "DEFAULT_OSCILLATORS",
    "CardSyncState",
    "synchronize_card",
    "synchronization_report",
]
