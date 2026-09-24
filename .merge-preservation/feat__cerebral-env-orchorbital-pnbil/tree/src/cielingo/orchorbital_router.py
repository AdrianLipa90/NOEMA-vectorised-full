"""OrchORbital router over CIELingo Card Trace EEG.

This router consumes a current card-trace EEG snap, memory snaps and a Semantic
Collatz route, then emits an association/reduction/expansion decision.

It is a project analog, not a biological Orch-OR proof.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .card_trace_eeg import CardTraceSnap, snap_similarity
from .semantic_collatz import route_summary, semantic_collatz_route, semantic_seed


@dataclass(frozen=True)
class OrchORbitalDecision:
    schema: str
    operator: str
    selected_memory_snap_id: str | None
    association_score: float
    route_summary: dict[str, Any]
    decision: str
    execution_layer: str = "fallback_cpu_ram"
    source_role: str = "orchorbital_router_reference_surface"
    nonlocal_claim_allowed: bool = False
    primary_noema_runtime_available: bool = False
    not_biological_orchor_claim: bool = True

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "operator": self.operator,
            "selected_memory_snap_id": self.selected_memory_snap_id,
            "association_score": self.association_score,
            "route_summary": self.route_summary,
            "decision": self.decision,
            "execution_layer": self.execution_layer,
            "source_role": self.source_role,
            "nonlocal_claim_allowed": self.nonlocal_claim_allowed,
            "primary_noema_runtime_available": self.primary_noema_runtime_available,
            "not_biological_orchor_claim": self.not_biological_orchor_claim,
        }


def route_orchorbital(
    current: CardTraceSnap,
    memories: list[CardTraceSnap],
    *,
    association_threshold: float = 0.42,
    max_collatz_steps: int = 32,
) -> OrchORbitalDecision:
    comparisons = [snap_similarity(current, memory) for memory in memories]
    best = max(comparisons, key=lambda item: item["score"], default=None)

    seed = semantic_seed(current.layout_hash)
    route = semantic_collatz_route(seed, max_steps=max_collatz_steps)
    summary = route_summary(route)

    if best and best["score"] >= association_threshold:
        decision = "associate_memory_snap"
        selected = best["memory_snap_id"]
        score = float(best["score"])
    elif summary["dominant_mode"] == "expand":
        decision = "expand_semantic_neighbours"
        selected = None
        score = float(best["score"]) if best else 0.0
    else:
        decision = "reduce_to_identity_cluster"
        selected = None
        score = float(best["score"]) if best else 0.0

    return OrchORbitalDecision(
        schema="noema/orchorbital-router-decision/v0.1",
        operator="ORCHORBITAL_CARD_TRACE_ROUTER",
        selected_memory_snap_id=selected,
        association_score=score,
        route_summary=summary,
        decision=decision,
    )
