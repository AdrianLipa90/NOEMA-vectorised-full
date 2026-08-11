"""Relational closure for threshold-free function identity.

M7 derives a structural invariant from one callable in isolation. This module
closes that invariant over exact bindings before it may act as a system-level
identity. Missing proof remains OPEN; no similarity threshold or first-match
rule is used.
"""
from __future__ import annotations

import builtins
import hashlib
import json
import platform
import sys
from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Sequence

from .function_identity import FunctionIdentity


class BindingState(str, Enum):
    INTERNAL = "INTERNAL"
    ENVIRONMENT = "ENVIRONMENT"
    AMBIGUOUS = "AMBIGUOUS"
    UNRESOLVED = "UNRESOLVED"
    DYNAMIC = "DYNAMIC"


class ClosureState(str, Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"


class RelationalFunctionRelation(str, Enum):
    SAME_IDENTITY = "SAME_IDENTITY"
    ALIAS = "ALIAS"
    CONFLICT = "CONFLICT"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class FunctionBinding:
    source_occurrence: str
    source_qualified_name: str
    dependency_symbol: str
    state: BindingState
    target_occurrence: str | None = None
    target_qualified_name: str | None = None
    environment_anchor: str | None = None
    candidates: tuple[str, ...] = ()
    reason: str = ""


@dataclass(frozen=True)
class RelationalFunctionIdentity:
    occurrence_key: str
    source_path: str
    qualified_name: str
    structural_invariant: str
    relational_invariant: str | None
    state: ClosureState
    internal_targets: tuple[str, ...] = ()
    environment_anchors: tuple[str, ...] = ()
    closure_debt: tuple[str, ...] = ()


@dataclass(frozen=True)
class RelationalFunctionComparison:
    relation: RelationalFunctionRelation
    left: str
    right: str
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class FunctionComponent:
    component_id: str
    members: tuple[str, ...]
    symbols: tuple[str, ...]
    recursive: bool


@dataclass(frozen=True)
class FunctionTopology:
    identities: tuple[RelationalFunctionIdentity, ...]
    bindings: tuple[FunctionBinding, ...]
    components: tuple[FunctionComponent, ...]
    condensation_edges: tuple[tuple[str, str], ...]


def _digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def _runtime_id() -> str:
    version = ".".join(str(item) for item in sys.version_info[:3])
    return f"{platform.python_implementation()}-{version}"


def occurrence_key(identity: FunctionIdentity) -> str:
    return "occurrence:" + _digest(
        {
            "source_path": identity.source_path,
            "qualified_name": identity.qualified_name,
            "structural_invariant": identity.invariant_sha256,
        }
    )


def _symbol_index(
    identities: Sequence[FunctionIdentity],
) -> dict[str, tuple[FunctionIdentity, ...]]:
    index: dict[str, list[FunctionIdentity]] = {}
    for item in identities:
        index.setdefault(item.qualified_name, []).append(item)
    return {
        name: tuple(sorted(items, key=lambda item: (item.source_path, item.invariant_sha256)))
        for name, items in index.items()
    }


def _candidate_names(source: FunctionIdentity, dependency_symbol: str) -> tuple[str, ...]:
    candidates = {dependency_symbol}
    if "." not in dependency_symbol and source.module:
        candidates.add(f"{source.module}.{dependency_symbol}")
    return tuple(sorted(candidates))


def _environment_anchor(
    dependency_symbol: str,
    *,
    external_requirements: Mapping[str, str],
    runtime_id: str,
) -> str | None:
    if dependency_symbol == "<dynamic-call>":
        return None
    root = dependency_symbol.split(".", 1)[0]

    # A direct builtin is used only when no exact internal binding exists.
    if "." not in dependency_symbol and hasattr(builtins, dependency_symbol):
        return f"python:{runtime_id}:builtins.{dependency_symbol}"

    if root in getattr(sys, "stdlib_module_names", ()):
        return f"python:{runtime_id}:stdlib:{dependency_symbol}"

    requirement = external_requirements.get(root)
    # An unversioned distribution does not close semantic identity.
    if requirement and "==" in requirement:
        return f"distribution:{requirement}:{dependency_symbol}"
    return None


def resolve_function_bindings(
    identities: Sequence[FunctionIdentity],
    *,
    external_requirements: Mapping[str, str] | None = None,
    runtime_id: str | None = None,
) -> tuple[FunctionBinding, ...]:
    """Resolve exact callable bindings without lexical first-match selection."""

    external_requirements = dict(external_requirements or {})
    runtime_id = runtime_id or _runtime_id()
    index = _symbol_index(identities)
    output: list[FunctionBinding] = []

    for source in identities:
        source_key = occurrence_key(source)
        for dependency_symbol in source.dependency_symbols:
            if dependency_symbol == "<dynamic-call>":
                output.append(
                    FunctionBinding(
                        source_occurrence=source_key,
                        source_qualified_name=source.qualified_name,
                        dependency_symbol=dependency_symbol,
                        state=BindingState.DYNAMIC,
                        reason="dynamic call target is not statically named",
                    )
                )
                continue

            candidate_names = _candidate_names(source, dependency_symbol)
            matches = [item for name in candidate_names for item in index.get(name, ())]
            unique_targets = {
                occurrence_key(item): item
                for item in matches
            }
            if len(unique_targets) == 1:
                target_key, target = next(iter(unique_targets.items()))
                output.append(
                    FunctionBinding(
                        source_occurrence=source_key,
                        source_qualified_name=source.qualified_name,
                        dependency_symbol=dependency_symbol,
                        state=BindingState.INTERNAL,
                        target_occurrence=target_key,
                        target_qualified_name=target.qualified_name,
                        candidates=tuple(sorted(name for name in candidate_names if name in index)),
                        reason="one exact internal binding",
                    )
                )
                continue
            if len(unique_targets) > 1:
                output.append(
                    FunctionBinding(
                        source_occurrence=source_key,
                        source_qualified_name=source.qualified_name,
                        dependency_symbol=dependency_symbol,
                        state=BindingState.AMBIGUOUS,
                        candidates=tuple(sorted(item.qualified_name for item in unique_targets.values())),
                        reason="exact binding set contains multiple occurrences; first-match forbidden",
                    )
                )
                continue

            anchor = _environment_anchor(
                dependency_symbol,
                external_requirements=external_requirements,
                runtime_id=runtime_id,
            )
            if anchor is not None:
                output.append(
                    FunctionBinding(
                        source_occurrence=source_key,
                        source_qualified_name=source.qualified_name,
                        dependency_symbol=dependency_symbol,
                        state=BindingState.ENVIRONMENT,
                        environment_anchor=anchor,
                        candidates=candidate_names,
                        reason="binding closed by explicit runtime/distribution identity",
                    )
                )
            else:
                output.append(
                    FunctionBinding(
                        source_occurrence=source_key,
                        source_qualified_name=source.qualified_name,
                        dependency_symbol=dependency_symbol,
                        state=BindingState.UNRESOLVED,
                        candidates=candidate_names,
                        reason="no exact internal or versioned environment binding",
                    )
                )

    return tuple(
        sorted(
            output,
            key=lambda item: (
                item.source_occurrence,
                item.dependency_symbol,
                item.state.value,
                item.target_occurrence or "",
                item.environment_anchor or "",
            ),
        )
    )


def _internal_graph(
    identities: Sequence[FunctionIdentity],
    bindings: Sequence[FunctionBinding],
) -> dict[str, set[str]]:
    graph = {occurrence_key(item): set() for item in identities}
    for binding in bindings:
        if binding.state is BindingState.INTERNAL and binding.target_occurrence is not None:
            graph[binding.source_occurrence].add(binding.target_occurrence)
    return graph


def _scc(graph: Mapping[str, set[str]]) -> tuple[tuple[str, ...], ...]:
    index = 0
    indices: dict[str, int] = {}
    low: dict[str, int] = {}
    stack: list[str] = []
    on_stack: set[str] = set()
    output: list[tuple[str, ...]] = []

    def visit(node: str) -> None:
        nonlocal index
        indices[node] = index
        low[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)
        for target in sorted(graph.get(node, ())):
            if target not in indices:
                visit(target)
                low[node] = min(low[node], low[target])
            elif target in on_stack:
                low[node] = min(low[node], indices[target])
        if low[node] == indices[node]:
            members: list[str] = []
            while True:
                member = stack.pop()
                on_stack.remove(member)
                members.append(member)
                if member == node:
                    break
            output.append(tuple(sorted(members)))

    for node in sorted(graph):
        if node not in indices:
            visit(node)
    return tuple(sorted(output))


def derive_function_topology(
    identities: Sequence[FunctionIdentity],
    *,
    external_requirements: Mapping[str, str] | None = None,
    runtime_id: str | None = None,
) -> FunctionTopology:
    bindings = resolve_function_bindings(
        identities,
        external_requirements=external_requirements,
        runtime_id=runtime_id,
    )
    by_occurrence = {occurrence_key(item): item for item in identities}
    graph = _internal_graph(identities, bindings)
    components_raw = _scc(graph)
    component_for: dict[str, str] = {}
    components: list[FunctionComponent] = []
    recursive_members: set[str] = set()

    for members in components_raw:
        recursive = len(members) > 1 or any(member in graph[member] for member in members)
        if recursive:
            recursive_members.update(members)
        component_id = "component-instance:" + _digest({"members": list(members)})
        symbols = tuple(sorted(by_occurrence[item].qualified_name for item in members))
        components.append(FunctionComponent(component_id, members, symbols, recursive))
        for member in members:
            component_for[member] = component_id

    condensation = {
        (component_for[source], component_for[target])
        for source, targets in graph.items()
        for target in targets
        if component_for[source] != component_for[target]
    }

    bindings_by_source: dict[str, list[FunctionBinding]] = {}
    for binding in bindings:
        bindings_by_source.setdefault(binding.source_occurrence, []).append(binding)

    memo: dict[str, RelationalFunctionIdentity] = {}
    active: set[str] = set()

    def close(node: str) -> RelationalFunctionIdentity:
        if node in memo:
            return memo[node]
        item = by_occurrence[node]
        debt: set[str] = set()
        internal_targets: list[str] = []
        anchors: list[str] = []

        if node in recursive_members or node in active:
            debt.add("recursive dependency component requires separate cycle proof")
        else:
            active.add(node)
            for binding in bindings_by_source.get(node, ()):
                if binding.state is BindingState.INTERNAL and binding.target_occurrence is not None:
                    target = close(binding.target_occurrence)
                    internal_targets.append(binding.target_occurrence)
                    if target.state is ClosureState.CLOSED and target.relational_invariant is not None:
                        anchors.append(
                            f"internal:{binding.dependency_symbol}:{target.relational_invariant}"
                        )
                    else:
                        debt.add(f"open internal target:{binding.dependency_symbol}")
                elif binding.state is BindingState.ENVIRONMENT and binding.environment_anchor:
                    anchors.append(f"environment:{binding.dependency_symbol}:{binding.environment_anchor}")
                else:
                    debt.add(f"{binding.state.value.lower()}:{binding.dependency_symbol}")
            active.remove(node)

        state = ClosureState.CLOSED if not debt else ClosureState.OPEN
        relational = (
            _digest(
                {
                    "structural_invariant": item.invariant_sha256,
                    "dependency_anchors": sorted(anchors),
                }
            )
            if state is ClosureState.CLOSED
            else None
        )
        result = RelationalFunctionIdentity(
            occurrence_key=node,
            source_path=item.source_path,
            qualified_name=item.qualified_name,
            structural_invariant=item.invariant_sha256,
            relational_invariant=relational,
            state=state,
            internal_targets=tuple(sorted(set(internal_targets))),
            environment_anchors=tuple(sorted(set(anchors))),
            closure_debt=tuple(sorted(debt)),
        )
        memo[node] = result
        return result

    relational = tuple(sorted((close(node) for node in by_occurrence), key=lambda item: item.occurrence_key))
    return FunctionTopology(
        identities=relational,
        bindings=bindings,
        components=tuple(sorted(components, key=lambda item: item.component_id)),
        condensation_edges=tuple(sorted(condensation)),
    )


def compare_relational_functions(
    left: RelationalFunctionIdentity,
    right: RelationalFunctionIdentity,
) -> RelationalFunctionComparison:
    same_symbol = left.qualified_name == right.qualified_name
    both_closed = left.state is ClosureState.CLOSED and right.state is ClosureState.CLOSED
    same_identity = (
        both_closed
        and left.relational_invariant is not None
        and left.relational_invariant == right.relational_invariant
    )
    if same_symbol and same_identity:
        relation = RelationalFunctionRelation.SAME_IDENTITY
        reasons = ("same qualified symbol and closed relational invariant",)
    elif same_identity:
        relation = RelationalFunctionRelation.ALIAS
        reasons = ("different symbols share one closed relational invariant",)
    elif same_symbol and both_closed:
        relation = RelationalFunctionRelation.CONFLICT
        reasons = ("same qualified symbol has different closed relational invariants",)
    else:
        relation = RelationalFunctionRelation.UNKNOWN
        reasons = ("relational closure is incomplete or invariants differ without symbol conflict",)
    return RelationalFunctionComparison(relation, left.qualified_name, right.qualified_name, reasons)


__all__ = [
    "BindingState",
    "ClosureState",
    "FunctionBinding",
    "FunctionComponent",
    "FunctionTopology",
    "RelationalFunctionComparison",
    "RelationalFunctionIdentity",
    "RelationalFunctionRelation",
    "compare_relational_functions",
    "derive_function_topology",
    "occurrence_key",
    "resolve_function_bindings",
]
