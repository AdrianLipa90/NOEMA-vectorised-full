from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ciel_sot_agent.function_identity_cli import scan_payload


def test_scan_payload_is_explicitly_threshold_free(tmp_path: Path):
    source = tmp_path / "sample.py"
    source.write_text(
        "import json\nimport numpy as np\ndef f(x):\n    return np.asarray(x)\n",
        encoding="utf-8",
    )
    payload = scan_payload(tmp_path)
    assert payload["schema"] == "CIELPC_FUNCTION_IDENTITY_SCAN_V1"
    assert payload["thresholds"] == []
    dependencies = payload["dependencies"]
    assert "json" in dependencies["stdlib_imports"]
    assert "numpy" in dependencies["external_imports"]
    assert len(payload["functions"]) == 1
    assert payload["functions"][0]["identity_scope"] == "STRUCTURAL_ONLY"

    module_context = payload["module_context_dependencies"]
    assert module_context["schema"] == "CIELPC_MODULE_CONTEXT_DEPENDENCIES_V1"
    assert module_context["thresholds"] == []
    assert module_context["authority"] == "DERIVED_READ_ONLY_NO_SOURCE_REWRITE"

    closure = payload["relational_closure"]
    assert closure["schema"] == "CIELPC_RELATIONAL_FUNCTION_CLOSURE_V1"
    assert closure["thresholds"] == []
    assert closure["authority"] == "DERIVED_READ_ONLY_NO_AUTOMATIC_REWRITE"
    assert len(closure["identities"]) == 1

    bundles = payload["entrypoint_dependency_bundles"]
    assert bundles["schema"] == "CIELPC_ENTRYPOINT_DEPENDENCY_BUNDLES_V1"
    assert bundles["thresholds"] == []
    assert bundles["bundles"] == []

    bundle_ids = payload["bundle_identities"]
    assert bundle_ids["schema"] == "CIELPC_ENTRYPOINT_BUNDLE_IDENTITY_V1"
    assert bundle_ids["thresholds"] == []
    assert bundle_ids["identities"] == []
    assert bundle_ids["equivalence_groups"] == []


def test_scan_payload_exposes_exact_internal_binding_and_condensation(tmp_path: Path):
    source = tmp_path / "sample.py"
    source.write_text(
        "def helper():\n    return 1\n\ndef f():\n    return helper()\n",
        encoding="utf-8",
    )
    payload = scan_payload(tmp_path)
    closure = payload["relational_closure"]
    binding = next(
        item for item in closure["bindings"] if item["source_qualified_name"] == "sample.f"
    )
    assert binding["state"] == "INTERNAL"
    assert binding["target_qualified_name"] == "sample.helper"
    identities = {item["qualified_name"]: item for item in closure["identities"]}
    assert identities["sample.helper"]["state"] == "CLOSED"
    assert identities["sample.f"]["state"] == "CLOSED"
    assert closure["condensation_edges"]


def test_scan_payload_derives_bundle_and_identity_from_project_script(tmp_path: Path):
    source = tmp_path / "app.py"
    source.write_text(
        "def helper():\n    return 1\n\ndef main():\n    return helper()\n",
        encoding="utf-8",
    )
    (tmp_path / "pyproject.toml").write_text(
        "[project]\nname='demo'\nversion='0'\n[project.scripts]\ndemo='app:main'\n",
        encoding="utf-8",
    )
    payload = scan_payload(tmp_path)
    bundle_group = payload["entrypoint_dependency_bundles"]
    assert bundle_group["basis"] == "DECLARED_ENTRYPOINT_EXACT_TRANSITIVE_RELATIONAL_CLOSURE"
    assert bundle_group["authority"] == "DERIVED_READ_ONLY_NO_AUTOMATIC_PACKAGE_REWRITE"
    assert len(bundle_group["bundles"]) == 1
    bundle = bundle_group["bundles"][0]
    assert bundle["entrypoint"] == "demo"
    assert bundle["qualified_target"] == "app.main"
    assert bundle["state"] == "CLOSED"
    assert bundle["symbols"] == ["app.helper", "app.main"]
    assert bundle["blockers"] == []

    identity_group = payload["bundle_identities"]
    assert identity_group["basis"] == "CLOSED_RELATIONAL_GRAPH_MULTISET_AND_ENVIRONMENT_EDGES"
    assert identity_group["authority"] == "DERIVED_READ_ONLY_NO_AUTOMATIC_DEDUP_APPLY"
    assert len(identity_group["identities"]) == 1
    identity = identity_group["identities"][0]
    assert identity["entrypoint"] == "demo"
    assert identity["state"] == "DERIVED"
    assert identity["bundle_id"].startswith("bundle:")
    assert identity["blockers"] == []
    assert identity_group["equivalence_groups"][0]["entrypoints"] == ["demo"]


def test_scan_payload_relative_import_is_resolved_with_provenance(tmp_path: Path):
    package = tmp_path / "src" / "pkg"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "helper.py").write_text("def helper():\n    return 1\n", encoding="utf-8")
    (package / "main.py").write_text(
        "from .helper import helper\n\ndef main():\n    return helper()\n",
        encoding="utf-8",
    )
    (tmp_path / "pyproject.toml").write_text(
        "[project]\nname='demo'\nversion='0'\n[project.scripts]\ndemo='pkg.main:main'\n",
        encoding="utf-8",
    )

    payload = scan_payload(tmp_path)
    context = payload["module_context_dependencies"]
    rewrites = context["function_dependency_rewrites"]["pkg.main.main"]
    assert rewrites["helper.helper"] == "pkg.helper.helper"

    binding = next(
        item
        for item in payload["relational_closure"]["bindings"]
        if item["source_qualified_name"] == "pkg.main.main"
    )
    assert binding["observed_dependency_symbol"] == "helper.helper"
    assert binding["dependency_symbol"] == "pkg.helper.helper"
    assert binding["state"] == "INTERNAL"
    assert binding["target_qualified_name"] == "pkg.helper.helper"

    bundle = payload["entrypoint_dependency_bundles"]["bundles"][0]
    assert bundle["state"] == "CLOSED"
    assert bundle["symbols"] == ["pkg.helper.helper", "pkg.main.main"]
    identity = payload["bundle_identities"]["identities"][0]
    assert identity["state"] == "DERIVED"
    assert identity["bundle_id"].startswith("bundle:")
