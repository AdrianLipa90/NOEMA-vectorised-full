"""Audit declared project dependencies against the derived dependency package."""
from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from .dependency_resolver import DerivedDependencyPackage, ResolutionState

_NAME_RE = re.compile(r"^\s*([A-Za-z0-9][A-Za-z0-9._-]*)")
_NORMALIZE_RE = re.compile(r"[-_.]+")


@dataclass(frozen=True)
class DeclaredDependencyIndex:
    groups_by_distribution: Mapping[str, tuple[str, ...]]
    declared_spelling: Mapping[str, tuple[str, ...]]


@dataclass(frozen=True)
class DependencyDeclarationAudit:
    declared_matches: tuple[str, ...]
    resolved_but_undeclared: tuple[str, ...]
    declared_not_resolved: tuple[str, ...]
    blocked_imports: tuple[str, ...]
    version_compatibility: str = "UNKNOWN_NOT_EVALUATED"


def normalize_distribution_name(name: str) -> str:
    return _NORMALIZE_RE.sub("-", name).lower()


def dependency_name(requirement: str) -> str:
    match = _NAME_RE.match(requirement)
    if not match:
        raise ValueError(f"cannot derive distribution name from dependency declaration: {requirement!r}")
    return match.group(1)


def declared_dependency_index_from_toml(text: str) -> DeclaredDependencyIndex:
    payload = tomllib.loads(text)
    project = payload.get("project", {})
    groups: dict[str, set[str]] = {}
    spellings: dict[str, set[str]] = {}

    def ingest(items: object, group: str) -> None:
        if not isinstance(items, list):
            return
        for item in items:
            if not isinstance(item, str):
                raise ValueError(f"dependency declaration in group {group!r} must be a string")
            spelling = dependency_name(item)
            normalized = normalize_distribution_name(spelling)
            groups.setdefault(normalized, set()).add(group)
            spellings.setdefault(normalized, set()).add(spelling)

    ingest(project.get("dependencies", []), "core")
    optional = project.get("optional-dependencies", {})
    if isinstance(optional, dict):
        for group, items in sorted(optional.items()):
            ingest(items, f"optional:{group}")

    return DeclaredDependencyIndex(
        groups_by_distribution={key: tuple(sorted(value)) for key, value in sorted(groups.items())},
        declared_spelling={key: tuple(sorted(value)) for key, value in sorted(spellings.items())},
    )


def load_declared_dependency_index(path: str | Path) -> DeclaredDependencyIndex:
    return declared_dependency_index_from_toml(Path(path).read_text(encoding="utf-8"))


def audit_dependency_declarations(
    package: DerivedDependencyPackage,
    declared: DeclaredDependencyIndex,
) -> DependencyDeclarationAudit:
    resolved_names: set[str] = set()
    declared_matches: set[str] = set()
    undeclared: set[str] = set()

    for item in package.resolved:
        if item.state is not ResolutionState.RESOLVED or not item.selected_distribution:
            continue
        normalized = normalize_distribution_name(item.selected_distribution)
        resolved_names.add(normalized)
        if normalized in declared.groups_by_distribution:
            declared_matches.add(normalized)
        else:
            undeclared.add(normalized)

    declared_names = set(declared.groups_by_distribution)
    return DependencyDeclarationAudit(
        declared_matches=tuple(sorted(declared_matches)),
        resolved_but_undeclared=tuple(sorted(undeclared)),
        declared_not_resolved=tuple(sorted(declared_names - resolved_names)),
        blocked_imports=tuple(sorted(package.blocked_imports)),
    )


__all__ = [
    "DeclaredDependencyIndex",
    "DependencyDeclarationAudit",
    "audit_dependency_declarations",
    "declared_dependency_index_from_toml",
    "dependency_name",
    "load_declared_dependency_index",
    "normalize_distribution_name",
]
