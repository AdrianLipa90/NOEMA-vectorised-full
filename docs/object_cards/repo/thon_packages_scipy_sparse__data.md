# _data.py — .python_packages/scipy/sparse/_data.py

## Tożsamość
- **id_karty:** `REPO-_DATA-E87B`
- **ścieżka:** `.python_packages/scipy/sparse/_data.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.586`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/sparse/_data.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.586 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
Base class for sparse matrice with a .data attribute

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** _data_matrix, _minmax_mixin
- **funkcje:** `_find_missing_index`, `dtype`, `dtype`, `_deduped_data`, `_real`, `_imag`, `astype`, `conjugate`, `copy`, `power`, `_mul_scalar`, `_create_method`, `_min_or_max_axis`, `_min_or_max`, `_argminmax_axis`, `_argminmax`, `max`, `min`, `nanmax`, `nanmin`, `argmax`, `argmin`, `method`

## Opis
Base class for sparse matrice with a .data attribute

subclasses must provide a _with_data() method that
creates a new matrix with the same sparsity pattern
as self but with a different data array
