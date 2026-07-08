# test_ciel_pipeline.py — tests/test_ciel_pipeline.py

## Tożsamość
- **id_karty:** `REPO-TEST_CIEL_PIPELINE-7F07`
- **ścieżka:** `tests/test_ciel_pipeline.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.300`
- **φ (phi):** `3.719`
- **masa_semantyczna:** `0.40`

## Kotwice
- `tests/test_ciel_pipeline.py`

## Atraktor
- **system:** `sync_core`
- **główny_atraktor:** orbital_bridge_core → ent_Mr_Ciel_Apocalyptos

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.300 |
| φ | 3.719 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `sync_core`.

## PhaseNav
- **operator:** `BOUNDARY`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.587016`
- **R₃:** `0.481937`
- **R₆:** `0.525424`
- **R₉:** `0.380572`
- **potencjal_kappa:** `-0.130804`
- **masa_semantyczna:** `0.12548`
- **rodzaj_karty:** `0.280526`


## Rola
Tests for src.ciel_sot_agent.ciel_pipeline.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem sync_core*
- **wyjście:** *wywnioskowane z folderu — podsystem sync_core*

## Zawartość
- **klasy:** —
- **funkcje:** `test_orbital_state_to_context_contains_mode`, `test_orbital_state_to_context_contains_r_h`, `test_orbital_state_to_context_defaults_to_standard_mode`, `test_orbital_state_to_context_contains_chirality`, `test_run_ciel_pipeline_returns_expected_keys`, `test_run_ciel_pipeline_status_ok`, `test_run_ciel_pipeline_mood_in_range`, `test_run_ciel_pipeline_soul_invariant_is_float`, `test_run_ciel_pipeline_ethical_score_non_negative`, `test_run_ciel_pipeline_orbital_context_is_string`, `test_run_ciel_pipeline_uses_bridge_metrics_r_h`, `test_run_ciel_pipeline_uses_recommended_control_mode`, `test_run_ciel_pipeline_accepts_explicit_root`, `test_run_ciel_pipeline_ciel_raw_present`, `test_run_ciel_pipeline_exposes_j_and_memory_projection_keys`, `test_run_ciel_pipeline_exposes_phase_and_qualisensing_snapshots`, `test_run_ciel_pipeline_exposes_cognitive_fragment_and_candidate`, `test_candidate_promotion_and_durable_persistence`, `test_durable_memory_health_forces_reconsolidation_on_low_quality`

## Opis
Tests for src.ciel_sot_agent.ciel_pipeline.
