# j_decomposition.py — src/cielingo_core/global_layer/j_decomposition.py

## Tożsamość
- **id_karty:** `REPO-J_DECOMPOSITION-5C67`
- **ścieżka:** `src/cielingo_core/global_layer/j_decomposition.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.685`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/global_layer/j_decomposition.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.685 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SOURCE`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.591319`
- **R₃:** `0.39689`
- **R₆:** `0.568492`
- **R₉:** `0.527911`
- **potencjal_kappa:** `0.015345`
- **masa_semantyczna:** `-0.142691`
- **rodzaj_karty:** `0.266598`


## Rola
GLOBAL 0.5C J decomposition scaffold.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** PhaseBand, JDecomposition
- **funkcje:** `_bounded01`, `classify_phase_band_from_pressure`, `build_j_decomposition`, `total_j`, `validate`, `to_dict`

## Opis
GLOBAL 0.5C J decomposition scaffold.

This module formalizes J as a decomposition of pressures/charges.
It is not a proof engine and never grants SOURCE or canon.
