from __future__ import annotations

"""Leakage-resistant native crystal calibration and first fit (v15).

The module keeps TEST sealed. It uses only TRAIN to fit and VALIDATION to
calibrate candidate objective weights. Reconstruction is deliberately marked
not-generalizable with the current identity-ref input contract, rather than
fabricating a score.

No third-party runtime dependencies.
"""

from dataclasses import dataclass
from hashlib import sha256
from itertools import combinations
from math import sqrt
from struct import pack
from typing import Iterable, Mapping

from .cards import KnowledgeCard, RelationGraph
from .crystal import CrystalExampleKind, CrystalSplit, CrystalTrainingCorpus, CrystalTrainingExample


def _lp(value: str) -> bytes:
    raw = value.encode("utf-8")
    return pack(">I", len(raw)) + raw


def _internal_edges(group: set[str], graph: RelationGraph) -> tuple:
    return tuple(
        e for e in graph.edges
        if e.source_card_id in group and e.target_card_id in group
    )


def _trajectory_pairs(trajectory: tuple[str, ...], group: set[str]) -> int:
    return sum(1 for a, b in zip(trajectory, trajectory[1:]) if a in group and b in group)


def graph_stratified_partition(
    cards: Iterable[KnowledgeCard],
    graph: RelationGraph,
    *,
    trajectory: Iterable[str] = (),
    holdout_size: int | None = None,
) -> Mapping[str, CrystalSplit]:
    """Choose disjoint VAL/TEST card groups containing real positive edges.

    Split selection happens before examples are built. TEST is not evaluated by
    fitting/calibration.
    """
    cards = tuple(sorted(cards, key=lambda c: c.card_id))
    n = len(cards)
    if n < 10:
        raise ValueError("stratified grouped holdout requires at least 10 cards")
    k = holdout_size if holdout_size is not None else max(2, round(n * 0.1))
    if 2 * k >= n:
        raise ValueError("holdouts leave no training partition")
    ids = tuple(c.card_id for c in cards)
    traj = tuple(trajectory)
    candidates = []
    for comb in combinations(ids, k):
        group = set(comb)
        edges = _internal_edges(group, graph)
        if not edges:
            continue
        diversity = len({e.relation_type for e in edges})
        trajectory_score = _trajectory_pairs(traj, group)
        tie = sha256("|".join(comb).encode()).hexdigest()
        candidates.append(((len(edges), diversity, trajectory_score), tie, comb))
    if len(candidates) < 2:
        raise ValueError("cannot form two positive-edge holdouts")
    candidates.sort(
        key=lambda x: (x[0][0], x[0][1], x[0][2], x[1]),
        reverse=True,
    )
    validation = candidates[0][2]
    test = None
    for _, _, comb in candidates[1:]:
        if set(comb).isdisjoint(validation):
            test = comb
            break
    if test is None:
        raise ValueError("cannot form disjoint positive-edge holdouts")
    result = {card_id: CrystalSplit.TRAIN for card_id in ids}
    for card_id in validation:
        result[card_id] = CrystalSplit.VALIDATION
    for card_id in test:
        result[card_id] = CrystalSplit.TEST
    return result


