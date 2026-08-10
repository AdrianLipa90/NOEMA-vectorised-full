from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ciel_geometry.phasenav.dependency_resolver import (
    ResolutionState,
    derive_dependency_package,
    resolve_distribution_dependencies,
)
from ciel_geometry.phasenav.function_identity import DependencyManifest


def _manifest(*external: str) -> DependencyManifest:
    return DependencyManifest((), (), tuple(external))


def test_unique_distribution_mapping_is_resolved_and_pinned():
    result = resolve_distribution_dependencies(
        _manifest("yaml"),
        package_map={"yaml": ("PyYAML",)},
        version_lookup=lambda name: "6.0.2" if name == "PyYAML" else "",
    )[0]
    assert result.state is ResolutionState.RESOLVED
    assert result.selected_distribution == "PyYAML"
    assert result.requirement == "PyYAML==6.0.2"


def test_multiple_distribution_candidates_remain_ambiguous():
    result = resolve_distribution_dependencies(
        _manifest("shared"),
        package_map={"shared": ("dist-b", "dist-a")},
        version_lookup=lambda name: "1.0",
    )[0]
    assert result.state is ResolutionState.AMBIGUOUS
    assert result.candidates == ("dist-a", "dist-b")
    assert result.selected_distribution is None
    assert result.requirement is None


def test_missing_distribution_mapping_remains_unresolved():
    result = resolve_distribution_dependencies(
        _manifest("mystery"),
        package_map={},
        version_lookup=lambda name: "1.0",
    )[0]
    assert result.state is ResolutionState.UNRESOLVED
    assert result.requirement is None


def test_version_lookup_failure_is_recorded_not_hidden():
    def fail_version(name: str) -> str:
        raise LookupError(f"no version for {name}")

    result = resolve_distribution_dependencies(
        _manifest("yaml"),
        package_map={"yaml": ("PyYAML",)},
        version_lookup=fail_version,
    )[0]
    assert result.state is ResolutionState.RESOLVED
    assert result.requirement == "PyYAML"
    assert any("LookupError" in item for item in result.evidence)


def test_dependency_package_contains_only_resolved_requirements():
    package = derive_dependency_package(
        _manifest("yaml", "shared", "mystery"),
        package_map={
            "yaml": ("PyYAML",),
            "shared": ("dist-a", "dist-b"),
        },
        version_lookup=lambda name: "6.0.2" if name == "PyYAML" else "1.0",
    )
    assert package.requirements == ("PyYAML==6.0.2",)
    assert package.blocked_imports == ("mystery", "shared")
