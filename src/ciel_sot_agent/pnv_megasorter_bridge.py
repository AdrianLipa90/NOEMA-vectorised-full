"""Versioned PLAN_ONLY bridge between NOEMA observations and MegaSorter.

The bridge intentionally does not import `orbitalsort` classes. NOEMA remains
its own authority plane and emits a substrate-neutral envelope that an
installed/remote MegaSorter adapter may consume.

Invariant: co-retrieval does not create result-to-result semantic edges. The
only automatic relation in a RAG batch is the evidenced `retrieved_for`
relation between a retrieved observation and its query node.

Inbound proposals do not bring their own authority. Evidence is recovered from
the original NOEMA envelope. If no corresponding relation is present, the
resulting PhaseOperation has no evidence and the Gate Fabric must HOLD it.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from typing import Any, Mapping, Sequence

from ciel_geometry.phasenav.gate_contracts import (
    EpistemicState,
    PhaseOperation,
    PhaseSpace,
    RelationalObservation,
    RelationalState,
)
from ciel_geometry.phasenav.pnv_precise import ENCODER_ID, order_parameter, sentence_phase_precise

SCHEMA = "NOEMA_MEGASORTER_ENVELOPE_V1"
PROPOSALS_SCHEMA = "NOEMA_MEGASORTER_PROPOSALS_V1"


@dataclass(frozen=True)
class MegaSorterNode:
    node_id: str
    kind: str
    label: str
    text: str
    phase36: tuple[float, ...] | None
    phase_space: str
    order_parameter: float | None
    provenance: tuple[str, ...]
    confidence: float | None = None
    epistemic_state: str = "observation"
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class MegaSorterRelation:
    source: str
    target: str
    kind: str
    confidence: float | None
    evidence: tuple[str, ...]
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class MegaSorterEnvelope:
    schema: str
    batch_id: str
    source: str
    mode: str
    nodes: tuple[MegaSorterNode, ...]
    relations: tuple[MegaSorterRelation, ...]
    provenance: tuple[str, ...]
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _stable_id(prefix: str, value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, default=str, separators=(",", ":")).encode("utf-8")
    return f"{prefix}:{hashlib.sha256(encoded).hexdigest()[:24]}"


def _observation_text(observation: RelationalObservation) -> str:
    payload = observation.payload
    essence = str(payload.get("essence") or "")
    filename = str(payload.get("filename") or "")
    return essence or filename or observation.observation_id


def _node_map(envelope: MegaSorterEnvelope) -> dict[str, MegaSorterNode]:
    return {node.node_id: node for node in envelope.nodes}


def _phase_space(value: str) -> PhaseSpace:
    try:
        return PhaseSpace(value)
    except ValueError:
        return PhaseSpace.UNKNOWN


def build_rag_envelope(query: str, observations: Sequence[RelationalObservation]) -> MegaSorterEnvelope:
    """Build a relation-preserving MegaSorter batch for one RAG query."""

    query_text = str(query).strip()
    if not query_text:
        raise ValueError("query must not be empty")

    query_phase = sentence_phase_precise(query_text)
    query_id = _stable_id("query", query_text)
    query_provenance = ("user-query:runtime", "ciel_geometry.phasenav.pnv_precise:sentence_phase_precise")

    nodes: list[MegaSorterNode] = [
        MegaSorterNode(
            node_id=query_id,
            kind="query",
            label=query_text[:120],
            text=query_text,
            phase36=query_phase,
            phase_space=PhaseSpace.PNV_PRECISE_PHASE_36.value,
            order_parameter=order_parameter(query_phase),
            provenance=query_provenance,
            confidence=1.0,
            epistemic_state="observation",
            metadata={"phase_encoder": ENCODER_ID},
        )
    ]
    relations: list[MegaSorterRelation] = []
    batch_provenance: list[str] = [*query_provenance]

    for observation in observations:
        if observation.phase36 is not None and observation.phase_space is not PhaseSpace.PNV_PRECISE_PHASE_36:
            # Do not silently project another 36D coordinate system. Text can
            # be re-encoded canonically while the original space remains audit metadata.
            phase36 = sentence_phase_precise(_observation_text(observation))
            phase_source = "REENCODED_FROM_TEXT"
        elif observation.phase36 is not None:
            phase36 = observation.phase36
            phase_source = "OBSERVATION_NATIVE"
        else:
            phase36 = sentence_phase_precise(_observation_text(observation))
            phase_source = "ENCODED_FROM_TEXT"

        payload = observation.payload
        label = str(payload.get("filename") or payload.get("topic") or observation.observation_id)
        confidence = observation.confidence
        nodes.append(
            MegaSorterNode(
                node_id=observation.observation_id,
                kind="retrieved_observation",
                label=label[:160],
                text=_observation_text(observation),
                phase36=phase36,
                phase_space=PhaseSpace.PNV_PRECISE_PHASE_36.value,
                order_parameter=order_parameter(phase36),
                provenance=observation.provenance,
                confidence=confidence,
                epistemic_state="observation",
                metadata={
                    "source": observation.source,
                    "observation_class": observation.observation_class.value,
                    "input_phase_space": observation.phase_space.value,
                    "phase_source": phase_source,
                    "phase_encoder": ENCODER_ID,
                },
            )
        )
        relations.append(
            MegaSorterRelation(
                source=observation.observation_id,
                target=query_id,
                kind="retrieved_for",
                confidence=confidence,
                evidence=observation.provenance,
                metadata={"evidence_class": "retrieval"},
            )
        )
        batch_provenance.extend(observation.provenance)

    unique_provenance = tuple(dict.fromkeys(batch_provenance))
    batch_id = _stable_id(
        "megasorter:rag",
        {"query": query_text, "nodes": [node.node_id for node in nodes], "schema": SCHEMA},
    )
    return MegaSorterEnvelope(
        schema=SCHEMA,
        batch_id=batch_id,
        source="NOEMA",
        mode="PLAN_ONLY",
        nodes=tuple(nodes),
        relations=tuple(relations),
        provenance=unique_provenance,
        metadata={
            "phase_encoder": ENCODER_ID,
            "authority": "NOEMA",
            "consumer_role": "MEGASORTER_PLANNER",
            "no_result_result_edges_without_evidence": True,
        },
    )


def node_to_relational_state(node: MegaSorterNode) -> RelationalState:
    """Recover a typed NOEMA state from an envelope node without mutation."""

    space = _phase_space(node.phase_space)
    return RelationalState(
        identity=node.node_id,
        kind=node.kind,
        phase36=node.phase36,
        phase_space=space,
        order_parameter=node.order_parameter,
        provenance=node.provenance,
        epistemic_state=EpistemicState.CANDIDATE,
        authority_state="OBSERVED_ONLY",
        lifecycle="CANDIDATE",
        metadata={**dict(node.metadata), "label": node.label, "text": node.text},
    )


def _proposal_endpoint(proposal: Mapping[str, Any], prefix: str) -> str | None:
    for key in (f"{prefix}_card_id", f"{prefix}_id", prefix):
        value = proposal.get(key)
        if value:
            return str(value)
    return None


def _relation_evidence(
    envelope: MegaSorterEnvelope,
    source_id: str,
    target_id: str | None,
) -> tuple[str, ...]:
    if target_id is None:
        return ()
    for relation in envelope.relations:
        same = relation.source == source_id and relation.target == target_id
        reverse = relation.source == target_id and relation.target == source_id
        if same or reverse:
            return relation.evidence
    return ()


def proposal_to_candidate_operation(
    proposal: Mapping[str, Any],
    envelope: MegaSorterEnvelope,
) -> tuple[PhaseOperation, RelationalState]:
    """Convert a MegaSorter proposal into a read-only PNV candidate.

    The proposal is *not* an actuator command. Its evidence must resolve to a
    relation in the originating NOEMA envelope. A proposal without such a
    relation is still representable, but Gate Fabric will HOLD it because the
    resulting operation has no evidence.
    """

    source_id = _proposal_endpoint(proposal, "source")
    target_id = _proposal_endpoint(proposal, "target")
    if source_id is None:
        raise ValueError("MegaSorter proposal has no source identifier")

    nodes = _node_map(envelope)
    source = nodes.get(source_id)
    if source is None:
        raise ValueError(f"proposal source {source_id!r} is not present in originating envelope")
    target = nodes.get(target_id) if target_id is not None else None

    evidence = _relation_evidence(envelope, source_id, target_id)
    signature_node = target or source
    signature_space = _phase_space(signature_node.phase_space)
    action = str(
        proposal.get("gate_type")
        or proposal.get("action")
        or proposal.get("kind")
        or proposal.get("edge_kind")
        or "MEGASORTER_PROPOSAL"
    )
    operation_id = _stable_id(
        "op:megasorter:candidate",
        {"batch": envelope.batch_id, "proposal": dict(proposal), "source": source_id, "target": target_id},
    )

    operation = PhaseOperation(
        operation_id=operation_id,
        relation_type=action,
        source_id=source_id,
        target_id=target_id,
        phase_signature36=signature_node.phase36,
        phase_signature_space=signature_space,
        mutation_class="READ_ONLY",
        evidence=evidence,
        provenance_requirements=source.provenance,
        authority_requirements=(),
        reversible=True,
        return_required=True,
        metadata={
            "origin": "MEGASORTER",
            "originating_batch": envelope.batch_id,
            "proposal": dict(proposal),
            "proposal_confidence": proposal.get("confidence"),
            "mutation_allowed_by_megasorter": bool(proposal.get("mutation_allowed", False)),
            "candidate_only": True,
            "evidence_resolved_from_envelope": bool(evidence),
        },
    )
    return operation, node_to_relational_state(source)


def proposal_batch_to_candidate_operations(
    payload: Mapping[str, Any],
    envelope: MegaSorterEnvelope,
) -> tuple[tuple[PhaseOperation, RelationalState], ...]:
    """Validate `NOEMA_MEGASORTER_PROPOSALS_V1` and recover candidate operations.

    The batch is advisory-only. It cannot upgrade itself to mutation authority,
    cannot target a different originating envelope, and cannot supply evidence as
    authority. Evidence is always re-resolved from `envelope.relations`.
    """

    if not isinstance(payload, Mapping):
        raise ValueError("MegaSorter proposal batch must be an object")
    if payload.get("schema") != PROPOSALS_SCHEMA:
        raise ValueError(f"unsupported MegaSorter proposal schema: {payload.get('schema')!r}")
    if payload.get("source") != "MEGASORTER":
        raise ValueError("MegaSorter proposal batch source must be 'MEGASORTER'")
    if payload.get("mode") != "ADVISORY_ONLY":
        raise ValueError("MegaSorter proposal batch must be ADVISORY_ONLY")
    if payload.get("mutation_allowed") is not False:
        raise ValueError("MegaSorter proposal batch cannot grant mutation authority")
    if payload.get("originating_batch") != envelope.batch_id:
        raise ValueError(
            "MegaSorter proposal batch does not match originating NOEMA envelope"
        )

    metadata = payload.get("metadata", {})
    if not isinstance(metadata, Mapping):
        raise ValueError("MegaSorter proposal batch metadata must be an object")
    evidence_authority = metadata.get("evidence_authority")
    if evidence_authority not in (None, "ORIGINATING_NOEMA_ENVELOPE"):
        raise ValueError("MegaSorter proposal batch declares an invalid evidence authority")

    proposals = payload.get("proposals")
    if not isinstance(proposals, (list, tuple)):
        raise ValueError("MegaSorter proposal batch proposals must be a list/tuple")

    candidates: list[tuple[PhaseOperation, RelationalState]] = []
    for index, proposal in enumerate(proposals):
        if not isinstance(proposal, Mapping):
            raise ValueError(f"MegaSorter proposal {index} must be an object")
        if proposal.get("candidate_only") is not True:
            raise ValueError(f"MegaSorter proposal {index} must be candidate_only=true")
        if proposal.get("mutation_allowed") is not False:
            raise ValueError(f"MegaSorter proposal {index} cannot grant mutation authority")
        proposal_batch = proposal.get("originating_batch")
        if proposal_batch not in (None, envelope.batch_id):
            raise ValueError(f"MegaSorter proposal {index} targets a different envelope")
        candidates.append(proposal_to_candidate_operation(proposal, envelope))

    return tuple(candidates)


__all__ = [
    "SCHEMA",
    "PROPOSALS_SCHEMA",
    "MegaSorterNode",
    "MegaSorterRelation",
    "MegaSorterEnvelope",
    "build_rag_envelope",
    "node_to_relational_state",
    "proposal_to_candidate_operation",
    "proposal_batch_to_candidate_operations",
]
