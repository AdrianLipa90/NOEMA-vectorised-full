from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ciel_geometry.phasenav.function_identity import identities_from_source
from ciel_geometry.phasenav.relational_function_identity import (
    BindingState,
    ClosureState,
    RelationalFunctionRelation,
    compare_relational_functions,
    derive_function_topology,
)


def _by_name(topology, name: str):
    return next(item for item in topology.identities if item.qualified_name == name)


def test_structural_alias_is_rejected_when_global_binding_differs():
    a = identities_from_source(
        "def helper():\n    return 1\n\ndef f():\n    return helper()\n",
        module="a",
        source_path="a.py",
    )
    b = identities_from_source(
        "def helper():\n    return 2\n\ndef f():\n    return helper()\n",
        module="b",
        source_path="b.py",
    )
    assert a[1].invariant_sha256 == b[1].invariant_sha256

    topology = derive_function_topology((*a, *b), runtime_id="CPython-test")
    af = _by_name(topology, "a.f")
    bf = _by_name(topology, "b.f")
    assert af.state is ClosureState.CLOSED
    assert bf.state is ClosureState.CLOSED
    assert af.relational_invariant != bf.relational_invariant
    assert compare_relational_functions(af, bf).relation is RelationalFunctionRelation.UNKNOWN


def test_true_copy_closes_to_one_relational_alias():
    source = "def helper():\n    return 1\n\ndef f():\n    return helper()\n"
    a = identities_from_source(source, module="a", source_path="a.py")
    b = identities_from_source(source, module="b", source_path="b.py")
    topology = derive_function_topology((*a, *b), runtime_id="CPython-test")
    af = _by_name(topology, "a.f")
    bf = _by_name(topology, "b.f")
    assert af.state is ClosureState.CLOSED
    assert bf.state is ClosureState.CLOSED
    assert af.relational_invariant == bf.relational_invariant
    assert compare_relational_functions(af, bf).relation is RelationalFunctionRelation.ALIAS


def test_bare_builtin_name_remains_open_without_global_binding_table():
    identities = identities_from_source(
        "def f(x):\n    return len(x)\n",
        module="m",
        source_path="m.py",
    )
    topology = derive_function_topology(identities, runtime_id="CPython-3.test")
    item = _by_name(topology, "m.f")
    assert item.state is ClosureState.OPEN
    assert item.relational_invariant is None
    binding = topology.bindings[0]
    assert binding.state is BindingState.UNRESOLVED
    assert binding.dependency_symbol == "len"


def test_explicit_stdlib_import_can_close_binding():
    identities = identities_from_source(
        "import json\ndef f(x):\n    return json.loads(x)\n",
        module="m",
        source_path="m.py",
    )
    topology = derive_function_topology(identities, runtime_id="CPython-3.test")
    item = _by_name(topology, "m.f")
    assert item.state is ClosureState.CLOSED
    assert any("stdlib:json.loads" in anchor for anchor in item.environment_anchors)


def test_versioned_external_distribution_can_close_binding():
    identities = identities_from_source(
        "import numpy as np\ndef f(x):\n    return np.asarray(x)\n",
        module="m",
        source_path="m.py",
    )
    topology = derive_function_topology(
        identities,
        external_requirements={"numpy": "numpy==2.0.0"},
        runtime_id="CPython-test",
    )
    item = _by_name(topology, "m.f")
    assert item.state is ClosureState.CLOSED
    assert any("distribution:numpy==2.0.0:numpy.asarray" in anchor for anchor in item.environment_anchors)


def test_unversioned_external_distribution_does_not_close_identity():
    identities = identities_from_source(
        "import numpy as np\ndef f(x):\n    return np.asarray(x)\n",
        module="m",
        source_path="m.py",
    )
    topology = derive_function_topology(
        identities,
        external_requirements={"numpy": "numpy"},
        runtime_id="CPython-test",
    )
    item = _by_name(topology, "m.f")
    assert item.state is ClosureState.OPEN
    assert item.relational_invariant is None


def test_dynamic_parameter_call_remains_open():
    identities = identities_from_source(
        "def f(fn):\n    return fn()\n",
        module="m",
        source_path="m.py",
    )
    topology = derive_function_topology(identities, runtime_id="CPython-test")
    item = _by_name(topology, "m.f")
    assert item.state is ClosureState.OPEN
    assert item.relational_invariant is None
    assert any("unresolved:v0" == debt for debt in item.closure_debt)


def test_recursive_component_is_explicit_open_debt():
    identities = identities_from_source(
        "def f(x):\n    return f(x - 1) if x else 0\n",
        module="m",
        source_path="m.py",
    )
    topology = derive_function_topology(identities, runtime_id="CPython-test")
    item = _by_name(topology, "m.f")
    assert item.state is ClosureState.OPEN
    assert item.relational_invariant is None
    component = next(component for component in topology.components if item.occurrence_key in component.members)
    assert component.recursive is True


def test_same_symbol_with_closed_relational_change_is_conflict():
    left = identities_from_source(
        "def f():\n    return 1\n", module="m", source_path="left.py"
    )
    right = identities_from_source(
        "def f():\n    return 2\n", module="m", source_path="right.py"
    )
    topology = derive_function_topology((*left, *right), runtime_id="CPython-test")
    lf = next(item for item in topology.identities if item.source_path == "left.py")
    rf = next(item for item in topology.identities if item.source_path == "right.py")
    assert lf.state is ClosureState.CLOSED
    assert rf.state is ClosureState.CLOSED
    assert compare_relational_functions(lf, rf).relation is RelationalFunctionRelation.CONFLICT
