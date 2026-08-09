"""Versioned PLAN_ONLY bridge from NOEMA observations to MegaSorter.

The bridge intentionally does not import `orbitalsort` classes.  NOEMA remains
its own authority plane and emits a substrate-neutral envelope that an
installed/remote MegaSorter adapter may consume.

Invariant: co-retrieval does not create result-to-result semantic edges.  The
only automatic relation in a RAG batch is the evidenced `retrieved_for`
relation between a retrieved observation and its query node.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Mapping, Sequence

from ciel_geometry.phasenav.gate_contracts import PhaseSpace, RelationalObservation
from ciel_geometry.phasenav.pnv_precise import ENCODER_ID, order_parameter, sentence_phase_precise

SCHEMA = "NOEMA_MEGASORTER_ENVELOPE_V1"


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


def _observation_text(observation: RelationalObservation) -> str:
    payload = observation.payload
    essence = str(payload.get("essence") or "")
    filename = str(payload.get("filename") or "")
    return essence or filename or observation.observation_id


def build_rag_envelope(query: str, observations: Sequence[RelationalObservation]) -> MegaSorterEnvelope:
    """Build a relation-preserving MegaSorter batch for one RAG query."""

    query_text = str(query).strip()
    if not query_text:
        raise ValueError("query must not be empty")

    query_phase = sentence_phase_precise(query_text)
    query_id = "query:" + str(abs(hash(query_text)))
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
            # Do not silently project another 36D coordinate system.  Text can
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
    batch_id = "megasorter:rag:" + str(abs(hash((query_text, tuple(node.node_id for node in nodes)))))
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


__all__ = [
    "SCHEMA",
    "MegaSorterNode",
    "MegaSorterRelation",
    "MegaSorterEnvelope",
    "build_rag_envelope",
]
