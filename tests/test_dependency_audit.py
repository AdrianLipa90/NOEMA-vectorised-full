from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ciel_geometry.phasenav.dependency_audit import (
    audit_dependency_declarations,
    declared_dependency_index_from_toml,
    normalize_distribution_name,
)
from ciel_geometry.phasenav.dependency_resolver import derive_dependency_package
from ciel_geometry.phasenav.function_identity import DependencyManifest


def test_distribution_name_normalization_is_pep503_style():
    assert normalize_distribution_name("Py_YAML") == "py-yaml"
    assert normalize_distribution_name("my.pkg-name") == "my-pkg-name"


def test_declared_index_preserves_core_and_optional_groups():
    index = declared_dependency_index_from_toml(
        """
[project]
dependencies = ["numpy>=1.26", "PyYAML>=6"]
[project.optional-dependencies]
omega = ["networkx>=3"]
"""
    )
    assert index.groups_by_distribution["numpy"] == ("core",)
    assert index.groups_by_distribution["pyyaml"] == ("core",)
    assert index.groups_by_distribution["networkx"] == ("optional:omega",)


def test_declared_dependencies_are_claims_not_authority():
    manifest = DependencyManifest((), (), ("numpy", "yaml", "mystery"))
    package = derive_dependency_package(
        manifest,
        package_map={
            "numpy": ("numpy",),
            "yaml": ("PyYAML",),
        },
        version_lookup=lambda name: {"numpy": "2.0.0", "PyYAML": "6.0.2"}[name],
    )
    declared = declared_dependency_index_from_toml(
        """
[project]
dependencies = ["numpy>=1.26", "scipy>=1.14"]
"""
    )
    audit = audit_dependency_declarations(package, declared)
    assert audit.declared_matches == ("numpy",)
    assert audit.resolved_but_undeclared == ("pyyaml",)
    assert audit.declared_not_resolved == ("scipy",)
    assert audit.blocked_imports == ("mystery",)
    assert audit.version_compatibility == "UNKNOWN_NOT_EVALUATED"
