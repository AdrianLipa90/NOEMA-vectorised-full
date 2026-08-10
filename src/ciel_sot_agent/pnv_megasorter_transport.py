"""M6 cross-repository transport conformance for NOEMA <-> MegaSorter.

This layer is intentionally thin. M4/M5 remain responsible for envelope/proposal
semantics; M6 binds both sides to one machine-readable transport descriptor and
an exact fixture. Contract integrity is not epistemic or mutation authority.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from typing import Any, Mapping, Sequence

from ciel_geometry.phasenav.gate_contracts import RelationalObservation
from ciel_geometry.phasenav.pnv_precise import ENCODER_ID
from .pnv_megasorter_bridge import (
    MegaSorterEnvelope,
    MegaSorterNode,
    MegaSorterRelation,
    PROPOSALS_SCHEMA,
    SCHEMA,
    build_rag_envelope,
    proposal_batch_to_candidate_operations,
)

TRANSPORT_CONTRACT = "NOEMA_MEGASORTER_TRANSPORT_V1"
TRANSPORT_CONTRACT_SCHEMA = "NOEMA_MEGASORTER_TRANSPORT_CONTRACT_V1"
PHASE_SPACE = "pnv_precise_phase_36"
TRANSPORT_DESCRIPTOR: dict[str, Any] = {
    "contract": TRANSPORT_CONTRACT,
    "dimensions": 36,
    "envelope_schema": SCHEMA,
    "evidence_authority": "ORIGINATING_NOEMA_ENVELOPE",
    "inbound_mode": "ADVISORY_ONLY",
    "inbound_source": "MEGASORTER",
    "integrity_hash_is_authority": False,
    "mutation_allowed": False,
    "outbound_mode": "PLAN_ONLY",
    "outbound_source": "NOEMA",
    "phase_encoder": ENCODER_ID,
    "phase_space": PHASE_SPACE,
    "proposal_schema": PROPOSALS_SCHEMA,
}


def _canonical_sha256(value: Mapping[str, Any]) -> str:
    material = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(material).hexdigest()


TRANSPORT_CONTRACT_SHA256 = _canonical_sha256(TRANSPORT_DESCRIPTOR)
_EXPECTED_TRANSPORT_CONTRACT_SHA256 = "b490f9ec27879db1fd7ab83473a670a8e49190ca8bf6bc8d1595da2195654f7b"
if TRANSPORT_CONTRACT_SHA256 != _EXPECTED_TRANSPORT_CONTRACT_SHA256:
    raise RuntimeError("NOEMA MegaSorter transport descriptor drifted without version bump")


def contract_artifact() -> dict[str, Any]:
    return {
        "schema": TRANSPORT_CONTRACT_SCHEMA,
        "descriptor": dict(TRANSPORT_DESCRIPTOR),
        "descriptor_sha256": TRANSPORT_CONTRACT_SHA256,
        "authority": "NOEMA",
    }


def _require_contract_metadata(metadata: Mapping[str, Any], *, where: str) -> None:
    if metadata.get("transport_contract") != TRANSPORT_CONTRACT:
        raise ValueError(f"{where} transport contract mismatch")
    supplied = metadata.get("transport_contract_sha256")
    if supplied != TRANSPORT_CONTRACT_SHA256:
        raise ValueError(f"{where} transport contract fingerprint mismatch")


def build_transport_envelope(
    query: str,
    observations: Sequence[RelationalObservation],
) -> MegaSorterEnvelope:
    """Build the normal M5 envelope and bind it to the M6 transport contract."""

    envelope = build_rag_envelope(query, observations)
    metadata = dict(envelope.metadata)
    metadata.update(
        {
            "transport_contract": TRANSPORT_CONTRACT,
            "transport_contract_sha256": TRANSPORT_CONTRACT_SHA256,
        }
    )
    return replace(envelope, metadata=metadata)


def _require_envelope_contract(envelope: MegaSorterEnvelope) -> None:
    if envelope.schema != SCHEMA or envelope.source != "NOEMA" or envelope.mode != "PLAN_ONLY":
        raise ValueError("NOEMA transport envelope violates V1 source/schema/mode")
    _require_contract_metadata(envelope.metadata, where="NOEMA envelope")


def envelope_from_transport_dict(payload: Mapping[str, Any]) -> MegaSorterEnvelope:
    """Reconstruct a typed envelope from JSON/direct-Python transport material.

    This is a NOEMA-side round-trip helper, not a replacement for MegaSorter's
    stricter M4 ingest validation.
    """

    if not isinstance(payload, Mapping):
        raise ValueError("transport envelope must be an object")
    metadata = payload.get("metadata", {})
    if not isinstance(metadata, Mapping):
        raise ValueError("transport envelope metadata must be an object")
    _require_contract_metadata(metadata, where="NOEMA envelope")
    if payload.get("schema") != SCHEMA or payload.get("source") != "NOEMA" or payload.get("mode") != "PLAN_ONLY":
        raise ValueError("transport envelope violates V1 source/schema/mode")

    raw_nodes = payload.get("nodes")
    raw_relations = payload.get("relations", [])
    provenance = payload.get("provenance", [])
    if not isinstance(raw_nodes, (list, tuple)) or not raw_nodes:
        raise ValueError("transport envelope nodes must be a non-empty list/tuple")
    if not isinstance(raw_relations, (list, tuple)):
        raise ValueError("transport envelope relations must be a list/tuple")
    if not isinstance(provenance, (list, tuple)):
        raise ValueError("transport envelope provenance must be a list/tuple")

    nodes: list[MegaSorterNode] = []
    seen: set[str] = set()
    for index, raw in enumerate(raw_nodes):
        if not isinstance(raw, Mapping):
            raise ValueError(f"transport node {index} must be an object")
        node_id = str(raw.get("node_id") or "").strip()
        if not node_id or node_id in seen:
            raise ValueError(f"invalid/duplicate transport node id at index {index}")
        seen.add(node_id)
        if raw.get("phase_space") != PHASE_SPACE:
            raise ValueError(f"transport node {index} phase space mismatch")
        node_metadata = raw.get("metadata", {})
        if not isinstance(node_metadata, Mapping):
            raise ValueError(f"transport node {index} metadata must be an object")
        if node_metadata.get("phase_encoder") not in (None, ENCODER_ID):
            raise ValueError(f"transport node {index} encoder mismatch")
        phase = raw.get("phase36")
        if not isinstance(phase, (list, tuple)) or len(phase) != 36:
            raise ValueError(f"transport node {index} must contain 36 phases")
        node_prov = raw.get("provenance", [])
        if not isinstance(node_prov, (list, tuple)) or not node_prov:
            raise ValueError(f"transport node {index} requires provenance")
        nodes.append(
            MegaSorterNode(
                node_id=node_id,
                kind=str(raw.get("kind") or "unknown"),
                label=str(raw.get("label") or node_id),
                text=str(raw.get("text") or ""),
                phase36=tuple(float(x) for x in phase),
                phase_space=PHASE_SPACE,
                order_parameter=float(raw["order_parameter"]) if raw.get("order_parameter") is not None else None,
                provenance=tuple(str(x) for x in node_prov),
                confidence=float(raw["confidence"]) if raw.get("confidence") is not None else None,
                epistemic_state=str(raw.get("epistemic_state") or "observation"),
                metadata=dict(node_metadata),
            )
        )

    relations: list[MegaSorterRelation] = []
    for index, raw in enumerate(raw_relations):
        if not isinstance(raw, Mapping):
            raise ValueError(f"transport relation {index} must be an object")
        source = str(raw.get("source") or "")
        target = str(raw.get("target") or "")
        if source not in seen or target not in seen or source == target:
            raise ValueError(f"transport relation {index} endpoints are invalid")
        evidence = raw.get("evidence", [])
        if not isinstance(evidence, (list, tuple)) or not evidence:
            raise ValueError(f"transport relation {index} requires evidence")
        relation_metadata = raw.get("metadata", {})
        if not isinstance(relation_metadata, Mapping):
            raise ValueError(f"transport relation {index} metadata must be an object")
        relations.append(
            MegaSorterRelation(
                source=source,
                target=target,
                kind=str(raw.get("kind") or "unknown"),
                confidence=float(raw["confidence"]) if raw.get("confidence") is not None else None,
                evidence=tuple(str(x) for x in evidence),
                metadata=dict(relation_metadata),
            )
        )

    envelope = MegaSorterEnvelope(
        schema=SCHEMA,
        batch_id=str(payload.get("batch_id") or ""),
        source="NOEMA",
        mode="PLAN_ONLY",
        nodes=tuple(nodes),
        relations=tuple(relations),
        provenance=tuple(str(x) for x in provenance),
        metadata=dict(metadata),
    )
    if not envelope.batch_id:
        raise ValueError("transport envelope requires batch_id")
    return envelope


def proposal_batch_to_transport_candidates(
    payload: Mapping[str, Any],
    envelope: MegaSorterEnvelope,
):
    """Validate M6 contract fingerprint, then delegate to the M5 authority split."""

    _require_envelope_contract(envelope)
    if not isinstance(payload, Mapping):
        raise ValueError("MegaSorter proposal transport must be an object")
    metadata = payload.get("metadata", {})
    if not isinstance(metadata, Mapping):
        raise ValueError("MegaSorter proposal transport metadata must be an object")
    _require_contract_metadata(metadata, where="MegaSorter proposal batch")
    return proposal_batch_to_candidate_operations(payload, envelope)


__all__ = [
    "TRANSPORT_CONTRACT",
    "TRANSPORT_CONTRACT_SCHEMA",
    "TRANSPORT_DESCRIPTOR",
    "TRANSPORT_CONTRACT_SHA256",
    "contract_artifact",
    "build_transport_envelope",
    "envelope_from_transport_dict",
    "proposal_batch_to_transport_candidates",
]
