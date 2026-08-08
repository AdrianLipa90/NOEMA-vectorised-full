"""Validate the NOEMA PhaseNav/TIR/half dependency contract without side effects."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

CONTRACT = Path(__file__).with_name("dependency_contract.json")
_SHA_RE = re.compile(r"^[0-9a-f]{40}$")

EXPECTED_BLOCKED = {
    "TIR_SLOT_BINDING": "OPEN",
    "COLLATZ_STOPPING_ORIENTATION": "RETROSPECTIVE_CANDIDATE_NEEDS_PROSPECTIVE_TEST",
    "SOH_C004": "OPEN",
    "SOH_C005": "OPEN",
    "TIR_COMMON_LIKELIHOOD": "OPEN",
    "TIR_NEUTRON_EDM": "PHYSICAL_FAIL",
}


def load_contract(path: Path = CONTRACT) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_contract(contract: dict[str, object]) -> dict[str, object]:
    assert contract["schema"] == "noema.phasenav-dependency-contract/v0.7"
    assert contract["status"] == "CANON_DEPENDENCY"

    phasenav = contract["phasenav"]
    assert isinstance(phasenav, dict)
    assert phasenav["routing_dimension"] == 36
    assert phasenav["intrinsic_coefficient_dimension"] == 4
    assert phasenav["intrinsic_equals_routing"] is False
    assert _SHA_RE.fullmatch(str(phasenav["commit"]))

    anchors = contract["source_anchors"]
    assert isinstance(anchors, dict)
    for anchor in anchors.values():
        assert isinstance(anchor, dict)
        assert _SHA_RE.fullmatch(str(anchor["commit"]))

    deps = contract["dependencies"]
    assert isinstance(deps, dict)
    assert deps["ROLE_ROUTER_HABC"] == "STRUCTURAL_ROLE_ROUTING_PASS"
    assert deps["ORBIT_DIRECTION"] == "IMPLEMENTED_PROJECT_ORBITAL_RULE"
    assert (
        deps["RELATIONAL_GRADIENT"]
        == "IMPLEMENTED_SOURCE_OPERATOR_CANDIDATE_TIR_BINDING"
    )
    for node_id, status in EXPECTED_BLOCKED.items():
        assert deps[node_id] == status

    boundary = contract["authority_boundary"]
    assert isinstance(boundary, dict)
    assert boundary["scientific_evidence_generator"] is False
    assert boundary["scientific_promotion_authority"] is False
    assert boundary["direct_phasenav_engine_copy"] is False
    assert boundary["direct_cielingo_phase_memory_write"] is False
    assert boundary["memory_mutation_by_contract_reader"] is False

    firewall = contract["firewall"]
    assert isinstance(firewall, dict)
    assert firewall["mass_as_derivation_input"] == "FORBIDDEN"
    assert firewall["yukawa_as_derivation_input"] == "FORBIDDEN"
    assert firewall["coefficient_enriched_vector_as_parent"] == "FORBIDDEN"
    assert firewall["retrospective_promotion_without_prospective_test"] == "FORBIDDEN"
    assert firewall["vectorization_implies_scientific_promotion"] is False
    assert firewall["open_or_failed_to_exact_without_external_receipt"] == "FORBIDDEN"

    canonical = json.dumps(
        contract,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return {
        "schema": "noema.phasenav-dependency-contract-validation/v0.7",
        "status": "PASS",
        "contract_sha256": hashlib.sha256(canonical).hexdigest(),
        "phasenav_commit": phasenav["commit"],
        "routing_dimension": 36,
        "intrinsic_coefficient_dimension": 4,
        "blocked_statuses_preserved": sorted(EXPECTED_BLOCKED),
        "memory_mutation": "NOT_PERFORMED",
        "scientific_promotion": "NOT_PERFORMED",
    }


def main() -> None:
    print(json.dumps(validate_contract(load_contract()), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
