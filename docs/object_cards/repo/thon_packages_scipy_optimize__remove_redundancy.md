# _remove_redundancy.py — .python_packages/scipy/optimize/_remove_redundancy.py

## Tożsamość
- **id_karty:** `REPO-_REMOVE_REDUNDANCY-D8EA`
- **ścieżka:** `.python_packages/scipy/optimize/_remove_redundancy.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.286`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/optimize/_remove_redundancy.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.286 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CAUSE`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.440841`
- **R₃:** `0.698384`
- **R₆:** `0.560357`
- **R₉:** `0.385177`
- **potencjal_kappa:** `0.165796`
- **masa_semantyczna:** `0.077602`
- **rodzaj_karty:** `0.2472`


## Rola
Routines for removing redundant (linearly dependent) equations from linear

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_row_count`, `_get_densest`, `_remove_zero_rows`, `bg_update_dense`, `_remove_redundancy_pivot_dense`, `_remove_redundancy_pivot_sparse`, `_remove_redundancy_svd`, `_remove_redundancy_id`

## Opis
Routines for removing redundant (linearly dependent) equations from linear
programming equality constraints.