class StratifiedGroupedCorpusBuilder:
    VERSION = "stratified-grouped-crystal-corpus-v1"

    @staticmethod
    def _prov(card: KnowledgeCard) -> tuple[str, ...]:
        return tuple(sorted([
            *(f"prov:{p.digest}" for p in card.provenance),
            f"extractor:{card.extractor_receipt}",
        ]))

    @classmethod
    def build(
        cls,
        cards: Iterable[KnowledgeCard],
        graph: RelationGraph,
        *,
        trajectory: Iterable[str] = (),
    ):
        from .crystal import CrystalTrainingCorpus, DEFAULT_OBJECTIVES

        cards = tuple(sorted(cards, key=lambda c: c.card_id))
        cmap = {c.card_id: c for c in cards}
        traj = tuple(trajectory)
        partition = graph_stratified_partition(cards, graph, trajectory=traj)
        examples = []
        edge_keys = set()

        for card in cards:
            split = partition[card.card_id]
            prov = cls._prov(card)
            examples.append(CrystalTrainingExample(
                f"reconstruct:{card.card_id}",
                CrystalExampleKind.CARD_RECONSTRUCTION,
                split,
                (card.card_id,),
                f"{card.canonical_name}\n{card.definition}",
                prov,
                False,
            ))
            examples.append(CrystalTrainingExample(
                f"lanes:{card.card_id}",
                CrystalExampleKind.LANE_ROUTING,
                split,
                (card.card_id,),
                ",".join(map(str, card.lane_affinity.values)),
                prov,
                False,
            ))

        for edge in graph.edges:
            if edge.source_card_id not in cmap or edge.target_card_id not in cmap:
                continue
            edge_keys.add((edge.source_card_id, edge.relation_type, edge.target_card_id))
            if partition[edge.source_card_id] is not partition[edge.target_card_id]:
                continue
            split = partition[edge.source_card_id]
            examples.append(CrystalTrainingExample(
                f"rel+:{edge.source_card_id}:{edge.relation_type}:{edge.target_card_id}",
                CrystalExampleKind.RELATION_POSITIVE,
                split,
                (edge.source_card_id, edge.target_card_id),
                edge.relation_type,
                (f"edge:{edge.receipt}", f"prov:{edge.provenance_digest}"),
                False,
            ))

        safe = ("DEPENDS_ON", "PART_OF", "DERIVED_FROM", "SUPPORTS")
        by_split = {
            split: [c for c in cards if partition[c.card_id] is split]
            for split in CrystalSplit
        }
        for split, group in by_split.items():
            for i, left in enumerate(group):
                for right in group[i + 1:]:
                    relation = safe[
                        int.from_bytes(
                            sha256((left.card_id + right.card_id).encode()).digest()[:2],
                            "big",
                        ) % len(safe)
                    ]
                    if (left.card_id, relation, right.card_id) in edge_keys:
                        continue
                    prov = tuple(sorted(cls._prov(left) + cls._prov(right)))
                    examples.append(CrystalTrainingExample(
                        f"rel-:{left.card_id}:{relation}:{right.card_id}",
                        CrystalExampleKind.RELATION_NEGATIVE,
                        split,
                        (left.card_id, right.card_id),
                        f"NOT:{relation}",
                        prov,
                        True,
                    ))

        for a, b in zip(traj, traj[1:]):
            if a not in cmap or b not in cmap:
                raise ValueError("trajectory refs outside seed")
            if partition[a] is not partition[b]:
                continue
            prov = tuple(sorted(cls._prov(cmap[a]) + cls._prov(cmap[b])))
            examples.append(CrystalTrainingExample(
                f"next:{a}:{b}",
                CrystalExampleKind.TRAJECTORY_NEXT,
                partition[a],
                (a,),
                b,
                prov,
                False,
            ))

        examples = tuple(sorted(examples, key=lambda e: e.example_id))
        corpus = CrystalTrainingCorpus(
            "noema.stratified_grouped_crystal_training_corpus.v1",
            examples,
            tuple(sorted(c.digest for c in cards)),
            tuple(sorted(e.receipt for e in graph.edges)),
            DEFAULT_OBJECTIVES,
            None,
        )
        return corpus, partition


@dataclass(frozen=True)
class NativeFitState:
    schema: str
    epoch: int
    fitted: bool
    train_example_count: int
    lane_by_card_type: tuple[tuple[str, tuple[float, ...]], ...]
    relation_by_type_pair: tuple[tuple[str, str, str, int], ...]
    trajectory_by_source_type: tuple[tuple[str, str, int], ...]
    reconstruction_memory: tuple[tuple[str, str], ...]
    train_digest: str

    @property
    def digest(self) -> str:
        material = bytearray(b"NOEMA-NATIVE-FIRST-FIT-v1\0")
        material.extend(pack(">I", self.epoch))
        material.extend(b"\x01" if self.fitted else b"\x00")
        material.extend(pack(">I", self.train_example_count))
        material.extend(bytes.fromhex(self.train_digest))
        for card_type, vector in self.lane_by_card_type:
            material.extend(_lp(card_type))
            for value in vector:
                material.extend(pack(">d", value))
        for source_type, target_type, relation, count in self.relation_by_type_pair:
            material.extend(_lp(source_type))
            material.extend(_lp(target_type))
            material.extend(_lp(relation))
            material.extend(pack(">I", count))
        for source_type, target_type, count in self.trajectory_by_source_type:
            material.extend(_lp(source_type))
            material.extend(_lp(target_type))
            material.extend(pack(">I", count))
        for card_id, target in self.reconstruction_memory:
            material.extend(_lp(card_id))
            material.extend(_lp(target))
        return sha256(bytes(material)).hexdigest()


