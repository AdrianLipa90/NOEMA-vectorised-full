from __future__ import annotations
import unittest

from noema_native.seed_v14 import build_validated_seed
from noema_native.crystal import CrystalSplit
from noema_native.crystal_calibration import StratifiedGroupedCorpusBuilder
from noema_native.crystal_backend_v2 import FeatureDeltaBackendV2, FeatureDeltaCalibrationV2


class FeatureDeltaBackendV17Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cards,cls.graph,cls.trajectory=build_validated_seed()
        cls.corpus,cls.partition=StratifiedGroupedCorpusBuilder.build(
            cls.cards,cls.graph,trajectory=cls.trajectory
        )
        cls.fit=FeatureDeltaBackendV2.fit(cls.cards,cls.corpus)
        cls.report=FeatureDeltaCalibrationV2.evaluate(
            cls.cards,cls.corpus,cls.partition,cls.fit,
            relation_baseline=0.0,trajectory_baseline=0.0,
        )

    def test_fit_uses_train_only(self):
        expected=sum(1 for e in self.corpus.examples if e.split is CrystalSplit.TRAIN)
        self.assertEqual(self.fit.train_example_count,expected)
        self.assertTrue(self.fit.fitted); self.assertEqual(self.fit.epoch,1)

    def test_test_remains_sealed(self):
        self.assertTrue(self.report.test_sealed)

    def test_relation_validation_improves_over_v15(self):
        self.assertGreater(self.report.relation_score,self.report.relation_baseline)
        self.assertEqual(self.report.relation_score,0.4)

    def test_trajectory_validation_improves_over_v15(self):
        self.assertGreater(self.report.trajectory_score,self.report.trajectory_baseline)
        self.assertEqual(self.report.trajectory_score,0.5)

    def test_candidate_verdict_is_not_promotion(self):
        self.assertEqual(self.report.status,"PASS_VALIDATION_IMPROVEMENT_V2_CANDIDATE")
        self.assertEqual(set(self.report.improved_objectives),{"relation","trajectory"})

    def test_validation_candidate_pool_is_explicitly_transductive(self):
        self.assertTrue(self.report.transductive_candidate_pool)

    def test_deterministic(self):
        fit2=FeatureDeltaBackendV2.fit(tuple(reversed(self.cards)),self.corpus)
        report2=FeatureDeltaCalibrationV2.evaluate(
            tuple(reversed(self.cards)),self.corpus,self.partition,fit2,
            relation_baseline=0.0,trajectory_baseline=0.0,
        )
        self.assertEqual(self.fit.digest,fit2.digest)
        self.assertEqual(self.report.receipt,report2.receipt)

    def test_no_test_examples_are_consumed_by_fit_contract(self):
        train_digests=sorted(e.digest for e in self.corpus.examples if e.split is CrystalSplit.TRAIN)
        test_digests=sorted(e.digest for e in self.corpus.examples if e.split is CrystalSplit.TEST)
        self.assertTrue(train_digests); self.assertTrue(test_digests)
        self.assertFalse(set(train_digests)&set(test_digests))

if __name__=="__main__":
    unittest.main()
