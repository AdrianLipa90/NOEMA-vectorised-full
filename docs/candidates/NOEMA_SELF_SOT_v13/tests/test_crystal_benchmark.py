from __future__ import annotations
import hashlib
import unittest

from noema_native.cards import CardExtractor, CardType, ClaimStatus, LaneAffinity12, MemoryAdmissionPolicy, RelationGraph, SeedRecord
from noema_native.crystal import CrystalCorpusBuilder
from noema_native.crystal_benchmark import CrystalSeedBenchmark
from noema_native.crystal_train import NativeCrystalTopologyBuilder, CrystalTrainingPlanner

SRC = hashlib.sha256(b"benchmark-seed").hexdigest()
REL = hashlib.sha256(b"benchmark-relation").hexdigest()

def cand(name, definition):
    rec = SeedRecord(
        source_id="unit", source_sha256=SRC, location=f"unit:{name}",
        canonical_name=name, definition=definition, card_type=CardType.CONCEPT,
        aliases=(), constraints=(), lane_affinity=LaneAffinity12((0,0,2,2,0,0,1,0,0,0,2,0)),
        claim_status=ClaimStatus.VALIDATED, receipt_ref="unit-receipt",
    )
    return CardExtractor.from_seed_record(rec)

class SeedBenchmarkTests(unittest.TestCase):
    def fixture(self):
        cards = [MemoryAdmissionPolicy.evaluate(cand(f"C{i}", f"Definition {i}."), existing_cards=()).validated_card for i in range(12)]
        g = RelationGraph()
        for c in cards: g.add_card(c)
        for a,b in zip(cards, cards[1:]):
            g.add_edge(a.card_id, "SUPPORTS", b.card_id, confidence=1.0, provenance_digest=REL)
        corpus = CrystalCorpusBuilder.build(cards, g, trajectory=tuple(c.card_id for c in cards))
        return cards, g, corpus

    def test_seed_benchmark_is_deterministic_and_provenance_complete(self):
        cards,g,corpus = self.fixture()
        a = CrystalSeedBenchmark.evaluate(corpus)
        b = CrystalSeedBenchmark.evaluate(corpus)
        self.assertEqual(a.receipt, b.receipt)
        self.assertEqual(a.status, "PASS_SEED_SMOKE_BENCHMARK")
        self.assertEqual(a.provenance_coverage, 1.0)
        self.assertEqual(a.exact_id_leakage, ())

    def test_benchmark_warns_that_it_is_not_generalization_evidence(self):
        _,_,corpus = self.fixture()
        report = CrystalSeedBenchmark.evaluate(corpus)
        self.assertIn("seed_smoke_benchmark_only_not_generalization_evidence", report.warnings)

    def test_native_topology_is_pristine_and_deterministic(self):
        cards,g,corpus = self.fixture()
        traj = tuple(c.card_id for c in cards)
        a = NativeCrystalTopologyBuilder.build(cards,g,trajectory=traj)
        b = NativeCrystalTopologyBuilder.build(reversed(cards),g,trajectory=traj)
        self.assertEqual(a.digest,b.digest)
        self.assertEqual(a.epoch,0); self.assertFalse(a.fitted)
        self.assertTrue(all(c.initial_weight == 0.0 for c in a.couplings))

    def test_training_stays_blocked_below_seed_floor(self):
        cards,g,corpus = self.fixture()
        topo = NativeCrystalTopologyBuilder.build(cards,g,trajectory=tuple(c.card_id for c in cards))
        report = CrystalSeedBenchmark.evaluate(corpus)
        plan = CrystalTrainingPlanner.prepare(topo, report)
        self.assertFalse(plan.trainer_enabled)
        self.assertEqual(plan.status, "BLOCKED_PENDING_SEED_EXPANSION")
        self.assertIn("seed_card_count_below_training_floor_32", plan.blockers)

if __name__ == "__main__": unittest.main()
