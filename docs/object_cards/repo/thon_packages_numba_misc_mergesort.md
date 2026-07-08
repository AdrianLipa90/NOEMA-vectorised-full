# mergesort.py — .python_packages/numba/misc/mergesort.py

## Tożsamość
- **id_karty:** `REPO-MERGESORT-772A`
- **ścieżka:** `.python_packages/numba/misc/mergesort.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.150`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/misc/mergesort.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.150 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
The same algorithm as translated from numpy.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `make_mergesort_impl`, `make_jit_mergesort`, `argmergesort_inner`, `mergesort`, `argmergesort`, `lt`, `lessthan`, `lessthan`

## Opis
The same algorithm as translated from numpy.
See numpy/core/src/npysort/mergesort.c.src.
The high-level numba code is adding a little overhead comparing to
the pure-C implementation in numpy.
