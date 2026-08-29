from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ciel_geometry.phasenav.entrypoint_dependency_bundle import (
    EntrypointState,
    derive_entrypoint_bundles,
    load_project_entrypoints,
    parse_entrypoint_target,
)
from ciel_geometry.phasenav.function_identity import identities_from_source
from ciel_geometry.phasenav.relational_function_identity import derive_function_topology


def test_parse_entrypoint_target_is_exact():
    item = parse_entrypoint_target("tool", "pkg.cli:main")
    assert item.valid is True
    assert item.qualified_target == "pkg.cli.main"

    invalid = parse_entrypoint_target("bad", "pkg.cli.main")
    assert invalid.valid is False
    assert invalid.qualified_target is None


def test_load_project_entrypoints_uses_declared_scripts_only(tmp_path: Path):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        "[project]\nname='x'\nversion='0'\n[project.scripts]\nb='pkg.b:main'\na='pkg.a:main'\n",
        encoding="utf-8",
    )
    items = load_project_entrypoints(pyproject)
    assert [item.name for item in items] == ["a", "b"]
    assert [item.qualified_target for item in items] == ["pkg.a.main", "pkg.b.main"]


def test_bundle_is_exact_transitive_entrypoint_closure_with_requirement():
    identities = identities_from_source(
        "import numpy as np\n"
        "def leaf(x):\n    return np.asarray(x)\n\n"
        "def helper(x):\n    return leaf(x)\n\n"
        "def main(x):\n    return helper(x)\n",
        module="app",
        source_path="app.py",
    )
    topology = derive_function_topology(
        identities,
        external_requirements={"numpy": "numpy==2.0.0"},
        runtime_id="CPython-test",
    )
    declaration = parse_entrypoint_target("app", "app:main")
    bundle = derive_entrypoint_bundles(identities, topology, (declaration,))[0]

    assert bundle.state is EntrypointState.CLOSED
    assert bundle.symbols == ("app.helper", "app.leaf", "app.main")
    assert bundle.requirements == ("numpy==2.0.0",)
    assert any("numpy.asarray" in item for item in bundle.environment_anchors)
    assert len(bundle.occurrences) == 3
    assert len(bundle.component_ids) == 3
    assert bundle.blockers == ()


def test_open_relational_debt_propagates_to_entrypoint_bundle():
    identities = identities_from_source(
        "def main(x):\n    return len(x)\n",
        module="app",
        source_path="app.py",
    )
    topology = derive_function_topology(identities, runtime_id="CPython-test")
    declaration = parse_entrypoint_target("app", "app:main")
    bundle = derive_entrypoint_bundles(identities, topology, (declaration,))[0]

    assert bundle.state is EntrypointState.OPEN
    assert bundle.target_relational_invariant is None
    assert any("UNRESOLVED:len" in blocker for blocker in bundle.blockers)


def test_unresolved_declared_target_stays_unresolved():
    identities = identities_from_source(
        "def main():\n    return 1\n", module="other", source_path="other.py"
    )
    topology = derive_function_topology(identities, runtime_id="CPython-test")
    declaration = parse_entrypoint_target("app", "missing:main")
    bundle = derive_entrypoint_bundles(identities, topology, (declaration,))[0]
    assert bundle.state is EntrypointState.UNRESOLVED
    assert bundle.target_occurrence is None


def test_duplicate_exact_target_is_ambiguous_without_first_match():
    left = identities_from_source(
        "def main():\n    return 1\n", module="app", source_path="left.py"
    )
    right = identities_from_source(
        "def main():\n    return 1\n", module="app", source_path="right.py"
    )
    identities = (*left, *right)
    topology = derive_function_topology(identities, runtime_id="CPython-test")
    declaration = parse_entrypoint_target("app", "app:main")
    bundle = derive_entrypoint_bundles(identities, topology, (declaration,))[0]
    assert bundle.state is EntrypointState.AMBIGUOUS
    assert len(bundle.blockers) == 2


def test_invalid_entrypoint_never_gets_guessed():
    identities = identities_from_source(
        "def main():\n    return 1\n", module="app", source_path="app.py"
    )
    topology = derive_function_topology(identities, runtime_id="CPython-test")
    declaration = parse_entrypoint_target("app", "app.main")
    bundle = derive_entrypoint_bundles(identities, topology, (declaration,))[0]
    assert bundle.state is EntrypointState.INVALID
