"""Side-effect-free validator for NOEMA private tree/blob scanner receipt v0.10."""
from __future__ import annotations

import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
RECEIPT = ROOT / "GIT_TREE_BLOB_SCANNER_RECEIPT.json"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def validate(payload: dict[str, object]) -> list[str]:
    failures: list[str] = []

    def require(condition: bool, name: str) -> None:
        if not condition:
            failures.append(name)

    require(payload.get("schema") == "noema.private-repository-tree-blob-scanner/v0.10", "schema")
    require(payload.get("status") == "CANON_SCANNER_PRIVATE_CHECKOUT_EXECUTION_NOT_RUN", "status")
    require(payload.get("predecessor_noema_commit") == "b477487ed1100c362d639bf676397e998f5ea087", "predecessor")

    phase = payload.get("phasenav", {})
    require(isinstance(phase, dict), "phasenav")
    if isinstance(phase, dict):
        require(phase.get("merge_commit") == "5a4a06eec8611dc8f890516ea457926d069e6612", "PhaseNav merge")
        require(HEX40.fullmatch(str(phase.get("merge_commit", ""))) is not None, "PhaseNav SHA format")
        require(phase.get("canon_version") == "1.5.0", "canon version")
        require(phase.get("scanner_version") == "0.10.0", "scanner version")

    parent = payload.get("parent_snapshot", {})
    require(isinstance(parent, dict), "parent snapshot")
    if isinstance(parent, dict):
        require(parent.get("private_repository_count") == 40, "repo count")
        require(parent.get("frozen_real_head_count") == 39, "head count")
        require(parent.get("archived_empty_count") == 1, "empty count")
        for key in ("inventory_sha256", "repository_vector_set_sha256"):
            require(HEX64.fullmatch(str(parent.get(key, ""))) is not None, key)

    focused = payload.get("focused_validation", {})
    require(isinstance(focused, dict), "focused")
    if isinstance(focused, dict):
        require(focused.get("status") == "PASS_13_OF_13", "focused status")
        require(all(value is True for key, value in focused.items() if key != "status"), "focused checks")

    firewall = payload.get("arbitrariness_firewall", {})
    require(isinstance(firewall, dict), "firewall")
    if isinstance(firewall, dict):
        require(all(value is False for value in firewall.values()), "arbitrariness firewall")

    execution = payload.get("execution_state", {})
    require(isinstance(execution, dict), "execution")
    if isinstance(execution, dict):
        require(execution.get("repository_head_vectors") == "COMPLETE_39_OF_39_REAL_HEADS", "repo heads")
        require(execution.get("complete_tree_blob_scan_39_checkouts") == "NOT_RUN", "tree/blob execution")
        require(execution.get("manual_path_heuristic_used") is False, "manual heuristic")

    authority = payload.get("authority_boundary", {})
    require(isinstance(authority, dict), "authority")
    if isinstance(authority, dict):
        require(authority.get("object_geometry_implies_semantic_truth") is False, "semantic truth firewall")
        require(authority.get("vectorization_implies_scientific_promotion") is False, "promotion firewall")
        require(authority.get("scientific_promotion") == "NOT_PERFORMED", "promotion state")

    return failures


def main() -> int:
    failures = validate(json.loads(RECEIPT.read_text(encoding="utf-8")))
    print(json.dumps({"status": "PASS" if not failures else "FAIL", "failures": failures}, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
