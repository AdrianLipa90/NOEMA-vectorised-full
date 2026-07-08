# euler_constraint.py — src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/constraints/euler_constraint.py

## Tożsamość
- **id_karty:** `REPO-EULER_CONSTRAINT-E096`
- **ścieżka:** `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/constraints/euler_constraint.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.150`
- **φ (phi):** `4.830`
- **masa_semantyczna:** `0.80`

## Kotwice
- `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/constraints/euler_constraint.py`

## Atraktor
- **system:** `ciel_omega_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via ciel_omega_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.150 |
| φ | 4.830 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.80 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `ciel_omega_core`.

## PhaseNav
- **operator:** `SIMULATION_BOUNDARY`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.575665`
- **R₃:** `0.306554`
- **R₆:** `0.381064`
- **R₉:** `0.528951`
- **potencjal_kappa:** `-0.226686`
- **masa_semantyczna:** `-0.021063`
- **rodzaj_karty:** `0.269599`


## Rola
Unified multi-sector Euler/EBA/semantic closure for CIEL/Ω.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem ciel_omega_core*
- **wyjście:** *wywnioskowane z folderu — podsystem ciel_omega_core*

## Zawartość
- **klasy:** EulerConstraintReport
- **funkcje:** `_wrap`, `_circ_mean`, `_safe_angle_mean`, `_build_core_phase_vector`, `_canonical_id_to_phase`, `_priority_weight`, `_build_vocabulary_phase_vector`, `_build_affect_phase_vector`, `_memory_stats`, `_sector_metrics`, `_pairwise_tension`, `circular_target_phase`, `regulation_strength`, `evaluate_unified_euler_constraint`, `_apply_phase_pull`, `apply_active_euler_feedback`, `as_dict`, `euler_constraint_violation`, `phase_sector`

## Opis
Unified multi-sector Euler/EBA/semantic closure for CIEL/Ω.

This module now supports four phase sectors:
- memory
- core
- vocabulary / semantic
- affect

It also provides active feedback with rollback-safe helpers so the same
constraint can be used both as a metric and as a runtime regulator.
