"""CIELingo HTRI phase bus.

This module binds CIELingo language cards to the shared HTRI phase carrier used
by J-functionals, CQCL-shaped intention variables, NOEMA provenance and
OrchORbital card traces.

It is deliberately a *bus* layer, not a rejection/quarantine layer: cards remain
on the semantic surface and receive a lane/action describing how much phase
assistance they need before heavier inference consumes them.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Iterable

from .card_trace_eeg import create_card_trace_snap
from .collatz_semantic_htri_sync import (
    BASE_FREQUENCY_HZ,
    DEFAULT_OSCILLATORS,
    CardSyncState,
    synchronize_card,
)
from .lns_language_cards import LNSLanguageCard, load_all_language_cards, search_language_cards
from .semantic_collatz import route_summary, semantic_collatz_route, semantic_seed

from ciel_geometry.phasenav.metatime_contract import INFORMATION_KAPPA
KAPPA_INFO = INFORMATION_KAPPA


@dataclass(frozen=True)
class PhaseBusNode:
    """Single CIELingo card bound to the HTRI phase bus."""

    card_id: str
    card_kind: str
    canonical_label: str
    oscillator_id: int
    base_frequency_hz: float
    omega0_rad_s: float
    semantic_mass: float
    semantic_phase_rad: float
    htri_phase_rad: float
    phase_alignment: float
    phase_tension: float
    collatz_seed: int
    collatz_steps: int
    collatz_reduce_count: int
    collatz_expand_count: int
    j_phase_cost: float
    j_semantic_cost: float
    j_collatz_cost: float
    j_bus_total: float
    cqcl_quantum_variables: dict[str, float]
    noema_tags: list[str]
    noema_source_path: str
    orchorbital_channel: str
    phase_lane: str
    bus_action: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PhaseBusReport:
    """Aggregate phase-bus state for CIELingo."""

    schema: str
    source_role: str
    epistemic_status: str
    card_count: int
    htri_oscillators: int
    spare_oscillators: int
    base_frequency_hz: float
    omega0_rad_s: float
    registry_digest: str
    mean_phase_alignment: float
    mean_phase_tension: float
    mean_j_bus_total: float
    lane_counts: dict[str, int]
    bus_actions: dict[str, int]
    orchorbital_snap: dict[str, Any]
    nodes: list[dict[str, Any]]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _bounded(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _stable_float(seed: str) -> float:
    digest = hashlib.sha256(seed.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") / float(2**64 - 1)


def _registry_digest(cards: Iterable[LNSLanguageCard]) -> str:
    payload = [
        {
            "card_id": c.card_id,
            "kind": c.card_kind,
            "label": c.canonical_label,
            "source": c.source_path,
            "mass": round(float(c.semantic_mass), 8),
            "phase": round(float(c.phase_rad), 8),
        }
        for c in sorted(cards, key=lambda x: (x.card_kind, x.card_id, x.source_path))
    ]
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def _phase_lane(alignment: float, tension: float, j_total: float) -> tuple[str, str]:
    """Return non-excluding lane/action for a phase-bus node."""
    if alignment >= 0.72 and j_total <= 0.36:
        return "phase_locked", "run_on_shared_phase"
    if alignment >= 0.50 and tension <= 0.55:
        return "phase_coupled", "run_with_j_cqcl_weighting"
    if tension <= 0.72:
        return "phase_tension", "rephase_before_heavy_inference"
    return "phase_saturated", "throttle_and_rephase_on_htri_bus"


def _cqcl_variables(card: LNSLanguageCard, sync: CardSyncState, j_total: float) -> dict[str, float]:
    """Build CQCL-shaped normalized variables without importing legacy CQCL."""
    lexical_span = sum(len(v) for v in card.languages.values())
    axes_count = len(card.semantic_axes)
    label_entropy_proxy = _stable_float(f"cqcl|{card.card_id}|{card.canonical_label}")
    return {
        "semantic_mass": _bounded(sync.semantic_mass),
        "phase_alignment": _bounded(sync.phase_alignment),
        "phase_tension": _bounded(1.0 - sync.phase_alignment),
        "collatz_reduce_ratio": _bounded(sync.reduce_count / max(1, sync.collatz_steps)),
        "collatz_expand_ratio": _bounded(sync.expand_count / max(1, sync.collatz_steps)),
        "j_bus_total": _bounded(j_total),
        "lexical_span_norm": _bounded(lexical_span / 48.0),
        "semantic_axes_norm": _bounded(axes_count / 8.0),
        "label_entropy_proxy": _bounded(label_entropy_proxy),
    }


def bind_card_to_phase_bus(
    card: LNSLanguageCard,
    *,
    n_oscillators: int = DEFAULT_OSCILLATORS,
    base_frequency_hz: float = BASE_FREQUENCY_HZ,
) -> PhaseBusNode:
    """Bind one language card to HTRI/J/CQCL/NOEMA/OrchORbital phase bus."""
    sync = synchronize_card(
        card,
        n_oscillators=n_oscillators,
        base_frequency_hz=base_frequency_hz,
    )
    phase_tension = _bounded(1.0 - sync.phase_alignment)
    route = semantic_collatz_route(sync.collatz_seed, max_steps=max(4, sync.collatz_steps))
    collatz = route_summary(route)
    steps = max(1, int(collatz["steps"]))

    j_phase_cost = phase_tension
    j_semantic_cost = _bounded(1.0 - sync.semantic_mass)
    j_collatz_cost = _bounded(max(0.0, sync.expand_count - sync.reduce_count) / steps)
    j_total = _bounded((j_phase_cost + j_semantic_cost + j_collatz_cost) / 3.0 * (1.0 + KAPPA_INFO))
    lane, action = _phase_lane(sync.phase_alignment, phase_tension, j_total)

    return PhaseBusNode(
        card_id=card.card_id,
        card_kind=card.card_kind,
        canonical_label=card.canonical_label,
        oscillator_id=sync.oscillator_id,
        base_frequency_hz=base_frequency_hz,
        omega0_rad_s=2.0 * math.pi * base_frequency_hz,
        semantic_mass=sync.semantic_mass,
        semantic_phase_rad=sync.semantic_phase_rad,
        htri_phase_rad=sync.oscillator_phase_rad,
        phase_alignment=sync.phase_alignment,
        phase_tension=round(phase_tension, 6),
        collatz_seed=sync.collatz_seed,
        collatz_steps=sync.collatz_steps,
        collatz_reduce_count=sync.reduce_count,
        collatz_expand_count=sync.expand_count,
        j_phase_cost=round(j_phase_cost, 6),
        j_semantic_cost=round(j_semantic_cost, 6),
        j_collatz_cost=round(j_collatz_cost, 6),
        j_bus_total=round(j_total, 6),
        cqcl_quantum_variables=_cqcl_variables(card, sync, j_total),
        noema_tags=list(card.noema_tags),
        noema_source_path=card.source_path,
        orchorbital_channel="operator" if card.card_kind == "operator" else "semantic",
        phase_lane=lane,
        bus_action=action,
    )


def select_phase_bus_cards(repo_root: str | Path = ".", *, query: str = "", limit: int | None = None) -> list[LNSLanguageCard]:
    """Select language cards through the local NOEMA/LNS surface."""
    if query:
        hits = search_language_cards(query, repo_root, limit=limit or 64)
        hit_keys = {(h["card_id"], h["source_path"]) for h in hits}
        cards = [c for c in load_all_language_cards(repo_root) if (c.card_id, c.source_path) in hit_keys]
    else:
        cards = load_all_language_cards(repo_root)
    return cards[:limit] if limit else cards


def phase_bus_report(
    repo_root: str | Path = ".",
    *,
    query: str = "",
    limit: int | None = None,
    n_oscillators: int = DEFAULT_OSCILLATORS,
    context_key: str = "cielingo:htri_phase_bus",
    identity_anchor: str = "CIELINGO_HTRI_PHASE_BUS",
) -> dict[str, Any]:
    """Return a CIELingo phase-bus report.

    The report is local/diagnostic. It does not claim direct physical HTRI or
    external NOEMA execution.
    """
    cards = select_phase_bus_cards(repo_root, query=query, limit=limit)
    nodes = [bind_card_to_phase_bus(card, n_oscillators=n_oscillators) for card in cards]

    if nodes:
        mean_alignment = sum(n.phase_alignment for n in nodes) / len(nodes)
        mean_tension = sum(n.phase_tension for n in nodes) / len(nodes)
        mean_j = sum(n.j_bus_total for n in nodes) / len(nodes)
    else:
        mean_alignment = mean_tension = mean_j = 0.0

    lane_counts: dict[str, int] = {}
    action_counts: dict[str, int] = {}
    for n in nodes:
        lane_counts[n.phase_lane] = lane_counts.get(n.phase_lane, 0) + 1
        action_counts[n.bus_action] = action_counts.get(n.bus_action, 0) + 1

    snap = create_card_trace_snap(
        [n.card_id for n in nodes[: min(32, len(nodes))]],
        context_key=context_key,
        identity_anchor=identity_anchor,
    )

    report = PhaseBusReport(
        schema="cielingo/htri-phase-bus/v0.1",
        source_role="local_noema_lns_phase_bus_reference",
        epistemic_status=(
            "diagnostic phase bus: HTRI carrier coordinates CIELingo/J/CQCL/NOEMA/OrchORbital; "
            "not physical HTRI proof and not external NOEMA SoT execution"
        ),
        card_count=len(nodes),
        htri_oscillators=n_oscillators,
        spare_oscillators=max(0, n_oscillators - len(nodes)),
        base_frequency_hz=BASE_FREQUENCY_HZ,
        omega0_rad_s=2.0 * math.pi * BASE_FREQUENCY_HZ,
        registry_digest=_registry_digest(cards),
        mean_phase_alignment=round(mean_alignment, 6),
        mean_phase_tension=round(mean_tension, 6),
        mean_j_bus_total=round(mean_j, 6),
        lane_counts=dict(sorted(lane_counts.items())),
        bus_actions=dict(sorted(action_counts.items())),
        orchorbital_snap=snap.__dict__,
        nodes=[n.as_dict() for n in nodes],
    )
    return report.as_dict()


__all__ = [
    "KAPPA_INFO",
    "PhaseBusNode",
    "PhaseBusReport",
    "bind_card_to_phase_bus",
    "select_phase_bus_cards",
    "phase_bus_report",
]
