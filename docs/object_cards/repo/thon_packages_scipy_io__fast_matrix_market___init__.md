# __init__.py — .python_packages/scipy/io/_fast_matrix_market/__init__.py

## Tożsamość
- **id_karty:** `REPO-__INIT__-B018`
- **ścieżka:** `.python_packages/scipy/io/_fast_matrix_market/__init__.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.188`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/io/_fast_matrix_market/__init__.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.188 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
Matrix Market I/O with a C++ backend.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** _TextToBytesWrapper, _FMMThreadPoolCtlController
- **funkcje:** `_fmm_version`, `_read_body_array`, `_read_body_coo`, `_get_read_cursor`, `_get_write_cursor`, `_apply_field`, `_validate_symmetry`, `mmread`, `mmwrite`, `mminfo`, `_encoding_call`, `read`, `read1`, `peek`, `seek`, `get_num_threads`, `set_num_threads`, `get_version`, `set_additional_attributes`

## Opis
Matrix Market I/O with a C++ backend.
See http://math.nist.gov/MatrixMarket/formats.html
for information about the Matrix Market format.

.. versionadded:: 1.12.0
