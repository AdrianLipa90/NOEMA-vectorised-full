# _odrpack.py — .python_packages/scipy/odr/_odrpack.py

## Tożsamość
- **id_karty:** `REPO-_ODRPACK-1CD4`
- **ścieżka:** `.python_packages/scipy/odr/_odrpack.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.552`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/odr/_odrpack.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.552 |
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
Python wrappers for Orthogonal Distance Regression (ODRPACK).

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** OdrWarning, OdrError, OdrStop, Data, RealData, Model, Output, ODR
- **funkcje:** `_conv`, `_report_error`, `set_meta`, `_sd2wt`, `_cov2wt`, `set_meta`, `pprint`, `_check`, `_gen_work`, `set_job`, `set_iprint`, `run`, `restart`

## Opis
Python wrappers for Orthogonal Distance Regression (ODRPACK).

Notes
=====

* Array formats -- FORTRAN stores its arrays in memory column first, i.e., an
  array element A(i, j, k) will be next to A(i+1, j, k). In C and, consequently,
  NumPy, arrays are stored row first: A[i, j, k] is next to A[i, j, k+1]. For
  efficiency and convenience, the input and output arrays of the fitting
  function (an
