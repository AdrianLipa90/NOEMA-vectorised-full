from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ciel_geometry.phasenav.function_identity import identities_from_source
from ciel_geometry.phasenav.gate_contracts import PhaseSpace
from ciel_sot_agent.function_identity_bridge import function_identity_state


def test_aliases_share_relational_identity_without_fabricated_phase():
    left = identities_from_source("def f(x):\n    return x + 1\n", module="a", source_path="a.py")[0]
    right = identities_from_source("def g(value):\n    return value + 1\n", module="b", source_path="b.py")[0]

    left_state = function_identity_state(left)
    right_state = function_identity_state(right)

    assert left_state.identity == right_state.identity
    assert left_state.phase36 is None
    assert left_state.phase_space is PhaseSpace.UNKNOWN
    assert right_state.phase36 is None
    assert right_state.phase_space is PhaseSpace.UNKNOWN
    assert left_state.authority_state == "DERIVED_STATIC_NO_AUTHORITY"
    assert left_state.metadata["phase_projection"] == "UNKNOWN_UNTIL_DERIVED"


def test_dependencies_become_explicit_relations():
    identity = identities_from_source(
        "import numpy as np\ndef f(x):\n    return np.asarray(x)\n",
        module="m",
        source_path="m.py",
    )[0]
    state = function_identity_state(identity)
    assert state.relations == ("depends_on:numpy.asarray",)
    assert state.provenance == ("source:m.py",)
