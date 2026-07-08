from __future__ import annotations

from cielingo.htri_phase_bus import bind_card_to_phase_bus, phase_bus_report, select_phase_bus_cards


def test_phase_bus_binds_language_cards_without_default_quarantine() -> None:
    cards = select_phase_bus_cards('.', limit=12)
    assert cards
    node = bind_card_to_phase_bus(cards[0])
    assert node.card_id == cards[0].card_id
    assert node.base_frequency_hz == 7.83
    assert 0 <= node.phase_alignment <= 1
    assert 0 <= node.j_bus_total <= 1
    assert node.phase_lane in {'phase_locked', 'phase_coupled', 'phase_tension', 'phase_saturated'}
    assert node.bus_action != 'quarantine_for_semantic_htri_resync'
    assert 'semantic_mass' in node.cqcl_quantum_variables


def test_phase_bus_report_covers_lns_cards_and_spares() -> None:
    report = phase_bus_report('.', limit=None)
    assert report['schema'] == 'cielingo/htri-phase-bus/v0.1'
    assert report['card_count'] >= 100
    assert report['htri_oscillators'] == 36
    assert report['spare_oscillators'] == max(0, 36 - report['card_count'])
    assert report['orchorbital_snap']['schema'] == 'noema/card-trace-memory/v0.1'
    assert 'phase_locked' in report['lane_counts'] or 'phase_coupled' in report['lane_counts'] or 'phase_tension' in report['lane_counts']
    assert 'throttle_and_rephase_on_htri_bus' in report['bus_actions'] or report['mean_phase_tension'] >= 0
