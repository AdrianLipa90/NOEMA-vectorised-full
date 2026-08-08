"""Side-effect-free validator for the append-only PhaseNav/TIR/half closure receipt."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
RECEIPT = ROOT / "FINAL_CLOSURE_RECEIPT.json"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def canonical_receipt_sha256(payload: dict[str, object]) -> str:
    body = dict(payload)
    body.pop("receipt_sha256", None)
    encoded = json.dumps(
        body, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate(payload: dict[str, object]) -> list[str]:
    failures: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    require(payload.get("schema") == "noema.phasenav-tir-half-closure/v0.8", "schema")
    require(payload.get("status") == "CANON_CROSSREPO_CLOSURE", "status")

    state = payload.get("canonical_state", {})
    require(isinstance(state, dict), "canonical_state object")
    if isinstance(state, dict):
        phase = state.get("phasenav", {})
        tir = state.get("tir", {})
        half = state.get("secret_of_a_half", {})
        require(isinstance(phase, dict), "phasenav object")
        require(isinstance(tir, dict), "tir object")
        require(isinstance(half, dict), "half object")
        if isinstance(phase, dict):
            require(HEX40.fullmatch(str(phase.get("runtime_parent_commit", ""))) is not None, "PhaseNav runtime SHA")
            require(HEX40.fullmatch(str(phase.get("closure_merge_commit", ""))) is not None, "PhaseNav closure SHA")
            require(phase.get("closure_merge_commit") == "b3f31a0cad78f6c7c9e908434b98d5e3132b2a0a", "PhaseNav closure commit pin")
            require(phase.get("canon_version") == "1.3.0", "PhaseNav canon version")
            require(phase.get("closure_version") == "0.8.0", "closure version")
            require(phase.get("routing_dimension") == 36, "routing dimension")
        if isinstance(tir, dict):
            require(tir.get("merge_commit") == "df8a6e1321ecf2e2c8819f4e9d5ec7d4f997d170", "TIR merge pin")
            require(tir.get("validation") == "FULL_PUBLICATION_CI_PASS", "TIR validation")
        if isinstance(half, dict):
            require(half.get("merge_commit") == "a1b0aeba192766163893fab1468b8f9cd9b8853b", "half merge pin")
            require(half.get("validation") == "DHSE_AND_FULL_BUILD_CI_PASS", "half validation")
            require(half.get("monograph_pages") == 111, "half monograph page count")

    closure = payload.get("closure", {})
    require(isinstance(closure, dict), "closure object")
    if isinstance(closure, dict):
        require(closure.get("source_state_sha256") == "d0c624dffcbc889309ebab418d48e16d9c172cf902590f90883b8e34c88c4638", "source-state digest")
        require(closure.get("closure_sha256") == "1619fa17f609baf1fc4db12dac7b3a166b26b44c84f9ffb80fc7533fb3767361", "closure digest")
        require(HEX64.fullmatch(str(closure.get("source_state_sha256", ""))) is not None, "source-state SHA format")
        require(HEX64.fullmatch(str(closure.get("closure_sha256", ""))) is not None, "closure SHA format")
        counts = closure.get("vector_counts", {})
        require(isinstance(counts, dict), "vector counts object")
        if isinstance(counts, dict):
            require(counts.get("source_anchors") == 4, "source vector count")
            require(counts.get("dependency_nodes") == 11, "node vector count")
            require(counts.get("dependency_paths") == 7, "path vector count")
            require(counts.get("total") == 22, "total vector count")
            require(counts.get("unique_sha256") == 22, "unique vector hashes")
        source_hashes = closure.get("source_vector_sha256", {})
        require(isinstance(source_hashes, dict) and len(source_hashes) == 4, "source vector hashes")
        if isinstance(source_hashes, dict):
            require(all(HEX64.fullmatch(str(value)) is not None for value in source_hashes.values()), "source vector SHA format")
            require(len(set(source_hashes.values())) == 4, "source vectors unique")

    epistemic = payload.get("epistemic_state", {})
    require(isinstance(epistemic, dict), "epistemic state object")
    if isinstance(epistemic, dict):
        require(epistemic.get("KAPPA") == "PROJECT_DERIVED_EXACT_ALGEBRA", "KAPPA status")
        require(epistemic.get("TIR_SLOT_BINDING") == "OPEN", "TIR slot binding")
        require(epistemic.get("SOH_C004") == "OPEN", "SOH_C004")
        require(epistemic.get("SOH_C005") == "OPEN", "SOH_C005")
        require(epistemic.get("TIR_NEUTRON_EDM") == "PHYSICAL_FAIL", "neutron EDM")

    boundary = payload.get("authority_boundary", {})
    require(isinstance(boundary, dict), "authority boundary object")
    if isinstance(boundary, dict):
        require(boundary.get("scientific_promotion_authority") is False, "scientific promotion authority")
        require(boundary.get("scientific_evidence_generator") is False, "scientific evidence generator")
        require(boundary.get("direct_phasenav_engine_copy") is False, "PhaseNav engine copy")
        require(boundary.get("vectorization_implies_scientific_promotion") is False, "vectorization firewall")
        require(boundary.get("path_vector_implies_edge_truth") is False, "path firewall")
        require(boundary.get("memory_mutation_by_validator") is False, "validator mutation")

    writeback = payload.get("writeback", {})
    require(isinstance(writeback, dict), "writeback object")
    if isinstance(writeback, dict):
        require(writeback.get("mode") == "APPEND_ONLY", "append-only writeback")
        require(writeback.get("supersedes_history") is False, "history preservation")

    expected = payload.get("receipt_sha256")
    actual = canonical_receipt_sha256(payload)
    require(expected == actual, f"receipt SHA mismatch: expected={expected} actual={actual}")
    return failures


def main() -> int:
    payload = json.loads(RECEIPT.read_text(encoding="utf-8"))
    failures = validate(payload)
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    print("PASS: NOEMA PhaseNav/TIR/half closure v0.8")
    print(payload["receipt_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
