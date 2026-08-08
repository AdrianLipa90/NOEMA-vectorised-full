from __future__ import annotations

"""Leakage-resistant grouped corpus builder and benchmark for crystal seed v14."""

from dataclasses import dataclass
from hashlib import sha256
from typing import Iterable, Mapping

from .cards import CardStatus, KnowledgeCard, RelationGraph
from .crystal import (
    CrystalExampleKind, CrystalSplit, CrystalTrainingCorpus,
    CrystalTrainingExample, DEFAULT_OBJECTIVES,
)


def card_partition(cards: Iterable[KnowledgeCard]) -> Mapping[str, CrystalSplit]:
    cards = tuple(sorted(cards, key=lambda c: (sha256(c.card_id.encode()).hexdigest(), c.card_id)))
    n = len(cards)
    if n < 10:
        raise ValueError("grouped holdout requires at least 10 cards")
    n_val = max(1, round(n * 0.1))
    n_test = max(1, round(n * 0.1))
    n_train = n - n_val - n_test
    if n_train < 1:
        raise ValueError("empty train partition")
    out = {}
    for i, c in enumerate(cards):
        out[c.card_id] = CrystalSplit.TRAIN if i < n_train else (CrystalSplit.VALIDATION if i < n_train + n_val else CrystalSplit.TEST)
    return out


class GroupedCrystalCorpusBuilder:
    VERSION = "grouped-crystal-corpus-builder-v1"

    @staticmethod
    def _prov(card: KnowledgeCard):
        return tuple(sorted([*(f"prov:{p.digest}" for p in card.provenance), f"extractor:{card.extractor_receipt}"]))

    @classmethod
    def build(cls, cards: Iterable[KnowledgeCard], graph: RelationGraph, *, trajectory: Iterable[str] = ()):
        cards = tuple(sorted(cards, key=lambda c: c.card_id))
        if any(c.status not in {CardStatus.VALIDATED, CardStatus.PROMOTED} for c in cards):
            raise ValueError("grouped corpus accepts validated/promoted cards only")
        part = card_partition(cards)
        cmap = {c.card_id: c for c in cards}
        ex = []
        for c in cards:
            split = part[c.card_id]
            prov = cls._prov(c)
            ex.append(CrystalTrainingExample(f"reconstruct:{c.card_id}", CrystalExampleKind.CARD_RECONSTRUCTION, split, (c.card_id,), f"{c.canonical_name}\n{c.definition}", prov, False))
            ex.append(CrystalTrainingExample(f"lanes:{c.card_id}", CrystalExampleKind.LANE_ROUTING, split, (c.card_id,), ",".join(map(str, c.lane_affinity.values)), prov, False))
        edge_keys = set()
        for e in graph.edges:
            if e.source_card_id not in cmap or e.target_card_id not in cmap:
                continue
            edge_keys.add((e.source_card_id, e.relation_type, e.target_card_id))
            if part[e.source_card_id] is not part[e.target_card_id]:
                continue
            split = part[e.source_card_id]
            ex.append(CrystalTrainingExample(f"rel+:{e.source_card_id}:{e.relation_type}:{e.target_card_id}", CrystalExampleKind.RELATION_POSITIVE, split, (e.source_card_id, e.target_card_id), e.relation_type, (f"edge:{e.receipt}", f"prov:{e.provenance_digest}"), False))
        safe = ("DEPENDS_ON", "PART_OF", "DERIVED_FROM", "SUPPORTS")
        by_split = {s: [c for c in cards if part[c.card_id] is s] for s in CrystalSplit}
        for split, group in by_split.items():
            for i, left in enumerate(group):
                for right in group[i + 1:]:
                    relation = safe[int.from_bytes(sha256((left.card_id + right.card_id).encode()).digest()[:2], "big") % len(safe)]
                    if (left.card_id, relation, right.card_id) in edge_keys:
                        continue
                    prov = tuple(sorted(cls._prov(left) + cls._prov(right)))
                    ex.append(CrystalTrainingExample(f"rel-:{left.card_id}:{relation}:{right.card_id}", CrystalExampleKind.RELATION_NEGATIVE, split, (left.card_id, right.card_id), f"NOT:{relation}", prov, True))
        traj = tuple(trajectory)
        for a, b in zip(traj, traj[1:]):
            if a not in cmap or b not in cmap:
                raise ValueError("trajectory refs outside seed")
            if part[a] is not part[b]:
                continue
            prov = tuple(sorted(cls._prov(cmap[a]) + cls._prov(cmap[b])))
            ex.append(CrystalTrainingExample(f"next:{a}:{b}", CrystalExampleKind.TRAJECTORY_NEXT, part[a], (a,), b, prov, False))
        ex = tuple(sorted(ex, key=lambda x: x.example_id))
        corpus = CrystalTrainingCorpus("noema.grouped_crystal_training_corpus.v1", ex, tuple(sorted(c.digest for c in cards)), tuple(sorted(e.receipt for e in graph.edges)), DEFAULT_OBJECTIVES, None)
        return corpus, part


@dataclass(frozen=True)
class GroupedBenchmarkReport:
    status: str
    card_counts: Mapping[str, int]
    example_counts: Mapping[str, int]
    cross_split_card_overlap: Mapping[str, tuple[str, ...]]
    provenance_coverage: float
    blockers: tuple[str, ...]
    receipt: str


class GroupedCrystalBenchmark:
    VERSION = "grouped-crystal-benchmark-v1"

    @classmethod
    def evaluate(cls, corpus: CrystalTrainingCorpus, partition: Mapping[str, CrystalSplit]):
        blockers = []
        refs = {s.value: set() for s in CrystalSplit}
        for e in corpus.examples:
            refs[e.split.value].update(r for r in e.input_refs if r.startswith("card:"))
        overlap = {}
        pairs = ((CrystalSplit.TRAIN, CrystalSplit.VALIDATION), (CrystalSplit.TRAIN, CrystalSplit.TEST), (CrystalSplit.VALIDATION, CrystalSplit.TEST))
        for a, b in pairs:
            key = f"{a.value}__{b.value}"
            shared = tuple(sorted(refs[a.value] & refs[b.value]))
            overlap[key] = shared
            if shared:
                blockers.append(f"card_identity_leakage:{key}:{len(shared)}")
        if any(not refs[s.value] for s in CrystalSplit):
            blockers.append("empty_card_partition")
        prov = 1.0 if not corpus.examples else sum(bool(e.provenance_refs) for e in corpus.examples) / len(corpus.examples)
        if prov != 1.0:
            blockers.append("provenance_coverage_below_1")
        card_counts = {s.value: sum(1 for x in partition.values() if x is s) for s in CrystalSplit}
        status = "PASS_GROUPED_GENERALIZATION_GATE" if not blockers else "FAIL_GROUPED_GENERALIZATION_GATE"
        raw = "|".join([cls.VERSION, corpus.digest, status, str(card_counts), str(corpus.counts_by_split), str(overlap), str(prov), *blockers]).encode()
        return GroupedBenchmarkReport(status, card_counts, corpus.counts_by_split, overlap, prov, tuple(blockers), sha256(raw).hexdigest())
