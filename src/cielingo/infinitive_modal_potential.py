"""Infinitive -> modality potential layer for CIELingo.

This module models words before full sentence inference:

    infinitive seed -> modality map -> Collatz seed -> HTRI phase bus

The layer is deliberately scalar/diagnostic.  A Polish infinitive and a
modality receive rest semantic mass and an information potential measured in
``kappa_info = ln(2)/(24*pi)`` units.  Their semantic-linguistic potential energy
is then computed as an N-body interaction proxy that can feed later Kepler and
Lagrange modules.

Epistemic boundary: this is a deterministic runtime surface, not a complete
Polish lexicon, not a physical force law, and not a live NOEMA SoT write.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Iterable

from .collatz_semantic_htri_sync import BASE_FREQUENCY_HZ, DEFAULT_OSCILLATORS
from .lns_language_cards import LNSLanguageCard, load_all_language_cards
from .polish.linguistic_database import load_polish_database
from .semantic_collatz import route_summary, semantic_collatz_route, semantic_seed

KAPPA_INFO = math.log(2.0) / (24.0 * math.pi)
EPSILON_R = KAPPA_INFO


@dataclass(frozen=True)
class InfinitiveSeed:
    """Polish infinitive as semantic seed for Collatz/modal dynamics."""

    infinitive: str
    source: str
    source_id: str
    semantic_axes: tuple[str, ...]
    rest_semantic_mass: float
    potential_phi: float
    potential_unit: str
    collatz_seed: int
    collatz_steps: int
    reduce_count: int
    expand_count: int
    phase_rad: float
    htri_oscillator_id: int

    def as_dict(self) -> dict[str, Any]:
        out = asdict(self)
        out["semantic_axes"] = list(self.semantic_axes)
        return out


@dataclass(frozen=True)
class ModalitySeed:
    """Modality operator as semantic-potential body."""

    modality_id: str
    label: str
    family: str
    polish_markers: tuple[str, ...]
    semantic_axes: tuple[str, ...]
    rest_semantic_mass: float
    potential_phi: float
    potential_unit: str
    phase_rad: float
    htri_oscillator_id: int

    def as_dict(self) -> dict[str, Any]:
        out = asdict(self)
        out["polish_markers"] = list(self.polish_markers)
        out["semantic_axes"] = list(self.semantic_axes)
        return out


@dataclass(frozen=True)
class ModalMapping:
    """Infinitive/modal pair with N-body potential-energy proxy."""

    infinitive: str
    modality_id: str
    modality_label: str
    affinity: float
    semantic_distance: float
    phase_distance_rad: float
    nbody_binding_energy: float
    lagrangian_potential_U: float
    lagrangian_kinetic_proxy: float
    lagrangian_L_proxy: float
    kepler_mu_info: float
    kepler_period_proxy: float
    collatz_seed: int
    collatz_mode: str
    htri_phase_lock: float
    recommended_lane: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


DEFAULT_MODALITIES: tuple[dict[str, Any], ...] = (
    {
        "modality_id": "modal:epistemic_possibility",
        "label": "possibility / maybe-can",
        "family": "epistemic",
        "polish_markers": ("może", "chyba", "prawdopodobnie"),
        "semantic_axes": ("uncertainty", "possibility", "knowledge"),
        "rest_semantic_mass": 0.62,
    },
    {
        "modality_id": "modal:dynamic_ability",
        "label": "ability / can",
        "family": "dynamic",
        "polish_markers": ("mogę", "potrafię", "umiem"),
        "semantic_axes": ("capacity", "agency", "action"),
        "rest_semantic_mass": 0.74,
    },
    {
        "modality_id": "modal:deontic_obligation",
        "label": "obligation / must",
        "family": "deontic",
        "polish_markers": ("muszę", "należy", "trzeba"),
        "semantic_axes": ("constraint", "duty", "ethics"),
        "rest_semantic_mass": 0.86,
    },
    {
        "modality_id": "modal:deontic_permission",
        "label": "permission / may",
        "family": "deontic",
        "polish_markers": ("mogę", "wolno", "można"),
        "semantic_axes": ("boundary", "permission", "consent"),
        "rest_semantic_mass": 0.78,
    },
    {
        "modality_id": "modal:volitional_intention",
        "label": "intention / want-to",
        "family": "volitional",
        "polish_markers": ("chcę", "zamierzam", "pragnę"),
        "semantic_axes": ("intention", "will", "attractor"),
        "rest_semantic_mass": 0.82,
    },
    {
        "modality_id": "modal:negation_boundary",
        "label": "negation / not-to",
        "family": "boundary",
        "polish_markers": ("nie", "nigdy", "bez"),
        "semantic_axes": ("boundary", "refusal", "exclusion"),
        "rest_semantic_mass": 0.58,
    },
    {
        "modality_id": "modal:temporal_future",
        "label": "future / will",
        "family": "temporal",
        "polish_markers": ("będę", "będzie", "potem"),
        "semantic_axes": ("time", "future", "trajectory"),
        "rest_semantic_mass": 0.66,
    },
    {
        "modality_id": "modal:aspectual_completion",
        "label": "completion / manage-to",
        "family": "aspectual",
        "polish_markers": ("zdołam", "uda się", "dokonam"),
        "semantic_axes": ("completion", "closure", "act"),
        "rest_semantic_mass": 0.80,
    },
)


def _bounded(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _phase_from_id(value: str) -> float:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return (int(digest[:16], 16) / float(16**16 - 1)) * (2.0 * math.pi)


def _oscillator_id(value: str, n_oscillators: int = DEFAULT_OSCILLATORS) -> int:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return int(digest[:16], 16) % max(1, n_oscillators)


def _angle_delta(a: float, b: float) -> float:
    return abs(math.atan2(math.sin(a - b), math.cos(a - b)))


def _mass_from_axes(semantic_mass_payload: dict[str, Any] | None) -> float:
    if not semantic_mass_payload:
        return 0.5
    vals = [float(v) for v in semantic_mass_payload.values() if isinstance(v, (int, float))]
    return _bounded(sum(vals) / len(vals)) if vals else 0.5


def _collatz_summary(label: str) -> tuple[int, int, int, int]:
    seed = semantic_seed(label)
    route = semantic_collatz_route(seed, max_steps=32)
    summary = route_summary(route)
    return seed, int(summary["steps"]), int(summary["reduce_count"]), int(summary["expand_count"])


def _is_polish_infinitive(surface: str) -> bool:
    word = surface.strip().lower()
    # Polish infinitives generally end in ć/c; keep this strict enough to avoid
    # nominal seeds like "pamięć" by using it only for verb/operator sources.
    return len(word) >= 3 and word.endswith(("ć", "c"))


def _infinitive_from_card(card: LNSLanguageCard) -> str | None:
    if card.card_kind != "operator":
        return None
    for lang, values in card.languages.items():
        if lang.lower() in {"pl", "pol", "polish"}:
            for value in values:
                if _is_polish_infinitive(value):
                    return value.strip().lower()
    return None


def load_infinitive_seeds(repo_root: str | Path = ".") -> list[InfinitiveSeed]:
    """Load infinitive seeds from Polish DB and NOEMA/LNS operator cards."""
    root = Path(repo_root)
    seeds: dict[str, InfinitiveSeed] = {}

    db = load_polish_database(root)
    for lex in db.lexemes:
        if lex.pos != "verb":
            continue
        infinitive = lex.lemma.strip().lower()
        mass = _mass_from_axes(lex.payload.get("semantic_mass"))
        rsm = round(mass, 6)
        seed, steps, reduce_count, expand_count = _collatz_summary(infinitive)
        phase = _phase_from_id(f"infinitive|{infinitive}")
        seeds[infinitive] = InfinitiveSeed(
            infinitive=infinitive,
            source="polish_linguistic_database",
            source_id=lex.payload.get("frame_id", infinitive),
            semantic_axes=tuple(sorted(db.semantic_mass_axes)),
            rest_semantic_mass=rsm,
            potential_phi=round(rsm * KAPPA_INFO, 12),
            potential_unit="kappa_info = ln(2)/(24*pi)",
            collatz_seed=seed,
            collatz_steps=steps,
            reduce_count=reduce_count,
            expand_count=expand_count,
            phase_rad=round(phase, 6),
            htri_oscillator_id=_oscillator_id(f"infinitive|{infinitive}"),
        )

    for card in load_all_language_cards(root):
        infinitive = _infinitive_from_card(card)
        if not infinitive or infinitive in seeds:
            continue
        mass = _bounded(float(card.semantic_mass))
        rsm = round(mass, 6)
        seed, steps, reduce_count, expand_count = _collatz_summary(infinitive)
        phase = float(card.phase_rad) % (2.0 * math.pi)
        seeds[infinitive] = InfinitiveSeed(
            infinitive=infinitive,
            source="noema_lns_operator_card",
            source_id=card.card_id,
            semantic_axes=tuple(card.semantic_axes),
            rest_semantic_mass=rsm,
            potential_phi=round(rsm * KAPPA_INFO, 12),
            potential_unit="kappa_info = ln(2)/(24*pi)",
            collatz_seed=seed,
            collatz_steps=steps,
            reduce_count=reduce_count,
            expand_count=expand_count,
            phase_rad=round(phase, 6),
            htri_oscillator_id=_oscillator_id(f"infinitive|{infinitive}"),
        )

    return [seeds[k] for k in sorted(seeds)]


def load_modality_seeds(n_oscillators: int = DEFAULT_OSCILLATORS) -> list[ModalitySeed]:
    out: list[ModalitySeed] = []
    for item in DEFAULT_MODALITIES:
        mid = str(item["modality_id"])
        mass = _bounded(float(item["rest_semantic_mass"]))
        rsm = round(mass, 6)
        phase = _phase_from_id(mid)
        out.append(
            ModalitySeed(
                modality_id=mid,
                label=str(item["label"]),
                family=str(item["family"]),
                polish_markers=tuple(str(x) for x in item["polish_markers"]),
                semantic_axes=tuple(str(x) for x in item["semantic_axes"]),
                rest_semantic_mass=rsm,
                potential_phi=round(rsm * KAPPA_INFO, 12),
                potential_unit="kappa_info = ln(2)/(24*pi)",
                phase_rad=round(phase, 6),
                htri_oscillator_id=_oscillator_id(mid, n_oscillators=n_oscillators),
            )
        )
    return out


def _axis_affinity(a: Iterable[str], b: Iterable[str]) -> float:
    aa = {x.lower() for x in a}
    bb = {x.lower() for x in b}
    if not aa or not bb:
        return 0.0
    overlap = len(aa & bb) / len(aa | bb)
    return _bounded(overlap)


def _lexical_phase_affinity(inf: InfinitiveSeed, mod: ModalitySeed) -> float:
    axis = _axis_affinity(inf.semantic_axes, mod.semantic_axes)
    phase = 1.0 - (_angle_delta(inf.phase_rad, mod.phase_rad) / math.pi)
    # Axis overlap is the semantic term; phase is the carrier term.  A small
    # floor keeps sparse seed cards measurable without pretending full certainty.
    return round(_bounded(0.15 + 0.45 * axis + 0.40 * phase), 6)


def map_infinitive_to_modalities(
    infinitive: InfinitiveSeed,
    modalities: Iterable[ModalitySeed],
    *,
    base_frequency_hz: float = BASE_FREQUENCY_HZ,
) -> list[ModalMapping]:
    mappings: list[ModalMapping] = []
    omega0 = 2.0 * math.pi * base_frequency_hz
    for modality in modalities:
        affinity = _lexical_phase_affinity(infinitive, modality)
        phase_distance = _angle_delta(infinitive.phase_rad, modality.phase_rad)
        semantic_distance = math.sqrt(
            phase_distance**2
            + (infinitive.rest_semantic_mass - modality.rest_semantic_mass) ** 2
            + (1.0 - affinity) ** 2
        )
        radius = max(EPSILON_R, semantic_distance)
        reduced_mass = (
            infinitive.rest_semantic_mass * modality.rest_semantic_mass
        ) / max(EPSILON_R, infinitive.rest_semantic_mass + modality.rest_semantic_mass)
        kepler_mu = KAPPA_INFO * (infinitive.rest_semantic_mass + modality.rest_semantic_mass)
        binding = KAPPA_INFO * affinity * infinitive.rest_semantic_mass * modality.rest_semantic_mass / (radius + EPSILON_R)
        lagrangian_U = -binding
        # Kinetic proxy uses normalized HTRI angular velocity to keep the report
        # numeric range readable while retaining the phase-bus dependency.
        omega_norm = omega0 / (2.0 * math.pi * base_frequency_hz)
        kinetic = 0.5 * reduced_mass * (omega_norm * radius) ** 2
        lagrangian_L = kinetic - lagrangian_U
        period = 2.0 * math.pi * math.sqrt((radius**3) / max(EPSILON_R, kepler_mu))
        pair_seed = semantic_seed(f"{infinitive.infinitive}|{modality.modality_id}")
        route = route_summary(semantic_collatz_route(pair_seed, max_steps=32))
        reduce_count = int(route["reduce_count"])
        expand_count = int(route["expand_count"])
        mode = "reduce/identity" if reduce_count >= expand_count else "expand/association"
        phase_lock = _bounded(1.0 - phase_distance / math.pi)
        if affinity >= 0.72 and phase_lock >= 0.65:
            lane = "modal_phase_locked"
        elif binding >= KAPPA_INFO * 0.12:
            lane = "modal_bound_orbit"
        elif phase_lock < 0.35:
            lane = "modal_rephase_needed"
        else:
            lane = "modal_observe"
        mappings.append(
            ModalMapping(
                infinitive=infinitive.infinitive,
                modality_id=modality.modality_id,
                modality_label=modality.label,
                affinity=round(affinity, 6),
                semantic_distance=round(semantic_distance, 6),
                phase_distance_rad=round(phase_distance, 6),
                nbody_binding_energy=round(binding, 12),
                lagrangian_potential_U=round(lagrangian_U, 12),
                lagrangian_kinetic_proxy=round(kinetic, 12),
                lagrangian_L_proxy=round(lagrangian_L, 12),
                kepler_mu_info=round(kepler_mu, 12),
                kepler_period_proxy=round(period, 6),
                collatz_seed=pair_seed,
                collatz_mode=mode,
                htri_phase_lock=round(phase_lock, 6),
                recommended_lane=lane,
            )
        )
    return mappings


def infinitive_modal_report(repo_root: str | Path = ".") -> dict[str, Any]:
    infinitives = load_infinitive_seeds(repo_root)
    modalities = load_modality_seeds()
    mappings = [m for inf in infinitives for m in map_infinitive_to_modalities(inf, modalities)]
    lane_counts: dict[str, int] = {}
    for mapping in mappings:
        lane_counts[mapping.recommended_lane] = lane_counts.get(mapping.recommended_lane, 0) + 1
    total_binding = sum(m.nbody_binding_energy for m in mappings)
    total_L = sum(m.lagrangian_L_proxy for m in mappings)
    return {
        "schema": "cielingo/infinitive-modal-potential/v0.1",
        "source_role": "local_noema_lns_polish_word_surface",
        "epistemic_status": (
            "diagnostic scalar word-potential layer; not full Polish morphology, "
            "not physical force law, not external NOEMA SoT execution"
        ),
        "kappa_info": KAPPA_INFO,
        "potential_unit": "kappa_info = ln(2)/(24*pi)",
        "base_frequency_hz": BASE_FREQUENCY_HZ,
        "omega0_rad_s": 2.0 * math.pi * BASE_FREQUENCY_HZ,
        "infinitive_count": len(infinitives),
        "modality_count": len(modalities),
        "mapping_count": len(mappings),
        "total_nbody_binding_energy": round(total_binding, 12),
        "total_lagrangian_L_proxy": round(total_L, 12),
        "lane_counts": dict(sorted(lane_counts.items())),
        "infinitives": [i.as_dict() for i in infinitives],
        "modalities": [m.as_dict() for m in modalities],
        "mappings": [m.as_dict() for m in mappings],
    }


def write_report(path: str | Path, repo_root: str | Path = ".") -> dict[str, Any]:
    report = infinitive_modal_report(repo_root)
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


__all__ = [
    "KAPPA_INFO",
    "EPSILON_R",
    "InfinitiveSeed",
    "ModalitySeed",
    "ModalMapping",
    "load_infinitive_seeds",
    "load_modality_seeds",
    "map_infinitive_to_modalities",
    "infinitive_modal_report",
    "write_report",
]
