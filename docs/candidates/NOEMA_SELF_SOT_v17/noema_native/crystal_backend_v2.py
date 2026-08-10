from __future__ import annotations

"""Feature-delta backend v2 for controlled NOEMA crystal calibration (v17).

This backend is deliberately small, deterministic and stdlib-only.

Training authority:
- fit uses TRAIN examples only;
- VALIDATION is used only to measure/calibrate the candidate backend;
- TEST remains sealed;
- no weights or backend are promoted to canonical SoT here.

Feature authority:
- relation classification uses RELATIONAL_SEMANTIC CardFeatureFrame lexical deltas;
- trajectory ranking uses STRUCTURAL CardFeatureFrame lane deltas only;
- reconstruction remains out of scope and receives no semantic feature view;
- SparseLexical64 remains distinct from NOEMA Vector36 and CIELingoPhase36.
"""

from dataclasses import dataclass
from hashlib import sha256
from struct import pack
from typing import Iterable, Mapping

from .cards import KnowledgeCard
from .card_features import CardFeatureFrameBuilder, FeatureView
from .crystal import CrystalExampleKind, CrystalSplit, CrystalTrainingCorpus


def _lp(value: str) -> bytes:
    raw=value.encode("utf-8")
    return pack(">I",len(raw))+raw


def _mean(rows: list[tuple[float,...]]) -> tuple[float,...]:
    if not rows:
        raise ValueError("cannot average empty rows")
    return tuple(sum(col)/len(rows) for col in zip(*rows))


def _mse(a: tuple[float,...], b: tuple[float,...]) -> float:
    if len(a)!=len(b):
        raise ValueError("feature length mismatch")
    if not a:
        return 0.0
    return sum((x-y)*(x-y) for x,y in zip(a,b))/len(a)


def _lex_delta(a,b) -> tuple[float,...]:
    if a.lexical64 is None or b.lexical64 is None:
        raise ValueError("relation delta requires RELATIONAL_SEMANTIC frames")
    return tuple(float(y-x) for x,y in zip(a.lexical64.values,b.lexical64.values))


def _lane_delta(a,b) -> tuple[float,...]:
    return tuple(float(y-x) for x,y in zip(a.lane_affinity,b.lane_affinity))


@dataclass(frozen=True)
class FeatureDeltaFitV2:
    schema: str
    epoch: int
    fitted: bool
    train_example_count: int
    relation_delta_prototypes: tuple[tuple[str,tuple[float,...],int],...]
    trajectory_lane_delta: tuple[float,...]
    trajectory_count: int
    train_digest: str

    @property
    def digest(self) -> str:
        b=bytearray(b"NOEMA-FEATURE-DELTA-FIT-v2\0")
        b.extend(pack(">I",self.epoch))
        b.extend(b"\x01" if self.fitted else b"\x00")
        b.extend(pack(">I",self.train_example_count))
        b.extend(bytes.fromhex(self.train_digest))
        for relation,vec,count in self.relation_delta_prototypes:
            b.extend(_lp(relation)); b.extend(pack(">I",count))
            for x in vec: b.extend(pack(">d",x))
        b.extend(pack(">I",self.trajectory_count))
        for x in self.trajectory_lane_delta: b.extend(pack(">d",x))
        return sha256(bytes(b)).hexdigest()


class FeatureDeltaBackendV2:
    VERSION="feature-delta-backend-v2"

    @classmethod
    def fit(cls,cards:Iterable[KnowledgeCard],corpus:CrystalTrainingCorpus) -> FeatureDeltaFitV2:
        cards=tuple(cards)
        rel={f.card_id:f for f in CardFeatureFrameBuilder.build_many(cards,FeatureView.RELATIONAL_SEMANTIC)}
        structural={f.card_id:f for f in CardFeatureFrameBuilder.build_many(cards,FeatureView.STRUCTURAL)}
        train=tuple(e for e in corpus.examples if e.split is CrystalSplit.TRAIN)
        by_relation:dict[str,list[tuple[float,...]]]={}
        trajectory:list[tuple[float,...]]=[]
        for e in train:
            if e.kind is CrystalExampleKind.RELATION_POSITIVE:
                a,b=e.input_refs
                by_relation.setdefault(e.target,[]).append(_lex_delta(rel[a],rel[b]))
            elif e.kind is CrystalExampleKind.TRAJECTORY_NEXT:
                a=e.input_refs[0]; b=e.target
                trajectory.append(_lane_delta(structural[a],structural[b]))
        if not by_relation:
            raise ValueError("TRAIN has no positive relation examples")
        if not trajectory:
            raise ValueError("TRAIN has no trajectory examples")
        relation_prototypes=tuple(sorted(
            (relation,_mean(rows),len(rows)) for relation,rows in by_relation.items()
        ))
        td=sha256("".join(sorted(e.digest for e in train)).encode()).hexdigest()
        return FeatureDeltaFitV2(
            schema="noema.feature_delta_fit.v2",
            epoch=1,
            fitted=True,
            train_example_count=len(train),
            relation_delta_prototypes=relation_prototypes,
            trajectory_lane_delta=_mean(trajectory),
            trajectory_count=len(trajectory),
            train_digest=td,
        )

    @staticmethod
    def relation_predict(fit:FeatureDeltaFitV2,left,right) -> str:
        delta=_lex_delta(left,right)
        ranked=sorted(
            (_mse(delta,prototype),relation)
            for relation,prototype,_ in fit.relation_delta_prototypes
        )
        return ranked[0][1]

    @staticmethod
    def trajectory_rank(
        fit:FeatureDeltaFitV2,
        source,
        candidates:Iterable,
    ) -> tuple[str,...]:
        scored=[]
        for candidate in candidates:
            if candidate.card_id==source.card_id:
                continue
            delta=_lane_delta(source,candidate)
            scored.append((_mse(delta,fit.trajectory_lane_delta),candidate.card_id))
        return tuple(card_id for _,card_id in sorted(scored))


