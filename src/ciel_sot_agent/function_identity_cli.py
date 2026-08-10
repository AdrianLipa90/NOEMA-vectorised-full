"""CLI for derived function identities and dependency packages."""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Sequence

from ciel_geometry.phasenav.dependency_resolver import derive_dependency_package
from ciel_geometry.phasenav.function_identity import scan_python_tree


def scan_payload(root: str | Path) -> dict[str, object]:
    identities, dependencies = scan_python_tree(root)
    package = derive_dependency_package(dependencies)
    return {
        "schema": "CIELPC_FUNCTION_IDENTITY_SCAN_V1",
        "root": str(Path(root)),
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
            }
            for item in identities
        ],
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
