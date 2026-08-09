from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ciel_geometry.phasenav.associator import associator_defect, compression_associator


def _phase(value: float) -> tuple[float, ...]:
    return tuple([value] * 36)


def test_generic_associator_is_zero_for_associative_addition():
    measurement = associator_defect(
        1.0,
        2.0,
        3.0,
        compose=lambda a, b: a + b,
        distance=lambda a, b: abs(a - b),
        kind="ADDITION",
    )
    assert measurement.defect == 0.0
    assert measurement.left == measurement.right == 6.0


def test_lossy_pairwise_phase_compression_has_nonzero_associator():
    measurement = compression_associator(
        _phase(0.0),
        _phase(math.pi / 2.0),
        _phase(math.pi),
        provenance=("test:a", "test:b", "test:c"),
    )
    assert measurement.kind == "PHASE_COMPRESSION_ASSOCIATOR"
    assert measurement.metric == "rms_angular_distance_over_pi"
    assert measurement.provenance == ("test:a", "test:b", "test:c")
    assert 0.24 < measurement.defect < 0.26


def test_identical_phases_have_zero_compression_associator():
    p = _phase(math.pi / 3.0)
    measurement = compression_associator(p, p, p)
    assert measurement.defect < 1e-12
