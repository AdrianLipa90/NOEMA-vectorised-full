"""HTRI brain phase map — 24 oscillatory regions = 24 cognitive domains.

Każdy oscylator HTRI to region mózgu z własną funkcją kognitywną,
częstotliwością bazową i domyślnymi sprzężeniami holonomicznymi.
CQCL / OrchORbital / NOEMA / SoT / CIELingo — wszystkie jadą na tej
samej magistrali fazowej.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class BrainOscillator:
    id: int
    brain_region: str
    label_pl: str
    domain: str
    base_freq_hz: float
    cognitive_function: str
    default_couplings: tuple[tuple[int, float], ...]
    affect_sensitivity: str
    logic_role: str


# 24 oscylatory HTRI jako regiony mózgu
BRAIN_MAP: tuple[BrainOscillator, ...] = (
    # ── Cortex: executive, logic, language ──
    BrainOscillator(0, "dlPFC", "kora przedczołowa grzbietowo-boczna", "executive", 7.83,
        "Executive control, planning, working memory",
        ((1, 0.7), (2, 0.5), (4, 0.6), (8, 0.4), (20, 0.5)),
        "low", "operator_composition"),
    BrainOscillator(1, "vmPFC", "kora przedczołowa brzuszno-przyśrodkowa", "ethics", 7.73,
        "Value judgment, emotion-regulation, ethical weighting",
        ((0, 0.7), (2, 0.6), (3, 0.5), (12, 0.7), (18, 0.6)),
        "high", "ethical_valuation"),
    BrainOscillator(2, "OFC", "kora oczodołowo-czołowa", "affect", 7.88,
        "Reward, punishment, social affect grounding",
        ((0, 0.5), (1, 0.6), (11, 0.8), (12, 0.7), (19, 0.8)),
        "high", "affect_grounding"),
    BrainOscillator(3, "SMA", "pole ruchowe dodatkowe", "procedural", 7.68,
        "Action sequencing, intention, motor planning",
        ((4, 0.8), (5, 0.7), (14, 0.6), (15, 0.7)),
        "low", "procedural_chaining"),
    BrainOscillator(4, "M1", "kora ruchowa pierwotna", "motor", 7.58,
        "Motor execution, output interface",
        ((3, 0.8), (5, 0.5), (14, 0.4)),
        "none", "action_output"),
    BrainOscillator(5, "S1", "kora somatosensoryczna pierwotna", "sensory", 7.93,
        "Somatic sensation, body awareness, sensory grounding",
        ((3, 0.5), (4, 0.5), (6, 0.6), (13, 0.7)),
        "medium", "sensory_grounding"),
    BrainOscillator(6, "IPL", "płat ciemieniowy dolny", "spatial", 7.63,
        "Spatial reasoning, mathematics, attention",
        ((7, 0.6), (8, 0.5), (9, 0.4), (21, 0.6)),
        "low", "spatial_algebra"),
    BrainOscillator(7, "STG", "zakręt skroniowy górny", "phonological", 7.78,
        "Auditory, speech perception, phonology",
        ((8, 0.7), (6, 0.6), (11, 0.5)),
        "medium", "phonological_loop"),
    BrainOscillator(8, "MTG", "zakręt skroniowy środkowy", "lexical", 7.53,
        "Lexical access, semantic retrieval, word meaning",
        ((0, 0.4), (7, 0.7), (9, 0.5), (11, 0.5), (21, 0.6)),
        "medium", "lexical_semantics"),
    BrainOscillator(9, "V1", "kora wzrokowa pierwotna", "visual", 7.98,
        "Vision, visual imagery, mental simulation",
        ((6, 0.4), (8, 0.5), (13, 0.5)),
        "medium", "visual_imagery"),
    # ── Limbic / Memory ──
    BrainOscillator(10, "Hippocampus", "hipokamp", "episodic", 7.71,
        "Episodic memory formation, spatial navigation, binding",
        ((11, 0.7), (12, 0.5), (17, 0.5), (21, 0.7), (22, 0.6)),
        "medium", "episodic_binding"),
    BrainOscillator(11, "Amygdala", "ciało migdałowate", "affect", 7.85,
        "Fear, salience detection, affective tagging, threat assessment",
        ((2, 0.8), (10, 0.7), (12, 0.7), (19, 0.7), (23, 0.6)),
        "high", "affect_salience"),
    BrainOscillator(12, "ACC", "kora zakrętu obręczy przednia", "conflict", 7.67,
        "Conflict monitoring, error detection, performance adjustment",
        ((1, 0.7), (11, 0.7), (13, 0.6), (23, 0.7)),
        "high", "conflict_resolution"),
    BrainOscillator(13, "Insula", "wyspa", "self", 7.75,
        "Interoception, self-awareness, emotional awareness",
        ((5, 0.7), (9, 0.5), (12, 0.6), (21, 0.5)),
        "high", "self_awareness"),
    BrainOscillator(14, "BG", "jądra podstawy", "habit", 7.47,
        "Action selection, habits, procedural learning, gating",
        ((3, 0.6), (4, 0.4), (15, 0.7), (17, 0.6)),
        "low", "habit_selection"),
    BrainOscillator(15, "Cerebellum", "móżdżek", "timing", 7.89,
        "Timing, coordination, prediction, error correction",
        ((3, 0.7), (4, 0.6), (14, 0.7), (17, 0.5)),
        "none", "timing_prediction"),
    # ── Deep brain / Neuromodulation ──
    BrainOscillator(16, "Thalamus", "wzgórze", "gate", 7.60,
        "Sensory relay, attention gating, cortical synchronization",
        ((0, 0.6), (5, 0.8), (9, 0.7), (14, 0.6), (17, 0.7)),
        "low", "sensory_gate"),
    BrainOscillator(17, "Hypothalamus", "podwzgórze", "drive", 7.55,
        "Homeostasis, drives, autonomic regulation, hormonal control",
        ((16, 0.7), (18, 0.6), (19, 0.5)),
        "medium", "homeostatic_drive"),
    BrainOscillator(18, "VTA", "pole brzuszne nakrywki", "reward", 7.82,
        "Dopamine, reward prediction error, motivation",
        ((1, 0.6), (2, 0.8), (11, 0.7), (22, 0.5)),
        "high", "reward_learning"),
    BrainOscillator(19, "LC", "miejsce sinawe", "arousal", 7.95,
        "Norepinephrine, arousal, alertness, stress response",
        ((2, 0.8), (11, 0.7), (12, 0.6), (23, 0.7)),
        "high", "arousal_modulation"),
    # ── Large-scale networks ──
    BrainOscillator(20, "PCC", "zakręt obręczy tylny", "dmn", 7.65,
        "DMN hub, self-reflection, autobiographical memory",
        ((10, 0.6), (21, 0.7), (22, 0.6), (23, 0.4)),
        "medium", "self_reflection"),
    BrainOscillator(21, "AG", "zakręt kątowy", "semantic", 7.50,
        "DMN, semantic integration, cross-modal binding, comprehension",
        ((6, 0.6), (8, 0.6), (10, 0.7), (20, 0.7), (22, 0.6)),
        "medium", "semantic_integration"),
    BrainOscillator(22, "TPJ", "połączenie skroniowo-ciemieniowe", "social", 7.80,
        "Theory of mind, social cognition, perspective-taking, empathy",
        ((10, 0.6), (21, 0.6), (23, 0.7), (20, 0.6)),
        "high", "social_cognition"),
    BrainOscillator(23, "dACC", "kora zakrętu obręczy grzbietowa", "salience", 7.70,
        "Salience network, attention switching, pain, error salience",
        ((11, 0.6), (12, 0.7), (19, 0.7), (22, 0.7)),
        "high", "salience_switching"),
)

# Indeks szybkiego dostępu
BRAIN_BY_ID: dict[int, BrainOscillator] = {o.id: o for o in BRAIN_MAP}
DOMAINS: tuple[str, ...] = tuple(sorted({o.domain for o in BRAIN_MAP}))


def oscillator_for_card(card_id: str, *, semantic_phase_rad: float, oscillator_base: int = 0) -> int:
    """Assign a card to the best-matching oscillator by phase proximity + domain affinity."""
    domain_affinity: dict[str, int] = {
        "executive": 0, "ethics": 1, "affect": 2, "procedural": 3,
        "motor": 4, "sensory": 5, "spatial": 6, "phonological": 7,
        "lexical": 8, "visual": 9, "episodic": 10, "conflict": 12,
        "habit": 14, "timing": 15, "gate": 16, "drive": 17,
        "reward": 18, "arousal": 19, "dmn": 20, "semantic": 21,
        "social": 22, "salience": 23,
    }
    card_id_lower = card_id.lower()

    # Dedicated oscillator for known card kinds
    for keyword, osc_id in (
        ("operator", 0), ("ethical", 1), ("affect", 2), ("procedur", 3),
        ("speech", 7), ("lexical", 8), ("visual", 9), ("memory", 10),
        ("conflict", 12), ("spatial", 6), ("social", 22), ("timing", 15),
        ("self", 13), ("habit", 14), ("sensory", 5), ("motor", 4),
    ):
        if keyword in card_id_lower:
            return (osc_id + oscillator_base) % 24

    # Fallback: phase-based
    phase_norm = (semantic_phase_rad % (2.0 * math.pi)) / (2.0 * math.pi)
    return (int(phase_norm * 24) + oscillator_base) % 24


def brain_phase_topology(*, oscillator_focus: int | None = None) -> dict[str, Any]:
    """Return full brain phase topology: each oscillator, its couplings, domain."""
    oscs = [BRAIN_MAP[oscillator_focus]] if oscillator_focus is not None else BRAIN_MAP
    nodes = []
    for o in oscs:
        node = {
            "oscillator_id": o.id,
            "brain_region": o.brain_region,
            "label_pl": o.label_pl,
            "domain": o.domain,
            "cognitive_function": o.cognitive_function,
            "base_freq_hz": o.base_freq_hz,
            "affect_sensitivity": o.affect_sensitivity,
            "logic_role": o.logic_role,
            "couplings": [{"target": t, "weight": w} for t, w in o.default_couplings],
        }
        nodes.append(node)
    return {
        "schema": "htri/brain-phase-topology/v0.1",
        "oscillator_count": len(BRAIN_MAP),
        "domains": list(DOMAINS),
        "dominant_freq_hz": 7.83,
        "nodes": nodes,
        "edge_count": sum(len(o.default_couplings) for o in oscs),
    }
