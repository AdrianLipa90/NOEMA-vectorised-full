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

    closure = payload["relational_closure"]
    assert closure["schema"] == "CIELPC_RELATIONAL_FUNCTION_CLOSURE_V1"
    assert closure["thresholds"] == []
    assert closure["authority"] == "DERIVED_READ_ONLY_NO_AUTOMATIC_REWRITE"
    assert len(closure["identities"]) == 1

    bundles = payload["entrypoint_dependency_bundles"]
    assert bundles["schema"] == "CIELPC_ENTRYPOINT_DEPENDENCY_BUNDLES_V1"
    assert bundles["thresholds"] == []
    assert bundles["bundles"] == []


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


def test_scan_payload_derives_bundle_from_project_script(tmp_path: Path):
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
