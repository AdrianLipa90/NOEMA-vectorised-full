from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ciel_geometry.phasenav.bundle_identity import (
    BundleIdentityState,
    derive_bundle_identities,
    derive_bundle_identity,
    group_equivalent_bundles,
)
from ciel_geometry.phasenav.entrypoint_dependency_bundle import (
    derive_entrypoint_bundles,
    parse_entrypoint_target,
)
from ciel_geometry.phasenav.function_identity import identities_from_source
from ciel_geometry.phasenav.relational_function_identity import derive_function_topology


def test_relationally_equivalent_entrypoints_share_one_bundle_identity():
    source = "def helper():\n    return 1\n\ndef main():\n    return helper()\n"
    a = identities_from_source(source, module="a", source_path="a.py")
    b = identities_from_source(source, module="b", source_path="b.py")
    identities = (*a, *b)
    topology = derive_function_topology(identities, runtime_id="CPython-test")
    declarations = (
        parse_entrypoint_target("tool-a", "a:main"),
        parse_entrypoint_target("tool-b", "b:main"),
    )
    bundles = derive_entrypoint_bundles(identities, topology, declarations)
    derived = derive_bundle_identities(bundles, topology)

    assert all(item.state is BundleIdentityState.DERIVED for item in derived)
    assert derived[0].bundle_invariant == derived[1].bundle_invariant
    assert derived[0].bundle_id == derived[1].bundle_id
    groups = group_equivalent_bundles(derived)
    assert len(groups) == 1
    assert groups[0].entrypoints == ("tool-a", "tool-b")


def test_different_helper_relation_changes_bundle_identity():
    a = identities_from_source(
        "def helper():\n    return 1\n\ndef main():\n    return helper()\n",
        module="a",
        source_path="a.py",
    )
    b = identities_from_source(
        "def helper():\n    return 2\n\ndef main():\n    return helper()\n",
        module="b",
        source_path="b.py",
    )
    identities = (*a, *b)
    topology = derive_function_topology(identities, runtime_id="CPython-test")
    bundles = derive_entrypoint_bundles(
        identities,
        topology,
        (
            parse_entrypoint_target("tool-a", "a:main"),
            parse_entrypoint_target("tool-b", "b:main"),
        ),
    )
    derived = derive_bundle_identities(bundles, topology)
    assert derived[0].state is BundleIdentityState.DERIVED
    assert derived[1].state is BundleIdentityState.DERIVED
    assert derived[0].bundle_invariant != derived[1].bundle_invariant


def test_two_names_for_same_target_share_bundle_identity():
    identities = identities_from_source(
        "def main():\n    return 1\n",
        module="app",
        source_path="app.py",
    )
    topology = derive_function_topology(identities, runtime_id="CPython-test")
    bundles = derive_entrypoint_bundles(
        identities,
        topology,
        (
            parse_entrypoint_target("alpha", "app:main"),
            parse_entrypoint_target("beta", "app:main"),
        ),
    )
    derived = derive_bundle_identities(bundles, topology)
    assert derived[0].bundle_id == derived[1].bundle_id
    assert group_equivalent_bundles(derived)[0].entrypoints == ("alpha", "beta")


def test_open_bundle_cannot_receive_bundle_identity():
    identities = identities_from_source(
        "def main(x):\n    return len(x)\n",
        module="app",
        source_path="app.py",
    )
    topology = derive_function_topology(identities, runtime_id="CPython-test")
    bundle = derive_entrypoint_bundles(
        identities,
        topology,
        (parse_entrypoint_target("app", "app:main"),),
    )[0]
    identity = derive_bundle_identity(bundle, topology)
    assert identity.state is BundleIdentityState.OPEN
    assert identity.bundle_invariant is None
    assert identity.bundle_id is None
    assert identity.blockers


def test_bundle_identity_does_not_contain_entrypoint_or_source_path():
    source = "def helper():\n    return 1\n\ndef main():\n    return helper()\n"
    left = identities_from_source(source, module="left", source_path="x/left.py")
    right = identities_from_source(source, module="right", source_path="y/right.py")
    identities = (*left, *right)
    topology = derive_function_topology(identities, runtime_id="CPython-test")
    bundles = derive_entrypoint_bundles(
        identities,
        topology,
        (
            parse_entrypoint_target("first-name", "left:main"),
            parse_entrypoint_target("second-name", "right:main"),
        ),
    )
    derived = derive_bundle_identities(bundles, topology)
    assert derived[0].bundle_invariant == derived[1].bundle_invariant
