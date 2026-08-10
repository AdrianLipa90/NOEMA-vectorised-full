from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ciel_geometry.phasenav.function_identity import (
    FunctionRelation,
    compare_functions,
    derive_dependency_manifest,
    identities_from_source,
)


def _one(source: str, module: str = "m"):
    items = identities_from_source(source, module=module)
    assert len(items) == 1
    return items[0]


def test_alpha_renaming_does_not_change_identity():
    left = _one("def f(x):\n    y = x + 1\n    return y\n", module="a")
    right = _one("def g(value):\n    result = value + 1\n    return result\n", module="b")
    assert left.invariant_sha256 == right.invariant_sha256
    assert compare_functions(left, right).relation is FunctionRelation.ALIAS


def test_constant_change_is_not_silently_treated_as_alias():
    left = _one("def f(x):\n    return x + 1\n", module="a")
    right = _one("def g(x):\n    return x + 2\n", module="b")
    assert left.invariant_sha256 != right.invariant_sha256
    assert compare_functions(left, right).relation is FunctionRelation.UNKNOWN


def test_same_symbol_with_changed_invariant_is_conflict():
    left = _one("def f(x):\n    return x + 1\n")
    right = _one("def f(x):\n    return x + 2\n")
    assert compare_functions(left, right).relation is FunctionRelation.CONFLICT


def test_same_symbol_and_invariant_is_same_identity():
    left = _one("def f(x):\n    return x + 1\n")
    right = _one("def f(value):\n    return value + 1\n")
    assert compare_functions(left, right).relation is FunctionRelation.SAME_IDENTITY


def test_import_alias_spelling_is_not_identity_bearing():
    left = _one("import numpy as np\ndef f(x):\n    return np.asarray(x)\n", module="a")
    right = _one("import numpy as numpy_alias\ndef g(x):\n    return numpy_alias.asarray(x)\n", module="b")
    assert left.dependency_symbols == ("numpy.asarray",)
    assert right.dependency_symbols == ("numpy.asarray",)
    assert compare_functions(left, right).relation is FunctionRelation.ALIAS


def test_local_import_does_not_leak_into_other_function_scope():
    source = """
def first(x):
    import numpy as n
    return n.asarray(x)

def second(n):
    return n.asarray()
"""
    first, second = identities_from_source(source, module="m")
    assert first.dependency_symbols == ("numpy.asarray",)
    assert second.dependency_symbols == ("v0.asarray",)


def test_nested_helper_name_is_normalized_in_outer_scope():
    left_items = identities_from_source(
        "def f(x):\n"
        "    def inner():\n"
        "        hidden = 7\n"
        "        return hidden\n"
        "    return x + 1\n",
        module="a",
    )
    right_items = identities_from_source(
        "def g(value):\n"
        "    def nested():\n"
        "        hidden = 7\n"
        "        return hidden\n"
        "    return value + 1\n",
        module="b",
    )
    assert len(left_items) == 2
    assert len(right_items) == 2
    assert left_items[0].invariant_sha256 == right_items[0].invariant_sha256
    assert compare_functions(left_items[0], right_items[0]).relation is FunctionRelation.ALIAS


def test_nested_scope_internals_are_conservative():
    left = identities_from_source(
        "def f(x):\n"
        "    def inner():\n"
        "        hidden = 7\n"
        "        return hidden\n"
        "    return x + 1\n",
        module="a",
    )[0]
    right = identities_from_source(
        "def g(value):\n"
        "    def nested():\n"
        "        other = 7\n"
        "        return other\n"
        "    return value + 1\n",
        module="b",
    )[0]
    assert compare_functions(left, right).relation is FunctionRelation.UNKNOWN


def test_defaults_remain_identity_bearing():
    left = _one("def f(x=1):\n    return x\n", module="a")
    right = _one("def g(x=2):\n    return x\n", module="b")
    assert compare_functions(left, right).relation is FunctionRelation.UNKNOWN


def test_default_expressions_remain_in_outer_scope():
    left = _one("def f(x=x):\n    return x\n", module="a")
    right = _one("def g(y=y):\n    return y\n", module="b")
    assert compare_functions(left, right).relation is FunctionRelation.UNKNOWN


def test_dependency_manifest_is_derived_without_scores_or_thresholds():
    manifest = derive_dependency_manifest(
        {"json", "pathlib", "numpy", "ciel_geometry"},
        local_roots={"ciel_geometry"},
    )
    assert "json" in manifest.stdlib_imports
    assert "pathlib" in manifest.stdlib_imports
    assert manifest.local_imports == ("ciel_geometry",)
    assert manifest.external_imports == ("numpy",)
