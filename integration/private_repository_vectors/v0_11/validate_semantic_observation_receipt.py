"""Validate the append-only private Git semantic-observation receipt v0.11."""
from __future__ import annotations

import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
RECEIPT = ROOT / "GIT_SEMANTIC_OBSERVATION_RECEIPT.json"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def validate(payload: dict[str, object]) -> list[str]:
    failures: list[str] = []

    def require(condition: bool, name: str) -> None:
        if not condition:
            failures.append(name)

    require(payload.get("schema") == "noema.private-repository-semantic-observation/v0.11", "schema")
    require(payload.get("status") == "CANON_BINDING_CONTRACT_PRIVATE_SEMANTIC_EXECUTION_NOT_RUN", "status")
    require(payload.get("predecessor_noema_commit") == "f25bd87192db6b364fed526670becbe2a0c21827", "predecessor")

    phase = payload.get("phasenav", {})
    require(isinstance(phase, dict), "phasenav")
    if isinstance(phase, dict):
        merge = str(phase.get("merge_commit", ""))
        require(HEX40.fullmatch(merge) is not None, "PhaseNav merge SHA format")
        require(merge == "6f55d48983b1bc3d2e786a68c5b7c33cedf7f543", "PhaseNav merge pin")
        require(phase.get("canon_version") == "1.6.0", "canon version")
        require(phase.get("semantic_observation_version") == "0.11.0", "binding version")

    identity = payload.get("identity_state", {})
    require(isinstance(identity, dict), "identity state")
    if isinstance(identity, dict):
        require(identity.get("private_repository_inventory") == "COMPLETE_40", "inventory count")
        require(identity.get("real_head_identity_vectors") == "COMPLETE_39_OF_39", "head vectors")
        require(identity.get("archived_empty_without_invented_vector") == 1, "empty source")
        require(HEX64.fullmatch(str(identity.get("inventory_sha256", ""))) is not None, "inventory SHA")
        require(HEX64.fullmatch(str(identity.get("repository_vector_set_sha256", ""))) is not None, "vector set SHA")
        require(identity.get("complete_tree_blob_execution") == "NOT_RUN", "tree/blob boundary")

    semantic = payload.get("semantic_runtime", {})
    require(isinstance(semantic, dict), "semantic runtime")
    if isinstance(semantic, dict):
        require(semantic.get("runtime_code_commit") == "0a4a1b57217fc876ed0535829686cfed8ccd0d8f", "semantic runtime pin")
        require(semantic.get("cielingo_runtime_commit") == "ab097f99d46eb446836833ac90b2bc3cf9d219e1", "CIELingo runtime pin")
        require(semantic.get("phase_dimension") == 36, "phase dimension")
        require(semantic.get("phase_convention") == "native_spinor_4pi", "phase convention")
        require(semantic.get("memory_lane_count") == 12, "memory lane count")

    binding = payload.get("binding_rule", {})
    require(isinstance(binding, dict), "binding rule")
    if isinstance(binding, dict):
        require(binding.get("same_blob_can_have_multiple_contextual_observations") is True, "context multiplicity")
        require(binding.get("identity_vector_changes_with_semantic_context") is False, "identity context independence")
        require(binding.get("semantic_observation_receipt_changes_with_context") is True, "context receipt")
        require(binding.get("intrinsic_file_semantic_vector") == "NOT_DEFINED_BY_THIS_LAYER", "no semantic collapse")

    firewall = payload.get("arbitrariness_firewall", {})
    require(isinstance(firewall, dict), "firewall")
    if isinstance(firewall, dict):
        require(all(value is False for value in firewall.values()), "semantic firewall")

    execution = payload.get("execution_state", {})
    require(isinstance(execution, dict), "execution")
    if isinstance(execution, dict):
        require(execution.get("complete_private_tree_blob_scan") == "NOT_RUN", "tree/blob execution")
        require(execution.get("private_blob_semantic_observations") == "NOT_RUN", "semantic execution")
        require(execution.get("heuristic_semantic_substitution_used") is False, "heuristic substitution")

    authority = payload.get("authority_boundary", {})
    require(isinstance(authority, dict), "authority")
    if isinstance(authority, dict):
        require(authority.get("semantic_observation_implies_scientific_truth") is False, "truth firewall")
        require(authority.get("semantic_observation_implies_source_promotion") is False, "SOURCE firewall")
        require(authority.get("semantic_observation_implies_canon_promotion") is False, "canon firewall")
        require(authority.get("scientific_promotion") == "NOT_PERFORMED", "promotion state")

    return failures


def main() -> int:
    failures = validate(json.loads(RECEIPT.read_text(encoding="utf-8")))
    print(json.dumps({"status": "PASS" if not failures else "FAIL", "failures": failures}, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
