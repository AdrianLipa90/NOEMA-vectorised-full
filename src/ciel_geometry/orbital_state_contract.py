"""Verified read contract for the published NOEMA orbital topology state."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


STATE_SCHEMA = "noema.orbital.topology-state/v1"
RECEIPT_SCHEMA = "noema.orbital.topology-state-receipt/v1"


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_verified_orbital_state(path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    """Load a strict state only after verifying its content-addressed receipt."""
    state_path = path.resolve(strict=True)
    state_bytes = state_path.read_bytes()
    state_sha256 = _sha256(state_bytes)
    state = json.loads(state_bytes.decode("utf-8"))
    if not isinstance(state, dict) or state.get("schema") != STATE_SCHEMA:
        raise ValueError("unsupported or missing orbital state schema")
    if state.get("inference_used") is not False:
        raise ValueError("orbital state contains inferred values")
    if state.get("fallback_used") is not False:
        raise ValueError("orbital state contains fallback values")

    source = state.get("source")
    producer = state.get("producer")
    output = state.get("output")
    if not isinstance(source, dict) or not isinstance(producer, dict):
        raise ValueError("orbital state lacks source or producer provenance")
    if not isinstance(output, dict):
        raise ValueError("orbital state lacks output provenance")
    source_path = Path(str(source.get("path"))).resolve(strict=True)
    producer_path = Path(str(producer.get("path"))).resolve(strict=True)
    if _sha256(source_path.read_bytes()) != source.get("sha256"):
        raise ValueError("orbital source hash no longer matches the publication")
    if _sha256(producer_path.read_bytes()) != producer.get("sha256"):
        raise ValueError("orbital producer hash no longer matches the publication")
    if Path(str(output.get("path"))).resolve() != state_path:
        raise ValueError("orbital state output path mismatch")

    receipt_path = (
        state_path.parent
        / "receipts"
        / state_path.stem
        / f"{state_sha256}.json"
    )
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if not isinstance(receipt, dict) or receipt.get("schema") != RECEIPT_SCHEMA:
        raise ValueError("unsupported or missing orbital receipt schema")
    checks = {
        "output_sha256": receipt.get("output_sha256") == state_sha256,
        "output_path": Path(str(receipt.get("output_path"))).resolve()
        == state_path,
        "source_sha256": receipt.get("source_sha256")
        == state.get("source", {}).get("sha256"),
        "source_path": Path(str(receipt.get("source_path"))).resolve()
        == source_path,
        "producer_sha256": receipt.get("producer_sha256")
        == state.get("producer", {}).get("sha256"),
        "producer_path": Path(str(receipt.get("producer_path"))).resolve()
        == producer_path,
        "read_back_verified": receipt.get("read_back_verified") is True,
        "inference_used": receipt.get("inference_used") is False,
        "fallback_used": receipt.get("fallback_used") is False,
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise ValueError(f"orbital receipt verification failed: {', '.join(failed)}")

    publication = {
        "status": "verified",
        "state_path": str(state_path),
        "state_sha256": state_sha256,
        "receipt_path": str(receipt_path),
        "receipt_checks": checks,
    }
    return state, publication


def summarize_verified_orbital_state(path: Path) -> dict[str, Any]:
    """Return the shared compact projection used by portal and CIEL Hub."""
    state, publication = load_verified_orbital_state(path)
    primaries = state.get("primaries")
    all_systems = state.get("all_systems")
    result: dict[str, Any] = {
        "schema": state.get("schema"),
        "status": state.get("status"),
        "structural_status": state.get("structural_status"),
        "topology_status": state.get("topology_status"),
        "orbital_status": state.get("orbital_status"),
        "inference_used": state.get("inference_used"),
        "fallback_used": state.get("fallback_used"),
        "systems": state.get("systems"),
        "nodes": state.get("nodes"),
        "edges": state.get("edges"),
        "orbits": state.get("orbits"),
        "coherence": state.get("coherence"),
        "primaries": len(primaries) if isinstance(primaries, list) else None,
        "binaries": state.get("binaries"),
        "multi_orbit_3plus": state.get("multi_orbit_3plus"),
        "top_phases": state.get("top_phases"),
        "view_ascii": state.get("view_ascii"),
        "updated_at": state.get("generated_at"),
        "source": state.get("source"),
        "producer": state.get("producer"),
        "weight_contract": state.get("weight_contract"),
        "endpoint_resolution": state.get("endpoint_resolution"),
        "explicit_fields": state.get("explicit_fields"),
        "validation_errors": state.get("validation_errors"),
        "scientific_unavailable": state.get("scientific_unavailable"),
        "metrics": state.get("metrics"),
        "publication": publication,
    }
    if isinstance(all_systems, list):
        for system in all_systems:
            if isinstance(system, dict) and system.get("id") == "agent":
                result["agent"] = system
                break
    return result
