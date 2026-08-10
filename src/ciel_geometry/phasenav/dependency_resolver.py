"""Resolve external import roots into distribution requirements without first-match rules."""
from __future__ import annotations

import importlib.metadata
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Mapping, Sequence

from .function_identity import DependencyManifest


class ResolutionState(str, Enum):
    RESOLVED = "RESOLVED"
    AMBIGUOUS = "AMBIGUOUS"
    UNRESOLVED = "UNRESOLVED"


@dataclass(frozen=True)
class DistributionResolution:
    import_root: str
    state: ResolutionState
    candidates: tuple[str, ...]
    selected_distribution: str | None = None
    installed_version: str | None = None
    requirement: str | None = None
    evidence: tuple[str, ...] = ()


@dataclass(frozen=True)
class DerivedDependencyPackage:
    requirements: tuple[str, ...]
    resolved: tuple[DistributionResolution, ...]
    blocked_imports: tuple[str, ...]


def resolve_distribution_dependencies(
    manifest: DependencyManifest,
    *,
    package_map: Mapping[str, Sequence[str]] | None = None,
    version_lookup: Callable[[str], str] | None = None,
) -> tuple[DistributionResolution, ...]:
    """Resolve observed external import roots using explicit package metadata.

    A root with zero candidates remains UNRESOLVED. More than one candidate is
    AMBIGUOUS. No lexical ordering or first-match choice is permitted.
    """

    if package_map is None:
        try:
            package_map = importlib.metadata.packages_distributions()
        except Exception:
            package_map = {}
    if version_lookup is None:
        version_lookup = importlib.metadata.version

    output: list[DistributionResolution] = []
    for import_root in manifest.external_imports:
        candidates = tuple(sorted(set(package_map.get(import_root, ()))))
        if not candidates:
            output.append(
                DistributionResolution(
                    import_root=import_root,
                    state=ResolutionState.UNRESOLVED,
                    candidates=(),
                    evidence=("no distribution mapping evidence",),
                )
            )
            continue
        if len(candidates) > 1:
            output.append(
                DistributionResolution(
                    import_root=import_root,
                    state=ResolutionState.AMBIGUOUS,
                    candidates=candidates,
                    evidence=("multiple distribution mappings observed; first-match forbidden",),
                )
            )
            continue

        distribution = candidates[0]
        version: str | None
        try:
            version = str(version_lookup(distribution))
        except Exception:
            version = None
        requirement = f"{distribution}=={version}" if version else distribution
        output.append(
            DistributionResolution(
                import_root=import_root,
                state=ResolutionState.RESOLVED,
                candidates=candidates,
                selected_distribution=distribution,
                installed_version=version,
                requirement=requirement,
                evidence=("unique package metadata mapping",),
            )
        )
    return tuple(output)


def derive_dependency_package(
    manifest: DependencyManifest,
    *,
    package_map: Mapping[str, Sequence[str]] | None = None,
    version_lookup: Callable[[str], str] | None = None,
) -> DerivedDependencyPackage:
    resolutions = resolve_distribution_dependencies(
        manifest,
        package_map=package_map,
        version_lookup=version_lookup,
    )
    requirements = tuple(
        sorted(
            item.requirement
            for item in resolutions
            if item.state is ResolutionState.RESOLVED and item.requirement is not None
        )
    )
    blocked = tuple(
        sorted(item.import_root for item in resolutions if item.state is not ResolutionState.RESOLVED)
    )
    return DerivedDependencyPackage(
        requirements=requirements,
        resolved=resolutions,
        blocked_imports=blocked,
    )


__all__ = [
    "DerivedDependencyPackage",
    "DistributionResolution",
    "ResolutionState",
    "derive_dependency_package",
    "resolve_distribution_dependencies",
]
