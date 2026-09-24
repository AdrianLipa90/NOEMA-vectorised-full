"""Semantic Collatz routing for CIELingo card-trace states.

Even steps reduce toward a stable identity/cluster. Odd steps expand semantic
neighbours before the route folds back toward reduction.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import hashlib


@dataclass(frozen=True)
class CollatzSemanticStep:
    index: int
    n_before: int
    n_after: int
    operation: str
    mode: str


def semantic_seed(layout_hash: str, *, modulus: int = 2_147_483_647) -> int:
    value = int(hashlib.sha256(layout_hash.encode("utf-8")).hexdigest()[:16], 16)
    return max(1, value % modulus)


def semantic_collatz_route(seed: int, *, max_steps: int = 32) -> list[CollatzSemanticStep]:
    n = int(seed)
    route: list[CollatzSemanticStep] = []
    for idx in range(max_steps):
        if n <= 1:
            break
        if n % 2 == 0:
            nxt = n // 2
            operation = "n/2"
            mode = "reduce"
        else:
            nxt = 3 * n + 1
            operation = "3n+1"
            mode = "expand"
        route.append(CollatzSemanticStep(idx, n, nxt, operation, mode))
        n = nxt
    return route


def route_summary(route: list[CollatzSemanticStep]) -> dict[str, Any]:
    reduce_count = sum(1 for step in route if step.mode == "reduce")
    expand_count = sum(1 for step in route if step.mode == "expand")
    return {
        "steps": len(route),
        "reduce_count": reduce_count,
        "expand_count": expand_count,
        "final_n": route[-1].n_after if route else 1,
        "dominant_mode": "reduce" if reduce_count >= expand_count else "expand",
        "route": [step.__dict__ for step in route],
    }