@dataclass(frozen=True)
class FeatureDeltaValidationV2:
    status: str
    fit_digest: str
    relation_score: float
    relation_examples: int
    trajectory_score: float
    trajectory_examples: int
    relation_baseline: float
    trajectory_baseline: float
    improved_objectives: tuple[str,...]
    test_sealed: bool
    transductive_candidate_pool: bool
    receipt: str


class FeatureDeltaCalibrationV2:
    VERSION="feature-delta-calibration-v2"

    @classmethod
    def evaluate(
        cls,
        cards:Iterable[KnowledgeCard],
        corpus:CrystalTrainingCorpus,
        partition:Mapping[str,CrystalSplit],
        fit:FeatureDeltaFitV2,
        *,
        relation_baseline:float=0.0,
        trajectory_baseline:float=0.0,
    ) -> FeatureDeltaValidationV2:
        cards=tuple(cards)
        rel={f.card_id:f for f in CardFeatureFrameBuilder.build_many(cards,FeatureView.RELATIONAL_SEMANTIC)}
        structural={f.card_id:f for f in CardFeatureFrameBuilder.build_many(cards,FeatureView.STRUCTURAL)}
        val=tuple(e for e in corpus.examples if e.split is CrystalSplit.VALIDATION)

        rp=[e for e in val if e.kind is CrystalExampleKind.RELATION_POSITIVE]
        relation_hits=0
        for e in rp:
            a,b=e.input_refs
            relation_hits += cls._relation_hit(fit,rel[a],rel[b],e.target)
        relation_score=relation_hits/len(rp) if rp else 0.0

        te=[e for e in val if e.kind is CrystalExampleKind.TRAJECTORY_NEXT]
        val_ids=tuple(sorted(cid for cid,split in partition.items() if split is CrystalSplit.VALIDATION))
        trajectory_hits=0
        for e in te:
            source=structural[e.input_refs[0]]
            candidates=[structural[cid] for cid in val_ids if cid!=source.card_id]
            ranked=FeatureDeltaBackendV2.trajectory_rank(fit,source,candidates)
            trajectory_hits += int(bool(ranked) and ranked[0]==e.target)
        trajectory_score=trajectory_hits/len(te) if te else 0.0

        improved=[]
        if relation_score>relation_baseline: improved.append("relation")
        if trajectory_score>trajectory_baseline: improved.append("trajectory")
        status="PASS_VALIDATION_IMPROVEMENT_V2_CANDIDATE" if improved else "REJECT_FEATURE_DELTA_BACKEND_V2"

        material="|".join([
            cls.VERSION,fit.digest,status,
            f"{relation_score:.17g}",str(len(rp)),
            f"{trajectory_score:.17g}",str(len(te)),
            f"{relation_baseline:.17g}",f"{trajectory_baseline:.17g}",
            ",".join(improved),"TEST_SEALED","TRANSDUCTIVE_VALIDATION_POOL",
        ]).encode()
        return FeatureDeltaValidationV2(
            status=status,
            fit_digest=fit.digest,
            relation_score=relation_score,
            relation_examples=len(rp),
            trajectory_score=trajectory_score,
            trajectory_examples=len(te),
            relation_baseline=relation_baseline,
            trajectory_baseline=trajectory_baseline,
            improved_objectives=tuple(improved),
            test_sealed=True,
            transductive_candidate_pool=True,
            receipt=sha256(material).hexdigest(),
        )

    @staticmethod
    def _relation_hit(fit,left,right,target)->int:
        return int(FeatureDeltaBackendV2.relation_predict(fit,left,right)==target)
