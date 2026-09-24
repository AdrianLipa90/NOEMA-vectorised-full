"""CIELingo Card Trace EEG.

A CIELingo card is treated as a line in an inference-EEG surface. A memory snap
stores a multi-line trace pattern: amplitude, phase, semantic mass, affective
weight, couplings and clusters.

This is a CPU/RAM reference surface. It is not biological EEG and does not claim
primary NOEMA/nonlocal execution.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
from typing import Any, Iterable

import numpy as np


DEFAULT_TRACE_CHANNELS = (
    "semantic",
    "memory",
    "affective",
    "procedural",
    "ethical",
    "orbital",
    "pipeline",
)


@dataclass(frozen=True)
class CardTrace:
    card_id: str
    amplitude: float
    phase: float
    semantic_mass: float
    affective_weight: float
    orbital_position: float
    channel: str = "semantic"

    def complex_trace(self) -> complex:
        return complex(self.amplitude * math.cos(self.phase), self.amplitude * math.sin(self.phase))


@dataclass(frozen=True)
class CardTraceSnap:
    snap_id: str
    schema: str
    window: dict[str, int]
    active_traces: list[dict[str, Any]]
    clusters: list[str]
    layout_hash: str
    identity_anchor: str
    execution_layer: str = "fallback_cpu_ram"
    source_role: str = "card_trace_eeg_reference_surface"
    nonlocal_claim_allowed: bool = False
    primary_noema_runtime_available: bool = False
    not_primary_inference: bool = True


def _stable_float(seed: str, scale: float = 1.0) -> float:
    digest = hashlib.sha256(seed.encode("utf-8")).digest()
    value = int.from_bytes(digest[:8], "big") / float(2**64 - 1)
    return value * scale


def build_card_trace(card_id: str, *, context_key: str, channel: str = "semantic") -> CardTrace:
    return CardTrace(
        card_id=card_id,
        amplitude=float(0.35 + _stable_float(f"A|{context_key}|{card_id}", 0.65)),
        phase=float(_stable_float(f"P|{context_key}|{card_id}", 2.0 * math.pi)),
        semantic_mass=float(0.15 + _stable_float(f"M|{card_id}", 0.85)),
        affective_weight=float(-1.0 + _stable_float(f"F|{context_key}|{card_id}", 2.0)),
        orbital_position=float(_stable_float(f"O|{card_id}", 1.0)),
        channel=channel,
    )


def infer_clusters(traces: list[CardTrace]) -> list[str]:
    by_channel: dict[str, int] = {}
    for trace in traces:
        by_channel[trace.channel] = by_channel.get(trace.channel, 0) + 1
    clusters = [f"{channel}:{count}" for channel, count in sorted(by_channel.items())]
    strong = [t.card_id for t in traces if t.amplitude * t.semantic_mass >= 0.55]
    if strong:
        clusters.append("strong:" + ",".join(sorted(strong)[:7]))
    return clusters


def layout_hash(traces: list[CardTrace], *, identity_anchor: str) -> str:
    payload = {
        "identity_anchor": identity_anchor,
        "traces": [
            {
                "card_id": t.card_id,
                "channel": t.channel,
                "amplitude": round(t.amplitude, 8),
                "phase": round(t.phase, 8),
                "semantic_mass": round(t.semantic_mass, 8),
                "affective_weight": round(t.affective_weight, 8),
                "orbital_position": round(t.orbital_position, 8),
            }
            for t in sorted(traces, key=lambda x: (x.channel, x.card_id))
        ],
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


def create_card_trace_snap(
    card_ids: Iterable[str],
    *,
    context_key: str,
    identity_anchor: str,
    channel_cycle: tuple[str, ...] = DEFAULT_TRACE_CHANNELS,
    t0: int = 0,
    t1: int = 128,
) -> CardTraceSnap:
    traces = [
        build_card_trace(card_id, context_key=context_key, channel=channel_cycle[idx % len(channel_cycle)])
        for idx, card_id in enumerate(card_ids)
    ]
    lhash = layout_hash(traces, identity_anchor=identity_anchor)
    snap_id = hashlib.sha256(f"{context_key}|{identity_anchor}|{lhash}".encode("utf-8")).hexdigest()[:24]

    trace_dicts = []
    for trace in traces:
        neighbours = sorted(
            (
                (other.card_id, abs(np.angle(np.exp(1j * (trace.phase - other.phase)))))
                for other in traces
                if other.card_id != trace.card_id
            ),
            key=lambda x: x[1],
        )[:3]
        item = asdict(trace)
        item["coupled_to"] = [name for name, _ in neighbours]
        item["trace_energy"] = float(trace.amplitude * trace.semantic_mass * (1.0 + abs(trace.affective_weight)))
        trace_dicts.append(item)

    return CardTraceSnap(
        snap_id=snap_id,
        schema="noema/card-trace-memory/v0.1",
        window={"t0": int(t0), "t1": int(t1)},
        active_traces=trace_dicts,
        clusters=infer_clusters(traces),
        layout_hash=lhash,
        identity_anchor=identity_anchor,
    )


def snap_similarity(now: CardTraceSnap, memory: CardTraceSnap) -> dict[str, Any]:
    now_map = {t["card_id"]: t for t in now.active_traces}
    mem_map = {t["card_id"]: t for t in memory.active_traces}
    common = sorted(set(now_map) & set(mem_map))
    if not common:
        return {"score": 0.0, "common_cards": [], "phase_alignment": 0.0, "amplitude_alignment": 0.0}

    phase_terms, amp_terms, affect_terms = [], [], []
    for card_id in common:
        a = now_map[card_id]
        b = mem_map[card_id]
        phase_delta = abs(np.angle(np.exp(1j * (float(a["phase"]) - float(b["phase"])))))
        phase_terms.append(max(0.0, 1.0 - phase_delta / math.pi))
        amp_terms.append(1.0 - min(1.0, abs(float(a["amplitude"]) - float(b["amplitude"]))))
        affect_terms.append(1.0 - min(1.0, abs(float(a["affective_weight"]) - float(b["affective_weight"])) / 2.0))

    phase_alignment = float(np.mean(phase_terms))
    amplitude_alignment = float(np.mean(amp_terms))
    affect_alignment = float(np.mean(affect_terms))
    coverage = len(common) / max(len(now_map), 1)
    score = float(0.36 * phase_alignment + 0.24 * amplitude_alignment + 0.20 * affect_alignment + 0.20 * coverage)
    return {
        "score": score,
        "common_cards": common,
        "phase_alignment": phase_alignment,
        "amplitude_alignment": amplitude_alignment,
        "affect_alignment": affect_alignment,
        "coverage": coverage,
        "memory_snap_id": memory.snap_id,
    }
