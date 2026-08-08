"""Side-effect-free validator for NOEMA private-repository vector receipt v0.9."""
from __future__ import annotations

import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
RECEIPT = ROOT / "PRIVATE_REPOSITORY_VECTOR_RECEIPT.json"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def validate(payload: dict[str, object]) -> list[str]:
    failures: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    require(payload.get("schema") == "noema.private-repository-vectorization/v0.9", "schema")
    require(payload.get("status") == "CANON_CONTENT_IDENTITY_ROUTING", "status")
    require(payload.get("predecessor_noema_commit") == "205ea2937dce04124753feb46f91266d228564d9", "NOEMA predecessor")

    phase = payload.get("phasenav", {})
    require(isinstance(phase, dict), "phasenav object")
    if isinstance(phase, dict):
        merge = str(phase.get("merge_commit", ""))
        require(HEX40.fullmatch(merge) is not None, "PhaseNav merge SHA format")
        require(merge == "2cf1e433e21f4f3feab2f248218a38f5263e66ea", "PhaseNav merge pin")
        require(phase.get("canon_version") == "1.4.0", "canon version")
        require(phase.get("git_object_vectorization_version") == "0.9.0", "vectorization version")
        require(phase.get("validation") == "PASS_FOCUSED_FULL_CI_INFRA_BLOCKED", "validation boundary")

    inventory = payload.get("inventory", {})
    require(isinstance(inventory, dict), "inventory object")
    if isinstance(inventory, dict):
        require(inventory.get("repository_count") == 40, "repository count")
        require(inventory.get("head_present_count") == 39, "head count")
        require(inventory.get("archived_empty_count") == 1, "archived empty count")
        require(inventory.get("inventory_sha256") == "d47ace603e52fdb3fbe77556b370ac272d4ac5f3d0232b0bda4fbc998a05ab70", "inventory digest")
        require(inventory.get("vector_set_sha256") == "a7e458063b3fb94d817f132c3c4dceee5a6ed7ade32237bec4acaff392640e0b", "vector-set digest")
        require(HEX64.fullmatch(str(inventory.get("inventory_sha256", ""))) is not None, "inventory SHA format")
        require(HEX64.fullmatch(str(inventory.get("vector_set_sha256", ""))) is not None, "vector-set SHA format")

    parentage = payload.get("vector_parentage", {})
    require(isinstance(parentage, dict), "vector parentage object")
    if isinstance(parentage, dict):
        require(parentage.get("repository_state") == "native Git commit digest only", "repo parent")
        require(parentage.get("file_state") == "native Git blob digest only", "blob parent")
        require(parentage.get("directory_state") == "native Git tree digest only", "tree parent")
        require(parentage.get("routing_dimension") == 36, "routing dimension")

    firewall = payload.get("arbitrariness_firewall", {})
    require(isinstance(firewall, dict), "firewall object")
    if isinstance(firewall, dict):
        for key in (
            "repository_name_vector_parent",
            "repository_id_vector_parent",
            "default_branch_vector_parent",
            "repository_size_vector_parent",
            "path_label_vector_parent",
            "manual_importance_weight",
            "manual_numeric_id",
            "collatz_string_hash_for_git_content",
            "invented_edge_vector",
            "invented_empty_repository_vector",
        ):
            require(firewall.get(key) is False, key)

    edge = payload.get("edge_policy", {})
    require(isinstance(edge, dict), "edge policy object")
    if isinstance(edge, dict):
        require(edge.get("edge_vector_from_label") is False, "edge label vector")
        require(edge.get("edge_geometry_proves_semantics") is False, "edge semantic promotion")

    history = payload.get("historical_provenance", {})
    require(isinstance(history, dict), "history object")
    if isinstance(history, dict):
        require(history.get("v0_8_receipts_rewritten") is False, "history immutability")
        require(history.get("append_only") is True, "append-only")

    authority = payload.get("authority_boundary", {})
    require(isinstance(authority, dict), "authority boundary")
    if isinstance(authority, dict):
        require(authority.get("vectorization_implies_scientific_promotion") is False, "scientific firewall")
        require(authority.get("repository_geometry_implies_semantic_equivalence") is False, "semantic equivalence firewall")
        require(authority.get("repository_geometry_implies_scientific_correctness") is False, "scientific correctness firewall")
        require(authority.get("scientific_promotion") == "NOT_PERFORMED", "promotion status")

    return failures


def main() -> int:
    payload = json.loads(RECEIPT.read_text(encoding="utf-8"))
    failures = validate(payload)
    print(json.dumps({"status": "PASS" if not failures else "FAIL", "failures": failures}, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
