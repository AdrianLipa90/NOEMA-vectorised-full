from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ciel_geometry.phasenav.pnv_precise import (
    ENCODER_ID,
    KAPPA,
    N,
    circular_alignment,
    collatz_hash,
    descriptor,
    order_parameter,
    phase_precise,
    sentence_phase_precise,
)


def test_precise_encoder_is_36d_and_bounded():
    vec = sentence_phase_precise("phase memory return")
    assert len(vec) == N == 36
    assert all(0.0 <= value < 2.0 * math.pi for value in vec)


def test_one_word_sentence_matches_precise_word_phasor():
    word = "return"
    h = collatz_hash(word)
    expected = tuple(phase_precise(h, axis) for axis in range(36))
    actual = sentence_phase_precise(word)
    for a, b in zip(actual, expected):
        assert abs(a - b) < 1e-12


def test_repeated_identical_word_does_not_change_phase():
    once = sentence_phase_precise("memory")
    repeated = sentence_phase_precise("memory memory memory")
    assert circular_alignment(once, repeated) > 1.0 - 1e-12


def test_order_parameter_is_normalized():
    vec = sentence_phase_precise("oracle sorter doctor actuator return")
    r = order_parameter(vec)
    assert 0.0 <= r <= 1.0


def test_descriptor_records_canonical_source_and_kappa():
    desc = descriptor()
    assert desc["dimensions"] == 36
    assert desc["encoder"] == ENCODER_ID
    assert abs(float(desc["kappa"]) - KAPPA) < 1e-15
    assert "noema-phasenav-core" in str(desc["source"])