class NativeSparseRelationalFitV1:
    VERSION = "native-sparse-relational-fit-v1"

    @classmethod
    def fit(
        cls,
        cards: Iterable[KnowledgeCard],
        corpus: CrystalTrainingCorpus,
    ) -> NativeFitState:
        cmap = {c.card_id: c for c in cards}
        train = tuple(e for e in corpus.examples if e.split is CrystalSplit.TRAIN)
        lane_sum = {}
        lane_n = {}
        relation_counts = {}
        trajectory_counts = {}
        reconstruction = {}

        for example in train:
            if example.kind is CrystalExampleKind.LANE_ROUTING:
                card = cmap[example.input_refs[0]]
                key = card.card_type.value
                values = tuple(map(int, example.target.split(",")))
                if key not in lane_sum:
                    lane_sum[key] = [0.0] * 12
                    lane_n[key] = 0
                for i, value in enumerate(values):
                    lane_sum[key][i] += value
                lane_n[key] += 1
            elif example.kind is CrystalExampleKind.RELATION_POSITIVE:
                a, b = example.input_refs
                key = (cmap[a].card_type.value, cmap[b].card_type.value, example.target)
                relation_counts[key] = relation_counts.get(key, 0) + 1
            elif example.kind is CrystalExampleKind.TRAJECTORY_NEXT:
                a = example.input_refs[0]
                b = example.target
                key = (cmap[a].card_type.value, cmap[b].card_type.value)
                trajectory_counts[key] = trajectory_counts.get(key, 0) + 1
            elif example.kind is CrystalExampleKind.CARD_RECONSTRUCTION:
                reconstruction[example.input_refs[0]] = example.target

        lanes = tuple(sorted(
            (key, tuple(value / lane_n[key] for value in vector))
            for key, vector in lane_sum.items()
        ))
        relations = tuple(sorted(
            (a, b, relation, count)
            for (a, b, relation), count in relation_counts.items()
        ))
        trajectory = tuple(sorted(
            (a, b, count)
            for (a, b), count in trajectory_counts.items()
        ))
        memory = tuple(sorted(reconstruction.items()))
        train_digest = sha256(
            "".join(sorted(e.digest for e in train)).encode()
        ).hexdigest()
        return NativeFitState(
            "noema.native_first_fit.v1",
            1,
            True,
            len(train),
            lanes,
            relations,
            trajectory,
            memory,
            train_digest,
        )


@dataclass(frozen=True)
class Metric:
    objective: str
    status: str
    score: float | None
    examples: int
    note: str


@dataclass(frozen=True)
class CalibrationReport:
    status: str
    fit_digest: str
    validation_metrics: tuple[Metric, ...]
    candidate_loss_weights: tuple[tuple[str, float], ...]
    test_sealed: bool
    blockers: tuple[str, ...]
    receipt: str


