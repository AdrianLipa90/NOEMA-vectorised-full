"""Threshold-free dependency bundles derived from explicit project entrypoints.

A bundle is not a hand-authored package boundary. It is the exact transitive
closure reachable from one declared entrypoint through M8 internal bindings,
plus the environment anchors actually required by that closure.
"""
from __future__ import annotations

import tomllib
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Mapping, Sequence

from .function_identity import FunctionIdentity
from .relational_function_identity import (
    BindingState,
    ClosureState,
    FunctionTopology,
    occurrence_key,
)


class EntrypointState(str, Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    AMBIGUOUS = "AMBIGUOUS"
    UNRESOLVED = "UNRESOLVED"
    INVALID = "INVALID"


@dataclass(frozen=True)
class EntrypointDeclaration:
    name: str
    target: str
    module: str | None
    attribute: str | None
    qualified_target: str | None
    valid: bool
    reason: str = ""


@dataclass(frozen=True)
class EntrypointDependencyBundle:
    entrypoint: str
    declared_target: str
    qualified_target: str | None
    state: EntrypointState
    target_occurrence: str | None = None
    target_relational_invariant: str | None = None
    occurrences: tuple[str, ...] = ()
    symbols: tuple[str, ...] = ()
    component_ids: tuple[str, ...] = ()
    environment_anchors: tuple[str, ...] = ()
    requirements: tuple[str, ...] = ()
    blockers: tuple[str, ...] = ()


def parse_entrypoint_target(name: str, target: str) -> EntrypointDeclaration:
    raw = str(target).strip()
    if ":" not in raw:
        return EntrypointDeclaration(
            name=name,
            target=raw,
            module=None,
            attribute=None,
            qualified_target=None,
            valid=False,
            reason="entrypoint target must use module:attribute syntax",
        )
    module, attribute = (part.strip() for part in raw.split(":", 1))
    if not module or not attribute or any(not part for part in attribute.split(".")):
        return EntrypointDeclaration(
            name=name,
            target=raw,
            module=module or None,
            attribute=attribute or None,
            qualified_target=None,
            valid=False,
            reason="entrypoint module and attribute must be non-empty",
        )
    return EntrypointDeclaration(
        name=name,
        target=raw,
        module=module,
        attribute=attribute,
        qualified_target=f"{module}.{attribute}",
        valid=True,
    )


def load_project_entrypoints(pyproject: str | Path) -> tuple[EntrypointDeclaration, ...]:
    path = Path(pyproject)
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    scripts = data.get("project", {}).get("scripts", {})
    if not isinstance(scripts, dict):
        return ()
    return tuple(
        parse_entrypoint_target(str(name), str(target))
        for name, target in sorted(scripts.items(), key=lambda item: str(item[0]))
    )


def _target_index(identities: Sequence[FunctionIdentity]) -> dict[str, tuple[str, ...]]:
    index: dict[str, set[str]] = {}
    for item in identities:
        index.setdefault(item.qualified_name, set()).add(occurrence_key(item))
    return {name: tuple(sorted(keys)) for name, keys in index.items()}


def _internal_edges(topology: FunctionTopology) -> dict[str, set[str]]:
    graph = {item.occurrence_key: set() for item in topology.identities}
    for binding in topology.bindings:
        if binding.state is BindingState.INTERNAL and binding.target_occurrence is not None:
            graph.setdefault(binding.source_occurrence, set()).add(binding.target_occurrence)
    return graph


def _reachable(start: str, graph: Mapping[str, set[str]]) -> tuple[str, ...]:
    seen: set[str] = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        stack.extend(sorted(graph.get(node, ()), reverse=True))
    return tuple(sorted(seen))


def _requirement_from_anchor(anchor: str) -> str | None:
    if not anchor.startswith("distribution:"):
        return None
    _, rest = anchor.split("distribution:", 1)
    requirement, sep, _symbol = rest.partition(":")
    return requirement if sep and requirement else None


def derive_entrypoint_bundles(
    identities: Sequence[FunctionIdentity],
    topology: FunctionTopology,
    declarations: Sequence[EntrypointDeclaration],
) -> tuple[EntrypointDependencyBundle, ...]:
    """Derive one exact transitive dependency bundle per declared entrypoint."""

    targets = _target_index(identities)
    relationals = {item.occurrence_key: item for item in topology.identities}
    graph = _internal_edges(topology)
    component_for = {
        member: component.component_id
        for component in topology.components
        for member in component.members
    }
    bindings_by_source: dict[str, list] = {}
    for binding in topology.bindings:
        bindings_by_source.setdefault(binding.source_occurrence, []).append(binding)

    output: list[EntrypointDependencyBundle] = []
    for declaration in declarations:
        if not declaration.valid or declaration.qualified_target is None:
            output.append(
                EntrypointDependencyBundle(
                    entrypoint=declaration.name,
                    declared_target=declaration.target,
                    qualified_target=declaration.qualified_target,
                    state=EntrypointState.INVALID,
                    blockers=(declaration.reason or "invalid entrypoint declaration",),
                )
            )
            continue

        matches = targets.get(declaration.qualified_target, ())
        if not matches:
            output.append(
                EntrypointDependencyBundle(
                    entrypoint=declaration.name,
                    declared_target=declaration.target,
                    qualified_target=declaration.qualified_target,
                    state=EntrypointState.UNRESOLVED,
                    blockers=("declared target has no exact function occurrence",),
                )
            )
            continue
        if len(matches) > 1:
            output.append(
                EntrypointDependencyBundle(
                    entrypoint=declaration.name,
                    declared_target=declaration.target,
                    qualified_target=declaration.qualified_target,
                    state=EntrypointState.AMBIGUOUS,
                    blockers=tuple(f"candidate:{item}" for item in matches),
                )
            )
            continue

        target = matches[0]
        reachable = _reachable(target, graph)
        blockers: set[str] = set()
        anchors: set[str] = set()
        symbols: set[str] = set()
        requirements: set[str] = set()
        components: set[str] = set()

        for occurrence in reachable:
            relational = relationals[occurrence]
            symbols.add(relational.qualified_name)
            if component_for.get(occurrence):
                components.add(component_for[occurrence])
            if relational.state is not ClosureState.CLOSED:
                blockers.update(
                    f"{relational.qualified_name}:{debt}" for debt in relational.closure_debt
                )
            for binding in bindings_by_source.get(occurrence, ()):
                if binding.state is BindingState.ENVIRONMENT and binding.environment_anchor:
                    anchors.add(binding.environment_anchor)
                    requirement = _requirement_from_anchor(binding.environment_anchor)
                    if requirement:
                        requirements.add(requirement)
                elif binding.state not in (BindingState.INTERNAL, BindingState.ENVIRONMENT):
                    blockers.add(
                        f"{binding.source_qualified_name}:{binding.state.value}:{binding.dependency_symbol}"
                    )

        target_identity = relationals[target]
        state = EntrypointState.CLOSED if not blockers else EntrypointState.OPEN
        output.append(
            EntrypointDependencyBundle(
                entrypoint=declaration.name,
                declared_target=declaration.target,
                qualified_target=declaration.qualified_target,
                state=state,
                target_occurrence=target,
                target_relational_invariant=(
                    target_identity.relational_invariant
                    if target_identity.state is ClosureState.CLOSED
                    else None
                ),
                occurrences=reachable,
                symbols=tuple(sorted(symbols)),
                component_ids=tuple(sorted(components)),
                environment_anchors=tuple(sorted(anchors)),
                requirements=tuple(sorted(requirements)),
                blockers=tuple(sorted(blockers)),
            )
        )

    return tuple(sorted(output, key=lambda item: item.entrypoint))


__all__ = [
    "EntrypointDeclaration",
    "EntrypointDependencyBundle",
    "EntrypointState",
    "derive_entrypoint_bundles",
    "load_project_entrypoints",
    "parse_entrypoint_target",
]
