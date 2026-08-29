from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ciel_geometry.phasenav.function_identity import scan_python_tree
from ciel_geometry.phasenav.module_context_dependencies import scan_module_context
from ciel_geometry.phasenav.relational_function_identity import (
    BindingState,
    ClosureState,
    derive_function_topology,
)


def _package_tree(tmp_path: Path) -> Path:
    package = tmp_path / "src" / "pkg"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "helper.py").write_text(
        "def helper():\n    return 1\n",
        encoding="utf-8",
    )
    return package


def test_relative_import_rewrite_resolves_exact_internal_function(tmp_path: Path):
    package = _package_tree(tmp_path)
    (package / "main.py").write_text(
        "from .helper import helper\n\ndef main():\n    return helper()\n",
        encoding="utf-8",
    )

    identities, _legacy = scan_python_tree(tmp_path)
    context = scan_module_context(tmp_path)
    topology = derive_function_topology(
        identities,
        dependency_rewrites=context.function_dependency_rewrites,
        runtime_id="CPython-test",
    )

    binding = next(
        item for item in topology.bindings if item.source_qualified_name == "pkg.main.main"
    )
    assert binding.observed_dependency_symbol == "helper.helper"
    assert binding.dependency_symbol == "pkg.helper.helper"
    assert binding.state is BindingState.INTERNAL
    assert binding.target_qualified_name == "pkg.helper.helper"
    main = next(item for item in topology.identities if item.qualified_name == "pkg.main.main")
    assert main.state is ClosureState.CLOSED
    assert context.dependency_manifest.local_imports == ("pkg",)
    assert "helper" not in context.dependency_manifest.external_imports


def test_nested_function_inherits_relative_import_alias_binding(tmp_path: Path):
    package = _package_tree(tmp_path)
    (package / "main.py").write_text(
        "def outer():\n"
        "    from .helper import helper as h\n"
        "    def inner():\n"
        "        return h()\n"
        "    return inner()\n",
        encoding="utf-8",
    )

    identities, _legacy = scan_python_tree(tmp_path)
    context = scan_module_context(tmp_path)
    topology = derive_function_topology(
        identities,
        dependency_rewrites=context.function_dependency_rewrites,
        runtime_id="CPython-test",
    )

    inner_binding = next(
        item
        for item in topology.bindings
        if item.source_qualified_name == "pkg.main.outer.inner"
        and item.observed_dependency_symbol == "h"
    )
    assert inner_binding.dependency_symbol == "pkg.helper.helper"
    assert inner_binding.state is BindingState.INTERNAL
    assert inner_binding.target_qualified_name == "pkg.helper.helper"


def test_import_inside_function_enters_dependency_manifest(tmp_path: Path):
    (tmp_path / "main.py").write_text(
        "def main(x):\n"
        "    import numpy as np\n"
        "    return np.asarray(x)\n",
        encoding="utf-8",
    )
    context = scan_module_context(tmp_path)
    assert "numpy" in context.dependency_manifest.external_imports


def test_unresolvable_relative_import_is_explicit_debt(tmp_path: Path):
    (tmp_path / "main.py").write_text(
        "from .foo import bar\n\ndef main():\n    return bar()\n",
        encoding="utf-8",
    )
    context = scan_module_context(tmp_path)
    assert any(item.startswith("main.py:") for item in context.unresolved_relative_imports)


def test_absolute_import_does_not_create_relative_rewrite(tmp_path: Path):
    (tmp_path / "main.py").write_text(
        "import json\ndef main(x):\n    return json.loads(x)\n",
        encoding="utf-8",
    )
    context = scan_module_context(tmp_path)
    assert context.function_dependency_rewrites["main.main"] == {}
    assert "json" in context.dependency_manifest.stdlib_imports
