from __future__ import annotations

import math

from cielingo.collatz_semantic_htri_sync import BASE_FREQUENCY_HZ, synchronization_report


def test_collatz_semantic_htri_sync_report_shape():
    report = synchronization_report(".", query="słowo language semantic Collatz HTRI", limit=10)
    assert report["schema"] == "cielingo/collatz-semantic-htri-sync/v0.1"
    assert report["base_frequency_hz"] == BASE_FREQUENCY_HZ
    assert math.isclose(report["omega0_rad_s"], 2.0 * math.pi * 7.83)
    assert report["n_oscillators"] == 36
    assert report["card_count"] > 0
    assert 0.0 <= report["mean_phase_alignment"] <= 1.0
    assert 0.0 <= report["mean_sync_pressure"] <= 1.0
    assert report["actions"]
    first = report["states"][0]
    assert 0 <= first["oscillator_id"] < 36
    assert first["collatz_steps"] >= 1
    assert first["recommended_action"] in {
        "quarantine_for_semantic_htri_resync",
        "expand_then_rephase",
        "reduce_to_identity_cluster",
        "observe_reference_surface",
    }
