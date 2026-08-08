from __future__ import annotations

"""Seed benchmark harness for NOEMA crystal preparation.

This is a smoke/data-integrity benchmark, not a claim of generalization.
It evaluates only deterministic baselines over held-out example splits and
reports cross-split card-reference overlap explicitly.

No third-party runtime dependencies.
"""

from collections import Counter, defaultdict
from dataclasses import dataclass
from hashlib import sha256
from struct import pack
from typing import Iterable, Mapping

from .crystal import CrystalSplit, CrystalTrainingCorpus, CrystalTrainingExample


def _lp(value: str) -> bytes:
    raw = value.encode("utf-8")
    return pack(">I", len(raw)) + raw


@dataclass(frozen=True)
class BaselineScore:
    name: str
    split: str
    correct: int
    total: int
    coverage: int

    @property
    def accuracy(self) -> float:
        return 0.0 if self.total == 0 else self.correct / self.total

    @property
    def coverage_rate(self) -> float:
        return 0.0 if self.total == 0 else self.coverage / self.total


@dataclass(frozen=True)
class CrystalSeedBenchmarkReport:
    corpus_digest: str
    status: str
    split_counts: Mapping[str, int]
    provenance_coverage: float
    exact_id_leakage: tuple[str, ...]
    cross_split_card_refs: Mapping[str, tuple[str, ...]]
    scores: tuple[BaselineScore, ...]
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]
    receipt: str


class CrystalSeedBenchmark:
    VERSION = "crystal-seed-benchmark-v1"

    @staticmethod
    def _train(corpus: CrystalTrainingCorpus) -> tuple[CrystalTrainingExample, ...]:
        return tuple(x for x in corpus.examples if x.split is CrystalSplit.TRAIN)

    @staticmethod
    def _eval(corpus: CrystalTrainingCorpus, split: CrystalSplit) -> tuple[CrystalTrainingExample, ...]:
        return tuple(x for x in corpus.examples if x.split is split)

    @staticmethod
    def _majority_by_kind(train: Iterable[CrystalTrainingExample]):
        counts: dict[str, Counter[str]] = defaultdict(Counter)
        for ex in train:
            counts[ex.kind.value][ex.target] += 1
        return {k: v.most_common(1)[0][0] for k, v in counts.items() if v}

    @staticmethod
    def _lookup(train: Iterable[CrystalTrainingExample]):
        out: dict[tuple[str, tuple[str, ...]], str] = {}
        conflicts: set[tuple[str, tuple[str, ...]]] = set()
        for ex in train:
            key = (ex.kind.value, ex.input_refs)
            if key in out and out[key] != ex.target:
                conflicts.add(key)
            else:
                out[key] = ex.target
        for key in conflicts:
            out.pop(key, None)
        return out

    @classmethod
    def _score_majority(cls, train, eval_set, split: CrystalSplit) -> BaselineScore:
        model = cls._majority_by_kind(train)
        correct = coverage = 0
        for ex in eval_set:
            pred = model.get(ex.kind.value)
            if pred is None:
                continue
            coverage += 1
            correct += int(pred == ex.target)
        return BaselineScore("majority_by_kind", split.value, correct, len(eval_set), coverage)

    @classmethod
    def _score_lookup(cls, train, eval_set, split: CrystalSplit) -> BaselineScore:
        model = cls._lookup(train)
        correct = coverage = 0
        for ex in eval_set:
            pred = model.get((ex.kind.value, ex.input_refs))
            if pred is None:
                continue
            coverage += 1
            correct += int(pred == ex.target)
        return BaselineScore("exact_input_lookup", split.value, correct, len(eval_set), coverage)

    @classmethod
    def evaluate(cls, corpus: CrystalTrainingCorpus) -> CrystalSeedBenchmarkReport:
        train = cls._train(corpus)
        by_split = {s: cls._eval(corpus, s) for s in CrystalSplit}
        blockers: list[str] = []
        warnings: list[str] = []

        ids_by_split = {s.value: {x.example_id for x in xs} for s, xs in by_split.items()}
        leakage = set()
        names = list(ids_by_split)
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                leakage |= ids_by_split[a] & ids_by_split[b]
        if leakage:
            blockers.append("example_id_cross_split_leakage")

        provenance_total = len(corpus.examples)
        provenance_ok = sum(1 for x in corpus.examples if x.provenance_refs)
        prov_cov = 1.0 if provenance_total == 0 else provenance_ok / provenance_total
        if prov_cov != 1.0:
            blockers.append("provenance_coverage_below_1")

        train_refs = {r for x in train for r in x.input_refs}
        overlap: dict[str, tuple[str, ...]] = {}
        for split in (CrystalSplit.VALIDATION, CrystalSplit.TEST):
            eval_refs = {r for x in by_split[split] for r in x.input_refs}
            shared = tuple(sorted(train_refs & eval_refs))
            overlap[split.value] = shared
            if shared:
                warnings.append(f"cross_task_card_reference_overlap:{split.value}:{len(shared)}")

        for split in (CrystalSplit.VALIDATION, CrystalSplit.TEST):
            if not by_split[split]:
                blockers.append(f"empty_{split.value.lower()}_split")

        scores = []
        for split in (CrystalSplit.VALIDATION, CrystalSplit.TEST):
            scores.append(cls._score_majority(train, by_split[split], split))
            scores.append(cls._score_lookup(train, by_split[split], split))

        warnings.append("seed_smoke_benchmark_only_not_generalization_evidence")
        if len(corpus.source_card_digests) < 32:
            warnings.append("seed_card_count_below_32")

        status = "PASS_SEED_SMOKE_BENCHMARK" if not blockers else "FAIL_SEED_SMOKE_BENCHMARK"
        material = bytearray(b"NOEMA-CRYSTAL-SEED-BENCHMARK-v1\0")
        material.extend(_lp(cls.VERSION)); material.extend(bytes.fromhex(corpus.digest)); material.extend(_lp(status))
        material.extend(pack(">d", prov_cov))
        for item in sorted(leakage): material.extend(_lp(item))
        for split, refs in sorted(overlap.items()):
            material.extend(_lp(split))
            for ref in refs: material.extend(_lp(ref))
        for score in scores:
            material.extend(_lp(score.name)); material.extend(_lp(score.split))
            material.extend(pack(">III", score.correct, score.total, score.coverage))
        for item in blockers: material.extend(_lp(item))
        for item in warnings: material.extend(_lp(item))
        receipt = sha256(bytes(material)).hexdigest()
        return CrystalSeedBenchmarkReport(
            corpus_digest=corpus.digest,
            status=status,
            split_counts=corpus.counts_by_split,
            provenance_coverage=prov_cov,
            exact_id_leakage=tuple(sorted(leakage)),
            cross_split_card_refs=overlap,
            scores=tuple(scores),
            blockers=tuple(blockers),
            warnings=tuple(warnings),
            receipt=receipt,
        )
