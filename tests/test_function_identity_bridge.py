from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ciel_geometry.phasenav.function_identity import identities_from_source
from ciel_geometry.phasenav.gate_contracts import PhaseSpace
from ciel_geometry.phasenav.relational_function_identity import derive_function_topology
from ciel_sot_agent.function_identity_bridge import (
    function_identity_state,
    relational_function_identity_state,
)


def test_structural_bridge_does_not_claim_relational_closure():
    identity = identities_from_source(
        "def f(x):\n    return x + 1\n", module="a", source_path="a.py"
    )[0]
    state = function_identity_state(identity)
    assert state.identity.startswith("function-structural:")
    assert state.phase36 is None
    assert state.phase_space is PhaseSpace.UNKNOWN
    assert state.authority_state == "DERIVED_STRUCTURAL_NO_AUTHORITY"
    assert state.metadata["identity_scope"] == "STRUCTURAL_ONLY_NOT_RELATIONALLY_CLOSED"
    assert state.metadata["phase_projection"] == "UNKNOWN_UNTIL_DERIVED"


def test_structural_dependencies_are_symbol_relations_only():
    identity = identities_from_source(
        "import numpy as np\ndef f(x):\n    return np.asarray(x)\n",
        module="m",
        source_path="m.py",
    )[0]
    state = function_identity_state(identity)
    assert state.relations == ("depends_on-symbol:numpy.asarray",)
    assert state.provenance == ("source:m.py",)


def test_closed_relational_aliases_share_noema_identity_without_phase_fabrication():
    source = "def helper():\n    return 1\n\ndef f():\n    return helper()\n"
    left = identities_from_source(source, module="a", source_path="a.py")
    right = identities_from_source(source, module="b", source_path="b.py")
    topology = derive_function_topology((*left, *right), runtime_id="CPython-test")
    af = next(item for item in topology.identities if item.qualified_name == "a.f")
    bf = next(item for item in topology.identities if item.qualified_name == "b.f")

    left_state = relational_function_identity_state(af)
    right_state = relational_function_identity_state(bf)
    assert left_state.identity == right_state.identity
    assert left_state.identity.startswith("function-relational:")
    assert left_state.phase36 is None
    assert left_state.phase_space is PhaseSpace.UNKNOWN
    assert left_state.authority_state == "DERIVED_RELATIONAL_NO_AUTHORITY"


def test_open_relational_identity_stays_occurrence_specific():
    identities = identities_from_source(
        "def f(fn):\n    return fn()\n", module="m", source_path="m.py"
    )
    topology = derive_function_topology(identities, runtime_id="CPython-test")
    item = topology.identities[0]
    state = relational_function_identity_state(item)
    assert state.identity == item.occurrence_key
    assert state.authority_state == "OPEN_RELATIONAL_DEBT_NO_AUTHORITY"
    assert any(relation.startswith("closure-debt:") for relation in state.relations)
