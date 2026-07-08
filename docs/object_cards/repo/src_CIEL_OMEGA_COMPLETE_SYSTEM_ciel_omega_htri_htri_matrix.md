# htri_matrix.py — src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/htri/htri_matrix.py

## Tożsamość
- **id_karty:** `REPO-HTRI_MATRIX-8147`
- **ścieżka:** `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/htri/htri_matrix.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.150`
- **φ (phi):** `3.411`
- **masa_semantyczna:** `0.80`

## Kotwice
- `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/htri/htri_matrix.py`

## Atraktor
- **system:** `ciel_omega_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via ciel_omega_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.150 |
| φ | 3.411 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.80 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `ciel_omega_core`.

## PhaseNav
- **operator:** `MODAL_OBLIGATION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.59271`
- **R₃:** `0.552945`
- **R₆:** `0.534582`
- **R₉:** `0.582078`
- **potencjal_kappa:** `0.23834`
- **masa_semantyczna:** `-0.091456`
- **rodzaj_karty:** `0.276031`


## Rola
HTRI vectorized phase networks.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem ciel_omega_core*
- **wyjście:** *wywnioskowane z folderu — podsystem ciel_omega_core*

## Zawartość
- **klasy:** DensePhaseNetwork
- **funkcje:** `plo_frequencies`, `build_all_to_all_matrix`, `build_ring_matrix`, `build_grid_matrix`, `_build_matrix`, `phase_differences`, `phase_kernel`, `coupling_field`, `external_field`, `potential_matrix`, `potential_energy`, `order_parameter`, `laplacian`, `spectral_radius`, `step`, `run`, `snapshot`

## Opis
HTRI vectorized phase networks.

This module upgrades the local HTRI model from scalar Kuramoto-style updates
into a dense matrix formulation with explicit potential, field, and spectral
observables. The implementation is intentionally classical: dense phase-space
math, not quantum dynamics.
