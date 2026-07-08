# api.py — .python_packages/mypy/api.py

## Tożsamość
- **id_karty:** `REPO-API-F1B3`
- **ścieżka:** `.python_packages/mypy/api.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.804`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/api.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.804 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ADDITION`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.662589`
- **R₃:** `0.614656`
- **R₆:** `0.542851`
- **R₉:** `0.417608`
- **potencjal_kappa:** `0.07638`
- **masa_semantyczna:** `0.206164`
- **rodzaj_karty:** `0.259027`


## Rola
This module makes it possible to use mypy as part of a Python application.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_run`, `run`, `run_dmypy`, `f`

## Opis
This module makes it possible to use mypy as part of a Python application.

Since mypy still changes, the API was kept utterly simple and non-intrusive.
It just mimics command line activation without starting a new interpreter.
So the normal docs about the mypy command line apply.
Changes in the command line version of mypy will be immediately usable.

Just import this module and then call the 'ru
