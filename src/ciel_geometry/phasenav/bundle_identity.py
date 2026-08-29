"""Exact, threshold-free identity for CLOSED M9 execution bundles.

Bundle identity deliberately excludes entrypoint names, source paths, and
filesystem package boundaries. It is derived from the closed relational graph
and environment anchors only.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from dataclasses import dataclass
from enum import Enum
from typing import Sequence

from .entrypoint_dependency_bundle import EntrypointDependencyBundle, EntrypointState
from .relational_function_identity import BindingState, ClosureState, FunctionTopology


class BundleIdentityState(str, Enum):
    DERIVED = "DERIVED"
    OPEN = "OPEN"


@dataclass(frozen=True)
class DerivedBundleIdentity:
    entrypoint: str
    state: BundleIdentityState
    bundle_invariant: str | None
    bundle_id: str | None
    target_relational_invariant: str | None
    relational_node_multiset: tuple[tuple[str, int], ...] = ()
    internal_edge_multiset: tuple[tuple[str, str, int], ...] = ()
    environment_edge_multiset: tuple[tuple[str, str, int], ...] = ()
    requirements: tuple[str, ...] = ()
    blockers: tuple[str, ...] = ()


@dataclass(frozen=True)
class BundleIdentityGroup:
    bundle_invariant: str
    bundle_id: str
    entrypoints: tuple[str, ...]
    requirements: tuple[str, ...]


def _digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def _counter_items(counter: Counter[str]) -> tuple[tuple[str, int], ...]:
    return tuple(sorted((key, int(value)) for key, value in counter.items()))


def derive_bundle_identity(
    bundle: EntrypointDependencyBundle,
    topology: FunctionTopology,
) -> DerivedBundleIdentity:
    """Derive one path/name-independent identity from a CLOSED M9 bundle."""

    if bundle.state is not EntrypointState.CLOSED or bundle.target_occurrence is None:
        return DerivedBundleIdentity(
            entrypoint=bundle.entrypoint,
            state=BundleIdentityState.OPEN,
            bundle_invariant=None,
            bundle_id=None,
            target_relational_invariant=bundle.target_relational_invariant,
            requirements=bundle.requirements,
            blockers=tuple(sorted(set(bundle.blockers) | {"entrypoint bundle is not CLOSED"})),
        )

    reachable = set(bundle.occurrences)
    relational = {item.occurrence_key: item for item in topology.identities}
    blockers: set[str] = set()
    node_counts: Counter[str] = Counter()
    internal_edges: Counter[tuple[str, str]] = Counter()
    environment_edges: Counter[tuple[str, str]] = Counter()

    for occurrence in sorted(reachable):
        item = relational.get(occurrence)
        if item is None:
            blockers.add(f"missing relational occurrence:{occurrence}")
            continue
        if item.state is not ClosureState.CLOSED or item.relational_invariant is None:
            blockers.add(f"open relational occurrence:{item.qualified_name}")
            continue
        node_counts[item.relational_invariant] += 1

    for binding in topology.bindings:
        if binding.source_occurrence not in reachable:
            continue
        source = relational.get(binding.source_occurrence)
        if source is None or source.relational_invariant is None:
            blockers.add(f"binding source has no closed relational identity:{binding.source_occurrence}")
            continue
        if binding.state is BindingState.INTERNAL:
            if binding.target_occurrence is None or binding.target_occurrence not in reachable:
                blockers.add(
                    f"internal edge escapes bundle:{binding.source_qualified_name}:{binding.dependency_symbol}"
                )
                continue
            target = relational.get(binding.target_occurrence)
            if target is None or target.relational_invariant is None:
                blockers.add(
                    f"internal edge target has no closed relational identity:{binding.dependency_symbol}"
                )
                continue
            internal_edges[(source.relational_invariant, target.relational_invariant)] += 1
        elif binding.state is BindingState.ENVIRONMENT:
            if not binding.environment_anchor:
                blockers.add(
                    f"environment edge lacks anchor:{binding.source_qualified_name}:{binding.dependency_symbol}"
                )
                continue
            environment_edges[(source.relational_invariant, binding.environment_anchor)] += 1
        else:
            blockers.add(
                f"non-closed binding in CLOSED bundle:{binding.source_qualified_name}:"
                f"{binding.state.value}:{binding.dependency_symbol}"
            )

    target = relational.get(bundle.target_occurrence)
    if target is None or target.relational_invariant is None:
        blockers.add("target occurrence has no closed relational identity")
        target_relational = None
    else:
        target_relational = target.relational_invariant

    if blockers:
        return DerivedBundleIdentity(
            entrypoint=bundle.entrypoint,
            state=BundleIdentityState.OPEN,
            bundle_invariant=None,
            bundle_id=None,
            target_relational_invariant=target_relational,
            relational_node_multiset=_counter_items(node_counts),
            internal_edge_multiset=tuple(
                sorted((source, target_id, count) for (source, target_id), count in internal_edges.items())
            ),
            environment_edge_multiset=tuple(
                sorted((source, anchor, count) for (source, anchor), count in environment_edges.items())
            ),
            requirements=bundle.requirements,
            blockers=tuple(sorted(blockers)),
        )

    node_multiset = _counter_items(node_counts)
    internal_multiset = tuple(
        sorted((source, target_id, count) for (source, target_id), count in internal_edges.items())
    )
    environment_multiset = tuple(
        sorted((source, anchor, count) for (source, anchor), count in environment_edges.items())
    )
    payload = {
        "schema": "CIELPC_ENTRYPOINT_BUNDLE_IDENTITY_V1",
        "target_relational_invariant": target_relational,
        "relational_node_multiset": node_multiset,
        "internal_edge_multiset": internal_multiset,
        "environment_edge_multiset": environment_multiset,
        "requirements": tuple(sorted(bundle.requirements)),
    }
    invariant = _digest(payload)
    return DerivedBundleIdentity(
        entrypoint=bundle.entrypoint,
        state=BundleIdentityState.DERIVED,
        bundle_invariant=invariant,
        bundle_id=f"bundle:{invariant}",
        target_relational_invariant=target_relational,
        relational_node_multiset=node_multiset,
        internal_edge_multiset=internal_multiset,
        environment_edge_multiset=environment_multiset,
        requirements=tuple(sorted(bundle.requirements)),
        blockers=(),
    )


def derive_bundle_identities(
    bundles: Sequence[EntrypointDependencyBundle],
    topology: FunctionTopology,
) -> tuple[DerivedBundleIdentity, ...]:
    return tuple(
        sorted(
            (derive_bundle_identity(bundle, topology) for bundle in bundles),
            key=lambda item: item.entrypoint,
        )
    )


def group_equivalent_bundles(
    identities: Sequence[DerivedBundleIdentity],
) -> tuple[BundleIdentityGroup, ...]:
    grouped: dict[str, list[DerivedBundleIdentity]] = {}
    for item in identities:
        if item.state is BundleIdentityState.DERIVED and item.bundle_invariant:
            grouped.setdefault(item.bundle_invariant, []).append(item)

    output: list[BundleIdentityGroup] = []
    for invariant, items in sorted(grouped.items()):
        requirements = {item.requirements for item in items}
        if len(requirements) != 1:
            # This should be impossible because requirements are identity-bearing.
            continue
        output.append(
            BundleIdentityGroup(
                bundle_invariant=invariant,
                bundle_id=f"bundle:{invariant}",
                entrypoints=tuple(sorted(item.entrypoint for item in items)),
                requirements=next(iter(requirements)),
            )
        )
    return tuple(output)


__all__ = [
    "BundleIdentityGroup",
    "BundleIdentityState",
    "DerivedBundleIdentity",
    "derive_bundle_identities",
    "derive_bundle_identity",
    "group_equivalent_bundles",
]
