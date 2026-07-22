#!/usr/bin/env python3
"""One-shot, receipt-gated PhaseNav binding assessment for Codex/NOEMA.

This command does not estimate orbital or HTRI science.  It verifies the
published orbital receipt and reports missing scientific provenance as
unavailable.  In particular it does not use the legacy ``ciel_binding_status``
marker, polling intervals, inferred coherence, velocity thresholds, or numeric
fallbacks as evidence of a binding.

Exit codes:

* 0 — the complete scientific binding is verified;
* 1 — an input or its receipt is invalid;
* 2 — verified inputs are structurally usable, but scientific binding evidence
  is unavailable.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import struct
import sys
from pathlib import Path
from typing import Any

from ciel_geometry.orbital_state_contract import load_verified_orbital_state
from ciel_geometry.paths import P


SCHEMA = "noema.phasenav-binding.assessment/v1"
EXIT_VERIFIED = 0
EXIT_INVALID = 1
EXIT_UNAVAILABLE = 2

NOEMA_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SOURCE = (NOEMA_ROOT / "system_map_v2.json").resolve()
EXPECTED_PRODUCER = (
    NOEMA_ROOT / "src" / "ciel_geometry" / "orbital_model.py"
).resolve()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _verify_current_artifact(
    record: Any,
    *,
    expected_path: Path,
    label: str,
) -> dict[str, Any]:
    """Verify that a receipt names the active canonical artifact and its hash."""
    if not isinstance(record, dict):
        raise ValueError(f"orbital state has no {label} provenance")
    declared_path = record.get("path")
    declared_sha256 = record.get("sha256")
    if not isinstance(declared_path, str) or not isinstance(declared_sha256, str):
        raise ValueError(f"orbital state has incomplete {label} provenance")
    resolved_path = Path(declared_path).resolve(strict=True)
    if resolved_path != expected_path:
        raise ValueError(
            f"orbital {label} is outside the active canonical path: {resolved_path}"
        )
    current_sha256 = _sha256_file(resolved_path)
    if current_sha256 != declared_sha256:
        raise ValueError(f"orbital {label} changed after state publication")
    return {
        "path": str(resolved_path),
        "sha256": current_sha256,
        "status": "verified",
    }


def _inspect_unreceipted_phase(path: Path) -> dict[str, Any]:
    """Inspect bytes without turning an unreceipted phase vector into authority."""
    try:
        resolved = path.resolve(strict=True)
        payload = resolved.read_bytes()
    except (FileNotFoundError, OSError) as exc:
        return {
            "status": "unavailable",
            "path": str(path),
            "reason": f"phase vector cannot be read: {exc}",
            "receipt": None,
        }

    if not payload:
        return {
            "status": "invalid",
            "path": str(resolved),
            "reason": "phase vector is empty",
            "receipt": None,
        }
    if len(payload) % struct.calcsize("d") != 0:
        return {
            "status": "invalid",
            "path": str(resolved),
            "byte_count": len(payload),
            "reason": "phase vector is not a complete float64 sequence",
            "receipt": None,
        }

    values = (item[0] for item in struct.iter_unpack("=d", payload))
    if not all(math.isfinite(value) for value in values):
        return {
            "status": "invalid",
            "path": str(resolved),
            "byte_count": len(payload),
            "reason": "phase vector contains a non-finite value",
            "receipt": None,
        }

    return {
        "status": "unverified",
        "path": str(resolved),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "byte_count": len(payload),
        "element_count": len(payload) // struct.calcsize("d"),
        "reason": "no content-addressed HTRI phase receipt is defined",
        "receipt": None,
    }


def assess_binding(orbital_state_path: Path, phase_path: Path) -> dict[str, Any]:
    """Return facts sufficient to prove why the binding is or is not available."""
    try:
        state, publication = load_verified_orbital_state(orbital_state_path)
        source = _verify_current_artifact(
            state.get("source"), expected_path=EXPECTED_SOURCE, label="source"
        )
        producer = _verify_current_artifact(
            state.get("producer"), expected_path=EXPECTED_PRODUCER, label="producer"
        )
    except (FileNotFoundError, OSError, json.JSONDecodeError, ValueError) as exc:
        return {
            "schema": SCHEMA,
            "status": "invalid",
            "binding_verified": False,
            "exit_code": EXIT_INVALID,
            "reason": str(exc),
            "orbital": {"status": "invalid", "path": str(orbital_state_path)},
            "htri_phase": {"status": "not_evaluated"},
        }

    topology_verified = (
        state.get("structural_status") == "ok"
        and state.get("topology_status") == "ok"
        and state.get("endpoint_resolution", {}).get("status") == "ok"
        and state.get("endpoint_resolution", {}).get("unresolved_reference_count") == 0
        and state.get("inference_used") is False
        and state.get("fallback_used") is False
    )
    weight_contract = state.get("weight_contract")
    weight_contract_verified = (
        isinstance(weight_contract, dict)
        and weight_contract.get("status") == "verified"
        and weight_contract.get("active_for_scientific_inference") is True
    )
    orbital_science_verified = (
        state.get("status") == "ok"
        and state.get("orbital_status") == "ok"
        and weight_contract_verified
    )
    phase = _inspect_unreceipted_phase(phase_path)
    binding_verified = (
        topology_verified
        and orbital_science_verified
        and phase.get("status") == "verified"
    )

    if phase.get("status") == "invalid" or not topology_verified:
        status = "invalid"
        exit_code = EXIT_INVALID
    elif binding_verified:
        status = "verified"
        exit_code = EXIT_VERIFIED
    else:
        status = "unavailable"
        exit_code = EXIT_UNAVAILABLE

    reasons: list[str] = []
    if not topology_verified:
        reasons.append("orbital topology contract is not verified")
    if not orbital_science_verified:
        reasons.append("orbital scientific state is not verified")
    if not weight_contract_verified:
        reasons.append("edge-weight contract is not verified for scientific inference")
    if phase.get("status") != "verified":
        reasons.append(str(phase.get("reason") or "HTRI phase is not verified"))

    return {
        "schema": SCHEMA,
        "status": status,
        "binding_verified": binding_verified,
        "exit_code": exit_code,
        "reasons": reasons,
        "orbital": {
            "publication": publication,
            "state_status": state.get("status"),
            "structural_status": state.get("structural_status"),
            "topology_status": state.get("topology_status"),
            "orbital_status": state.get("orbital_status"),
            "topology_verified": topology_verified,
            "scientific_verified": orbital_science_verified,
            "weight_contract_verified": weight_contract_verified,
            "inference_used": state.get("inference_used"),
            "fallback_used": state.get("fallback_used"),
            "source": source,
            "producer": producer,
            "weight_contract": weight_contract,
            "explicit_fields": state.get("explicit_fields"),
            "scientific_unavailable": state.get("scientific_unavailable"),
        },
        "htri_phase": phase,
    }


def main() -> int:
    configured_root = os.environ.get("NOEMA_ROOT")
    if configured_root and Path(configured_root).resolve() != NOEMA_ROOT:
        result = {
            "schema": SCHEMA,
            "status": "invalid",
            "binding_verified": False,
            "exit_code": EXIT_INVALID,
            "reason": f"NOEMA_ROOT does not match the executing repository: {configured_root}",
        }
    else:
        orbital_state = Path(P.MEMORY) / "state" / "noema_orbital_state.json"
        phase_path = Path(P.surface_file("phi"))
        result = assess_binding(orbital_state, phase_path)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return int(result["exit_code"])


if __name__ == "__main__":
    sys.exit(main())
