import unittest

from noema_native.seed_v14 import build_validated_seed
from noema_native.card_features import (
    CardFeatureFrameBuilder,
    FeatureView,
    OBJECTIVE_FEATURE_POLICY,
    SparseLexical64,
    structural_distance,
    relational_distance,
)


class CardFeatureFrameV16Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cards, _, _ = build_validated_seed()

    def test_structural_view_has_no_lexical_payload(self):
        frame = CardFeatureFrameBuilder.build(self.cards[0], FeatureView.STRUCTURAL)
        self.assertIsNone(frame.lexical64)

    def test_relational_view_has_separate_64_bin_type(self):
        frame = CardFeatureFrameBuilder.build(
            self.cards[0], FeatureView.RELATIONAL_SEMANTIC
        )
        self.assertIsInstance(frame.lexical64, SparseLexical64)
        self.assertEqual(len(frame.lexical64.values), 64)
        self.assertTrue(all(x in (-1, 0, 1) for x in frame.lexical64.values))

    def test_deterministic_frames(self):
        for view in FeatureView:
            a = CardFeatureFrameBuilder.build_many(self.cards, view)
            b = CardFeatureFrameBuilder.build_many(tuple(reversed(self.cards)), view)
            self.assertEqual(tuple(x.digest for x in a), tuple(x.digest for x in b))

    def test_distances_are_zero_for_identity(self):
        structural = CardFeatureFrameBuilder.build(self.cards[0], FeatureView.STRUCTURAL)
        relational = CardFeatureFrameBuilder.build(
            self.cards[0], FeatureView.RELATIONAL_SEMANTIC
        )
        self.assertEqual(structural_distance(structural, structural), 0.0)
        self.assertEqual(relational_distance(relational, relational), 0.0)

    def test_reconstruction_has_no_feature_policy(self):
        self.assertIsNone(OBJECTIVE_FEATURE_POLICY["reconstruction"])
        self.assertIs(
            OBJECTIVE_FEATURE_POLICY["relation"], FeatureView.RELATIONAL_SEMANTIC
        )
        self.assertIs(OBJECTIVE_FEATURE_POLICY["trajectory"], FeatureView.STRUCTURAL)

    def test_frame_digests_do_not_alias_36d_types(self):
        structural = CardFeatureFrameBuilder.build(self.cards[0], FeatureView.STRUCTURAL)
        relational = CardFeatureFrameBuilder.build(
            self.cards[0], FeatureView.RELATIONAL_SEMANTIC
        )
        self.assertNotEqual(structural.digest, relational.digest)
        self.assertNotEqual(structural.view, relational.view)


if __name__ == "__main__":
    unittest.main()
