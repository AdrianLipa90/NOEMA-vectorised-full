"""CLI for derived function identities, relational closure, and dependency bundles."""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Sequence

from ciel_geometry.phasenav.dependency_audit import (
    audit_dependency_declarations,
    load_declared_dependency_index,
)
from ciel_geometry.phasenav.dependency_resolver import derive_dependency_package
from ciel_geometry.phasenav.entrypoint_dependency_bundle import (
    derive_entrypoint_bundles,
    load_project_entrypoints,
)
from ciel_geometry.phasenav.function_identity import scan_python_tree
from ciel_geometry.phasenav.relational_function_identity import derive_function_topology


def scan_payload(root: str | Path) -> dict[str, object]:
    root_path = Path(root)
    identities, dependencies = scan_python_tree(root_path)
    package = derive_dependency_package(dependencies)
    external_requirements = {
        item.import_root: item.requirement
        for item in package.resolved
        if item.requirement is not None and item.installed_version is not None
    }
    topology = derive_function_topology(
        identities,
        external_requirements=external_requirements,
    )

    declaration_audit: dict[str, object] | None = None
    entrypoint_bundles: list[dict[str, object]] = []
    pyproject = root_path / "pyproject.toml"
    if pyproject.is_file():
        declared = load_declared_dependency_index(pyproject)
        audit = audit_dependency_declarations(package, declared)
        declaration_audit = {
            "declared_matches": list(audit.declared_matches),
            "resolved_but_undeclared": list(audit.resolved_but_undeclared),
            "declared_not_resolved": list(audit.declared_not_resolved),
            "blocked_imports": list(audit.blocked_imports),
            "version_compatibility": audit.version_compatibility,
            "authority": "AUDIT_ONLY_NO_AUTOMATIC_REWRITE",
        }
        bundles = derive_entrypoint_bundles(
            identities,
            topology,
            load_project_entrypoints(pyproject),
        )
        entrypoint_bundles = [
            {
                "entrypoint": item.entrypoint,
                "declared_target": item.declared_target,
                "qualified_target": item.qualified_target,
                "state": item.state.value,
                "target_occurrence": item.target_occurrence,
                "target_relational_invariant": item.target_relational_invariant,
                "occurrences": list(item.occurrences),
                "symbols": list(item.symbols),
                "component_ids": list(item.component_ids),
                "environment_anchors": list(item.environment_anchors),
                "requirements": list(item.requirements),
                "blockers": list(item.blockers),
            }
            for item in bundles
        ]

    return {
        "schema": "CIELPC_FUNCTION_IDENTITY_SCAN_V1",
        "root": str(root_path),
        "identity_basis": "ALPHA_NORMALIZED_AST_SIGNATURE_AND_EXPLICIT_DEPENDENCIES",
        "thresholds": [],
        "functions": [
            {
                "source_path": item.source_path,
                "module": item.module,
                "qualified_name": item.qualified_name,
                "symbol_name": item.symbol_name,
                "signature": asdict(item.signature),
                "dependency_symbols": list(item.dependency_symbols),
                "import_roots": list(item.import_roots),
                "normalized_ast_sha256": item.normalized_ast_sha256,
                "invariant_sha256": item.invariant_sha256,
                "identity_scope": "STRUCTURAL_ONLY",
            }
            for item in identities
        ],
        "relational_closure": {
            "schema": "CIELPC_RELATIONAL_FUNCTION_CLOSURE_V1",
            "basis": "EXACT_BINDING_GRAPH_AND_DEPENDENCY_CLOSURE",
            "thresholds": [],
            "identities": [
                {
                    "occurrence_key": item.occurrence_key,
                    "source_path": item.source_path,
                    "qualified_name": item.qualified_name,
                    "structural_invariant": item.structural_invariant,
                    "relational_invariant": item.relational_invariant,
                    "state": item.state.value,
                    "internal_targets": list(item.internal_targets),
                    "environment_anchors": list(item.environment_anchors),
                    "closure_debt": list(item.closure_debt),
                }
                for item in topology.identities
            ],
            "bindings": [
                {
                    "source_occurrence": item.source_occurrence,
                    "source_qualified_name": item.source_qualified_name,
                    "dependency_symbol": item.dependency_symbol,
                    "state": item.state.value,
                    "target_occurrence": item.target_occurrence,
                    "target_qualified_name": item.target_qualified_name,
                    "environment_anchor": item.environment_anchor,
                    "candidates": list(item.candidates),
                    "reason": item.reason,
                }
                for item in topology.bindings
            ],
            "components": [
                {
                    "component_id": item.component_id,
                    "members": list(item.members),
                    "symbols": list(item.symbols),
                    "recursive": item.recursive,
                }
                for item in topology.components
            ],
            "condensation_edges": [list(edge) for edge in topology.condensation_edges],
            "authority": "DERIVED_READ_ONLY_NO_AUTOMATIC_REWRITE",
        },
        "entrypoint_dependency_bundles": {
            "schema": "CIELPC_ENTRYPOINT_DEPENDENCY_BUNDLES_V1",
            "basis": "DECLARED_ENTRYPOINT_EXACT_TRANSITIVE_RELATIONAL_CLOSURE",
            "thresholds": [],
            "bundles": entrypoint_bundles,
            "authority": "DERIVED_READ_ONLY_NO_AUTOMATIC_PACKAGE_REWRITE",
        },
        "dependencies": {
            "stdlib_imports": list(dependencies.stdlib_imports),
            "local_imports": list(dependencies.local_imports),
            "external_imports": list(dependencies.external_imports),
        },
        "derived_dependency_package": {
            "requirements": list(package.requirements),
            "blocked_imports": list(package.blocked_imports),
            "resolutions": [
                {
                    "import_root": item.import_root,
                    "state": item.state.value,
                    "candidates": list(item.candidates),
                    "selected_distribution": item.selected_distribution,
                    "installed_version": item.installed_version,
                    "requirement": item.requirement,
                    "evidence": list(item.evidence),
                }
                for item in package.resolved
            ],
        },
        "declaration_audit": declaration_audit,
    }


def _main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Derive CIELPC function identities and dependency package"
    )
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    payload = scan_payload(args.root)
    rendered = json.dumps(payload, indent=2, sort_keys=True)
    if args.output is None:
        print(rendered)
    else:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    return 0


def main() -> int:
    return _main()


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["main", "scan_payload"]
