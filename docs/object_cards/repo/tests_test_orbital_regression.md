# test_orbital_regression.py — tests/test_orbital_regression.py

## Tożsamość
- **id_karty:** `REPO-TEST_ORBITAL_REGRESS-A221`
- **ścieżka:** `tests/test_orbital_regression.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.300`
- **φ (phi):** `1.384`
- **masa_semantyczna:** `0.40`

## Kotwice
- `tests/test_orbital_regression.py`

## Atraktor
- **system:** `sync_core`
- **główny_atraktor:** orbital_bridge_core → ent_Mr_Ciel_Apocalyptos

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.300 |
| φ | 1.384 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `sync_core`.

## PhaseNav
- **operator:** `CONSENT`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.382156`
- **R₃:** `0.389068`
- **R₆:** `0.420273`
- **R₉:** `0.412754`
- **potencjal_kappa:** `-0.014557`
- **masa_semantyczna:** `0.231183`
- **rodzaj_karty:** `0.291598`


## Rola
P7 — Orbital Regression Suite + Crash Recovery.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem sync_core*
- **wyjście:** *wywnioskowane z folderu — podsystem sync_core*

## Zawartość
- **klasy:** TestGlobalPassRegression, TestOrbitalBridgeRegression, TestCrashRecoveryMissingFiles, TestCrashRecoveryCorruptedJSON, TestCrashRecoveryEmptyFiles, TestOutputSchemaStability
- **funkcje:** `_finite`, `_in_range`, `test_R_H_final_finite_and_nonnegative`, `test_closure_penalty_final_bounded`, `test_Lambda_glob_final_finite`, `test_closure_penalty_decreases_over_run`, `test_R_H_decreases_over_run`, `test_nonlocal_coherent_fraction_remains_high`, `test_history_length_matches_steps`, `test_history_R_H_monotone_decreasing_early`, `test_coherence_index_in_range`, `test_system_health_in_range`, `test_euler_bridge_closure_score_in_range`, `test_system_health_above_minimum`, `test_mode_is_valid`, `test_schema_version_stable`, `test_bridge_report_files_written`, `test_global_pass_with_fresh_tmp_no_existing_manifests`, `test_bridge_with_missing_summary_json`, `test_bridge_survives_missing_definitions_dir`, `test_ensure_orbital_manifests_idempotent`, `_corrupt`, `test_bridge_survives_corrupted_sectors_global`, `test_bridge_survives_corrupted_couplings_global`, `test_bridge_survives_corrupted_bridge_report`, `test_bridge_survives_empty_summary_json`, `test_global_pass_writes_non_empty_summary`, `test_global_pass_result_has_required_keys`, `test_global_pass_final_has_physics_keys`, `test_bridge_summary_has_required_keys`

## Opis
P7 — Orbital Regression Suite + Crash Recovery.

Checks structural invariants of orbital dynamics rather than fixed numeric
baselines, because berry_phase accumulation across sessions causes natural
drift in R_H, Lambda_glob, and closure_penalty. The regression suite verifies:
  - metrics exist and are finite
  - correct direction of change over 20 steps
  - closure_penalty bounded below 2π (6.283