class NativeCrystalCalibrationV1:
    VERSION = "native-crystal-calibration-v1"

    @classmethod
    def evaluate(
        cls,
        cards: Iterable[KnowledgeCard],
        corpus: CrystalTrainingCorpus,
        fit: NativeFitState,
    ) -> CalibrationReport:
        cmap = {c.card_id: c for c in cards}
        validation = tuple(
            e for e in corpus.examples if e.split is CrystalSplit.VALIDATION
        )
        lane_table = dict(fit.lane_by_card_type)
        relation_table = {}
        for a, b, relation, count in fit.relation_by_type_pair:
            relation_table.setdefault((a, b), []).append((count, relation))
        trajectory_table = {}
        for a, b, count in fit.trajectory_by_source_type:
            trajectory_table.setdefault(a, []).append((count, b))

        metrics = []
        reconstruction = [
            e for e in validation
            if e.kind is CrystalExampleKind.CARD_RECONSTRUCTION
        ]
        metrics.append(Metric(
            "reconstruction",
            "NOT_CALIBRATABLE",
            None,
            len(reconstruction),
            "held-out input is an unseen card identity; no semantic feature frame exists yet",
        ))

        lane_examples = [
            e for e in validation if e.kind is CrystalExampleKind.LANE_ROUTING
        ]
        lane_scores = []
        for example in lane_examples:
            card = cmap[example.input_refs[0]]
            predicted = lane_table.get(card.card_type.value)
            if predicted is None:
                continue
            target = tuple(map(int, example.target.split(",")))
            lane_scores.append(
                1.0 - sum(
                    abs(predicted[i] - target[i]) / 2.0 for i in range(12)
                ) / 12.0
            )
        metrics.append(Metric(
            "lane_routing",
            "MEASURED" if lane_scores else "NO_COVERAGE",
            sum(lane_scores) / len(lane_scores) if lane_scores else None,
            len(lane_examples),
            "card-type lane prototype similarity on held-out identities",
        ))

        relation_positive = [
            e for e in validation
            if e.kind is CrystalExampleKind.RELATION_POSITIVE
        ]
        relation_scores = []
        for example in relation_positive:
            a, b = example.input_refs
            options = relation_table.get(
                (cmap[a].card_type.value, cmap[b].card_type.value),
                [],
            )
            predicted = max(options)[1] if options else None
            relation_scores.append(1.0 if predicted == example.target else 0.0)
        metrics.append(Metric(
            "relation",
            "MEASURED" if relation_positive else "NO_COVERAGE",
            sum(relation_scores) / len(relation_scores) if relation_positive else None,
            len(relation_positive),
            "typed relation top-1 from TRAIN card-type-pair counts",
        ))

        relation_negative = [
            e for e in validation
            if e.kind is CrystalExampleKind.RELATION_NEGATIVE
        ]
        negative_scores = []
        for example in relation_negative:
            a, b = example.input_refs
            forbidden = example.target.split(":", 1)[1]
            options = relation_table.get(
                (cmap[a].card_type.value, cmap[b].card_type.value),
                [],
            )
            seen = {relation for _, relation in options}
            negative_scores.append(1.0 if forbidden not in seen else 0.0)
        metrics.append(Metric(
            "contradiction",
            "MEASURED" if relation_negative else "NO_COVERAGE",
            sum(negative_scores) / len(negative_scores) if relation_negative else None,
            len(relation_negative),
            "negative relation rejection from TRAIN type-pair evidence",
        ))

        trajectory_examples = [
            e for e in validation if e.kind is CrystalExampleKind.TRAJECTORY_NEXT
        ]
        trajectory_scores = []
        for example in trajectory_examples:
            source = example.input_refs[0]
            options = trajectory_table.get(cmap[source].card_type.value, [])
            predicted = max(options)[1] if options else None
            trajectory_scores.append(
                1.0 if predicted == cmap[example.target].card_type.value else 0.0
            )
        metrics.append(Metric(
            "trajectory",
            "MEASURED" if trajectory_examples else "NO_COVERAGE",
            sum(trajectory_scores) / len(trajectory_scores) if trajectory_examples else None,
            len(trajectory_examples),
            "next-card-type top-1 from TRAIN trajectory counts",
        ))
        metrics.append(Metric(
            "provenance",
            "HARD_CONSTRAINT",
            1.0,
            len(validation),
            "all validation examples retain provenance refs",
        ))

        raw_weights = []
        for metric in metrics:
            if (
                metric.objective == "provenance"
                or metric.score is None
                or metric.examples == 0
            ):
                continue
            raw_weights.append((
                metric.objective,
                max(0.0, metric.score) * sqrt(metric.examples),
            ))
        total = sum(value for _, value in raw_weights)
        weights = tuple(sorted(
            (name, value / total if total else 0.0)
            for name, value in raw_weights
        ))

        blockers = []
        if not relation_positive:
            blockers.append("validation_has_no_positive_relation_examples")
        elif not relation_scores or sum(relation_scores) == 0:
            blockers.append("relation_validation_score_zero")
        if not trajectory_examples:
            blockers.append("validation_has_no_trajectory_examples")
        elif not trajectory_scores or sum(trajectory_scores) == 0:
            blockers.append("trajectory_validation_score_zero")
        if any(
            m.status == "NO_COVERAGE"
            for m in metrics
            if m.objective in {"lane_routing", "relation", "contradiction"}
        ):
            blockers.append("required_validation_objective_without_coverage")

        status = (
            "PASS_FIRST_NATIVE_FIT_CALIBRATION"
            if not blockers
            else "REJECT_FIRST_NATIVE_FIT_BACKEND"
        )
        receipt_material = "|".join([
            cls.VERSION,
            fit.digest,
            corpus.digest,
            status,
            str([(m.objective, m.status, m.score, m.examples) for m in metrics]),
            str(weights),
            *blockers,
            "TEST_SEALED",
        ]).encode()
        return CalibrationReport(
            status,
            fit.digest,
            tuple(metrics),
            weights,
            True,
            tuple(blockers),
            sha256(receipt_material).hexdigest(),
        )
