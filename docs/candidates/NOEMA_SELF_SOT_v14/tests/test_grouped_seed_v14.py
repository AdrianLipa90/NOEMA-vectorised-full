from __future__ import annotations
import unittest
from noema_native.seed_v14 import seed_records, build_validated_seed
from noema_native.grouped_crystal import GroupedCrystalCorpusBuilder, GroupedCrystalBenchmark, card_partition
from noema_native.crystal_train import NativeCrystalTopologyBuilder

class SeedV14Tests(unittest.TestCase):
    def test_seed_has_training_floor(self):
        self.assertGreaterEqual(len(seed_records()),32)
    def test_seed_admits_without_merge_holds(self):
        cards,g,traj=build_validated_seed(); self.assertGreaterEqual(len(cards),32); self.assertGreater(len(g.edges),20)
    def test_partition_has_disjoint_groups(self):
        cards,g,traj=build_validated_seed(); p=card_partition(cards)
        self.assertEqual(set(p),{c.card_id for c in cards})
        self.assertEqual(set(x.value for x in p.values()),{'TRAIN','VALIDATION','TEST'})
    def test_grouped_corpus_has_no_card_leakage(self):
        cards,g,traj=build_validated_seed(); corpus,p=GroupedCrystalCorpusBuilder.build(cards,g,trajectory=traj); report=GroupedCrystalBenchmark.evaluate(corpus,p)
        self.assertEqual(report.status,'PASS_GROUPED_GENERALIZATION_GATE'); self.assertEqual(report.blockers,()); self.assertEqual(report.provenance_coverage,1.0)
        self.assertTrue(all(not x for x in report.cross_split_card_overlap.values()))
    def test_topology_pristine(self):
        cards,g,traj=build_validated_seed(); top=NativeCrystalTopologyBuilder.build(cards,g,trajectory=traj)
        self.assertFalse(top.fitted); self.assertEqual(top.epoch,0); self.assertGreaterEqual(len(top.nodes),32)

if __name__=='__main__': unittest.main()
