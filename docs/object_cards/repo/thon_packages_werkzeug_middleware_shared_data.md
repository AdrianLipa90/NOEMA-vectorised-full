# shared_data.py — .python_packages/werkzeug/middleware/shared_data.py

## Tożsamość
- **id_karty:** `REPO-SHARED_DATA-1776`
- **ścieżka:** `.python_packages/werkzeug/middleware/shared_data.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.194`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/werkzeug/middleware/shared_data.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.194 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SOURCE_REQUIRED`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.509375`
- **R₃:** `0.557002`
- **R₆:** `0.453972`
- **R₉:** `0.573802`
- **potencjal_kappa:** `-0.191054`
- **masa_semantyczna:** `-0.307021`
- **rodzaj_karty:** `0.246226`


## Rola
Serve Shared Static Files

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** SharedDataMiddleware
- **funkcje:** `is_allowed`, `_opener`, `get_file_loader`, `get_package_loader`, `get_directory_loader`, `generate_etag`, `loader`, `loader`

## Opis
Serve Shared Static Files
=========================

.. autoclass:: SharedDataMiddleware
    :members: is_allowed

:copyright: 2007 Pallets
:license: BSD-3-Clause
