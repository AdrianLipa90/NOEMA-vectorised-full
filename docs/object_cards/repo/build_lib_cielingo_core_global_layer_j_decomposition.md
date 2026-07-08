# j_decomposition.py — build/lib/cielingo_core/global_layer/j_decomposition.py

## Tożsamość
- **id_karty:** `REPO-J_DECOMPOSITION-54B5`
- **ścieżka:** `build/lib/cielingo_core/global_layer/j_decomposition.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.229`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo_core/global_layer/j_decomposition.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.229 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ASSERTION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.563342`
- **R₃:** `0.601856`
- **R₆:** `0.54039`
- **R₉:** `0.584219`
- **potencjal_kappa:** `-0.098441`
- **masa_semantyczna:** `0.347732`
- **rodzaj_karty:** `0.261593`


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
