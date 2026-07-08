from __future__ import annotations

from cielingo.collatz_semantic_htri_sync import DEFAULT_OSCILLATORS
from cielingo.infinitive_modal_potential import (
    KAPPA_INFO,
    infinitive_modal_report,
    load_infinitive_seeds,
    load_modality_seeds,
    map_infinitive_to_modalities,
)


def test_infinitive_seeds_are_loaded_from_noema_and_polish_surface() -> None:
    seeds = load_infinitive_seeds('.')
    labels = {s.infinitive for s in seeds}
    assert {'mieć', 'widzieć', 'dać'}.issubset(labels)
    assert 'być' in labels
    for seed in seeds:
        assert seed.rest_semantic_mass >= 0
        assert seed.potential_phi == round(seed.rest_semantic_mass * KAPPA_INFO, 12)
        assert seed.collatz_seed > 0
        assert 0 <= seed.htri_oscillator_id < DEFAULT_OSCILLATORS


def test_modalities_have_information_potential() -> None:
    modalities = load_modality_seeds()
    assert len(modalities) >= 8
    families = {m.family for m in modalities}
    assert {'epistemic', 'deontic', 'dynamic', 'volitional'}.issubset(families)
    for mod in modalities:
        assert mod.potential_phi == round(mod.rest_semantic_mass * KAPPA_INFO, 12)
        assert mod.polish_markers


def test_infinitive_maps_to_modalities_with_nbody_energy() -> None:
    seed = next(s for s in load_infinitive_seeds('.') if s.infinitive == 'mieć')
    mappings = map_infinitive_to_modalities(seed, load_modality_seeds())
    assert mappings
    assert {m.modality_id for m in mappings}
    for mapping in mappings:
        assert mapping.infinitive == 'mieć'
        assert 0 <= mapping.affinity <= 1
        assert mapping.semantic_distance >= 0
        assert mapping.nbody_binding_energy >= 0
        assert mapping.lagrangian_potential_U <= 0
        assert mapping.kepler_period_proxy > 0
        assert mapping.recommended_lane in {
            'modal_phase_locked',
            'modal_bound_orbit',
            'modal_rephase_needed',
            'modal_observe',
        }


def test_infinitive_modal_report_is_noema_ready() -> None:
    report = infinitive_modal_report('.')
    assert report['schema'] == 'cielingo/infinitive-modal-potential/v0.1'
    assert report['infinitive_count'] >= 4
    assert report['modality_count'] >= 8
    assert report['mapping_count'] == report['infinitive_count'] * report['modality_count']
    assert report['total_nbody_binding_energy'] >= 0
    assert report['lane_counts']
