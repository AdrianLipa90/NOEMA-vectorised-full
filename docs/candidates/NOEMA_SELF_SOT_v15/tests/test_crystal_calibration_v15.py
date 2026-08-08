import unittest

from noema_native.seed_v14 import build_validated_seed
from noema_native.crystal import CrystalExampleKind, CrystalSplit
from noema_native.crystal_calibration import (
    StratifiedGroupedCorpusBuilder,
    NativeSparseRelationalFitV1,
    NativeCrystalCalibrationV1,
)


class CrystalCalibrationV15Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cards, cls.graph, cls.trajectory = build_validated_seed()
        cls.corpus, cls.partition = StratifiedGroupedCorpusBuilder.build(
            cls.cards, cls.graph, trajectory=cls.trajectory
        )

    def test_partition_is_disjoint_and_complete(self):
        self.assertEqual(set(self.partition), {c.card_id for c in self.cards})
        self.assertEqual(sum(1 for s in self.partition.values() if s is CrystalSplit.VALIDATION), 4)
        self.assertEqual(sum(1 for s in self.partition.values() if s is CrystalSplit.TEST), 4)
        self.assertEqual(sum(1 for s in self.partition.values() if s is CrystalSplit.TRAIN), 34)

    def test_validation_and_test_have_real_positive_edges(self):
        for split in (CrystalSplit.VALIDATION, CrystalSplit.TEST):
            positives = [
                e for e in self.corpus.examples
                if e.split is split and e.kind is CrystalExampleKind.RELATION_POSITIVE
            ]
            self.assertGreater(len(positives), 0)

    def test_no_cross_split_card_identity_leakage(self):
        refs = {s: set() for s in CrystalSplit}
        for example in self.corpus.examples:
            refs[example.split].update(
                x for x in example.input_refs if x.startswith("card:")
            )
        self.assertFalse(refs[CrystalSplit.TRAIN] & refs[CrystalSplit.VALIDATION])
        self.assertFalse(refs[CrystalSplit.TRAIN] & refs[CrystalSplit.TEST])
        self.assertFalse(refs[CrystalSplit.VALIDATION] & refs[CrystalSplit.TEST])

    def test_first_fit_uses_train_only(self):
        fit = NativeSparseRelationalFitV1.fit(self.cards, self.corpus)
        self.assertTrue(fit.fitted)
        self.assertEqual(fit.epoch, 1)
        self.assertEqual(
            fit.train_example_count,
            sum(1 for e in self.corpus.examples if e.split is CrystalSplit.TRAIN),
        )
        held = {
            card_id for card_id, split in self.partition.items()
            if split is not CrystalSplit.TRAIN
        }
        self.assertTrue(all(card_id not in held for card_id, _ in fit.reconstruction_memory))

    def test_calibration_keeps_test_sealed_and_reconstruction_honest(self):
        fit = NativeSparseRelationalFitV1.fit(self.cards, self.corpus)
        report = NativeCrystalCalibrationV1.evaluate(self.cards, self.corpus, fit)
        self.assertTrue(report.test_sealed)
        reconstruction = next(
            m for m in report.validation_metrics if m.objective == "reconstruction"
        )
        self.assertEqual(reconstruction.status, "NOT_CALIBRATABLE")
        self.assertIsNone(reconstruction.score)
        self.assertNotIn("reconstruction", dict(report.candidate_loss_weights))

    def test_candidate_weights_are_normalized_when_present(self):
        fit = NativeSparseRelationalFitV1.fit(self.cards, self.corpus)
        report = NativeCrystalCalibrationV1.evaluate(self.cards, self.corpus, fit)
        if report.candidate_loss_weights:
            self.assertAlmostEqual(
                sum(value for _, value in report.candidate_loss_weights), 1.0, places=12
            )
        self.assertTrue(all(value >= 0 for _, value in report.candidate_loss_weights))

    def test_deterministic(self):
        corpus2, partition2 = StratifiedGroupedCorpusBuilder.build(
            self.cards, self.graph, trajectory=self.trajectory
        )
        self.assertEqual(self.corpus.digest, corpus2.digest)
        self.assertEqual(self.partition, partition2)
        fit1 = NativeSparseRelationalFitV1.fit(self.cards, self.corpus)
        fit2 = NativeSparseRelationalFitV1.fit(self.cards, corpus2)
        self.assertEqual(fit1.digest, fit2.digest)
        self.assertEqual(
            NativeCrystalCalibrationV1.evaluate(self.cards, self.corpus, fit1).receipt,
            NativeCrystalCalibrationV1.evaluate(self.cards, corpus2, fit2).receipt,
        )


if __name__ == "__main__":
    unittest.main()
