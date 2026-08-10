from __future__ import annotations

"""Native crystal topology and pre-training state.

This module prepares a trainable relational topology without fitting it.
No language model and no third-party numerical runtime is required.
"""

from dataclasses import dataclass
from hashlib import sha256
from struct import pack
from typing import Iterable

from .cards import CardStatus, KnowledgeCard, RelationGraph


def _lp(value: str) -> bytes:
    raw = value.encode("utf-8")
    return pack(">I", len(raw)) + raw


@dataclass(frozen=True)
class CrystalNode:
    card_id: str
    card_digest: str
    lane_affinity: tuple[int, ...]


@dataclass(frozen=True)
class CrystalCoupling:
    source_card_id: str
    target_card_id: str
    channel: str
    provenance_ref: str
    initial_weight: float = 0.0


@dataclass(frozen=True)
class NativeCrystalTopology:
    schema: str
    nodes: tuple[CrystalNode, ...]
    couplings: tuple[CrystalCoupling, ...]
    epoch: int
    fitted: bool

    @property
    def digest(self) -> str:
        material = bytearray(b"NOEMA-NATIVE-CRYSTAL-TOPOLOGY-v1\0")
        material.extend(_lp(self.schema)); material.extend(pack(">I", self.epoch))
        material.extend(b"\x01" if self.fitted else b"\x00")
        for n in self.nodes:
            material.extend(_lp(n.card_id)); material.extend(bytes.fromhex(n.card_digest))
            material.extend(bytes(n.lane_affinity))
        for c in self.couplings:
            material.extend(_lp(c.source_card_id)); material.extend(_lp(c.target_card_id))
            material.extend(_lp(c.channel)); material.extend(_lp(c.provenance_ref)); material.extend(pack(">d", c.initial_weight))
        return sha256(bytes(material)).hexdigest()


class NativeCrystalTopologyBuilder:
    VERSION = "native-crystal-topology-builder-v1"

    @classmethod
    def build(
        cls,
        cards: Iterable[KnowledgeCard],
        graph: RelationGraph,
        *,
        trajectory: Iterable[str] = (),
    ) -> NativeCrystalTopology:
        cards = tuple(sorted(cards, key=lambda c: c.card_id))
        if any(c.status not in {CardStatus.VALIDATED, CardStatus.PROMOTED} for c in cards):
            raise ValueError("topology accepts VALIDATED/PROMOTED cards only")
        card_map = {c.card_id: c for c in cards}
        nodes = tuple(CrystalNode(c.card_id, c.digest, c.lane_affinity.values) for c in cards)
        couplings: list[CrystalCoupling] = []
        for e in graph.edges:
            if e.source_card_id in card_map and e.target_card_id in card_map:
                couplings.append(CrystalCoupling(
                    e.source_card_id, e.target_card_id, f"RELATION:{e.relation_type}", f"edge:{e.receipt}"
                ))
        traj = tuple(trajectory)
        for a, b in zip(traj, traj[1:]):
            if a not in card_map or b not in card_map:
                raise ValueError("trajectory refs must point to supplied cards")
            prov = sha256((a + "\0" + b).encode("utf-8")).hexdigest()
            couplings.append(CrystalCoupling(a, b, "TRAJECTORY", f"trajectory:{prov}"))
        couplings.sort(key=lambda c: (c.source_card_id, c.channel, c.target_card_id, c.provenance_ref))
        return NativeCrystalTopology(
            schema="noema.native_crystal_topology.v1",
            nodes=nodes,
            couplings=tuple(couplings),
            epoch=0,
            fitted=False,
        )


@dataclass(frozen=True)
class CrystalTrainingPlan:
    backend: str
    topology_digest: str
    benchmark_receipt: str
    status: str
    trainer_enabled: bool
    blockers: tuple[str, ...]
    next_gate: str


class CrystalTrainingPlanner:
    """Prepare training authorization state; never silently starts fitting."""

    @staticmethod
    def prepare(topology: NativeCrystalTopology, benchmark_report) -> CrystalTrainingPlan:
        blockers: list[str] = []
        if topology.fitted or topology.epoch != 0:
            blockers.append("topology_not_pristine")
        if benchmark_report.status != "PASS_SEED_SMOKE_BENCHMARK":
            blockers.append("seed_benchmark_failed")
        if len(topology.nodes) < 32:
            blockers.append("seed_card_count_below_training_floor_32")
        status = "READY_FOR_SEED_EXPANSION" if not blockers else "BLOCKED_PENDING_SEED_EXPANSION"
        return CrystalTrainingPlan(
            backend="NOEMA_NATIVE_SPARSE_RELATIONAL_V1",
            topology_digest=topology.digest,
            benchmark_receipt=benchmark_report.receipt,
            status=status,
            trainer_enabled=False,
            blockers=tuple(blockers),
            next_gate="EXPAND_CANONICAL_SEED_AND_RUN_GROUPED_GENERALIZATION_BENCHMARK",
        )
