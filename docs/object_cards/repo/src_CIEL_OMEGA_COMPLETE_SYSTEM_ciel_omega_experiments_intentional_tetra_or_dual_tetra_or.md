# dual_tetra_or.py — src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/experiments/intentional_tetra_or/dual_tetra_or.py

## Tożsamość
- **id_karty:** `REPO-DUAL_TETRA_OR-92A2`
- **ścieżka:** `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/experiments/intentional_tetra_or/dual_tetra_or.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.150`
- **φ (phi):** `3.383`
- **masa_semantyczna:** `0.80`

## Kotwice
- `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/experiments/intentional_tetra_or/dual_tetra_or.py`

## Atraktor
- **system:** `ciel_omega_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via ciel_omega_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.150 |
| φ | 3.383 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.80 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `ciel_omega_core`.

## PhaseNav
- **operator:** `DIFFERENCE`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.563622`
- **R₃:** `0.51399`
- **R₆:** `0.516024`
- **R₉:** `0.447233`
- **potencjal_kappa:** `-0.196591`
- **masa_semantyczna:** `-0.06476`
- **rodzaj_karty:** `0.313562`


## Rola
CIEL/Ω — Intentional Dual-Tetrahedral Orch-OR

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem ciel_omega_core*
- **wyjście:** *wywnioskowane z folderu — podsystem ciel_omega_core*

## Zawartość
- **klasy:** IntentionalScenario
- **funkcje:** `normalize_rows`, `tetra_defect`, `centroid_defect`, `alignment_cost_dual`, `alignment_cost_same`, `mean_antipodal`, `stella_quality`, `tangent_project`, `grad_tetra_defect`, `grad_alignment_dual`, `grad_alignment_same`, `total_potential`, `sigmoid`, `build_intention_state`, `step_tetra`, `run_intentional_tetra_or`, `sweep_truth`, `demo`

## Opis
CIEL/Ω — Intentional Dual-Tetrahedral Orch-OR
===============================================
Dwa dualne tetrahedry (stella octangula):
  U = TETRA_A (biegun Adrian)
  V = TETRA_C = −TETRA_A (biegun Ciel)

Alignment cost ciągnie V ku DUALOWI U, nie ku U.
Docelowa konfiguracja: U_i · V_i = −1 (antypody).

CIEL integration:
  IntentionField (12D) → I scalar
  PhaseInfoSystem → R_H, A_ZS
  I, R_H, A_
