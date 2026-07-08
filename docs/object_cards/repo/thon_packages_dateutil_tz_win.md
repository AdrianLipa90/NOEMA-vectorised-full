# win.py — .python_packages/dateutil/tz/win.py

## Tożsamość
- **id_karty:** `REPO-WIN-62A8`
- **ścieżka:** `.python_packages/dateutil/tz/win.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.196`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/dateutil/tz/win.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.196 |
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
This module provides an interface to the native time zone data on Windows,

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** tzres, tzwinbase, tzwin, tzwinlocal
- **funkcje:** `_settzkeyname`, `picknthweekday`, `valuestodict`, `load_name`, `name_from_string`, `list`, `display`, `transitions`, `_get_hasdst`, `_dst_base_offset`

## Opis
This module provides an interface to the native time zone data on Windows,
including :py:class:`datetime.tzinfo` implementations.

Attempting to import this module on a non-Windows platform will raise an
:py:obj:`ImportError`.
