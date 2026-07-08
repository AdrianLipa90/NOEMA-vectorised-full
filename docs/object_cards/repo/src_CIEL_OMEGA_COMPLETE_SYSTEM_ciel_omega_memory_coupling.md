# coupling.py — src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/coupling.py

## Tożsamość
- **id_karty:** `REPO-COUPLING-1765`
- **ścieżka:** `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/coupling.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.150`
- **φ (phi):** `4.497`
- **masa_semantyczna:** `0.80`

## Kotwice
- `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/coupling.py`

## Atraktor
- **system:** `ciel_omega_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via ciel_omega_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.150 |
| φ | 4.497 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.80 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `ciel_omega_core`.

## PhaseNav
- **operator:** `SCOPE`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.516458`
- **R₃:** `0.452404`
- **R₆:** `0.493743`
- **R₉:** `0.465851`
- **potencjal_kappa:** `0.026123`
- **masa_semantyczna:** `0.147985`
- **rodzaj_karty:** `0.241584`


## Rola
CIEL/Ω Memory Architecture - Coupling Matrix

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem ciel_omega_core*
- **wyjście:** *wywnioskowane z folderu — podsystem ciel_omega_core*

## Zawartość
- **klasy:** CouplingEngine
- **funkcje:** `print_coupling_summary`, `_validate_matrix`, `compute_coupling_force`, `compute_all_coupling_forces`, `get_strongest_couplings`, `analyze_coupling_hierarchy`, `compute_phase_shift_matrix`, `get_default_role_amplitudes`

## Opis
CIEL/Ω Memory Architecture - Coupling Matrix

Defines inter-channel coupling strengths J_kj that govern how memory
channels influence each other. Asymmetric by design: impact of relation
on identity differs from impact of identity on relation.

Copyright (c) 2025 Adrian Lipa / Intention Lab
Licensed under the CIEL Research Non-Commercial License v1.1.
