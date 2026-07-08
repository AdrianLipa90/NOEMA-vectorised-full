# _project.py — .python_packages/scipy/_external/pyprima/common/_project.py

## Tożsamość
- **id_karty:** `REPO-_PROJECT-BCD2`
- **ścieżka:** `.python_packages/scipy/_external/pyprima/common/_project.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.334`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/_external/pyprima/common/_project.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.334 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `FORCE`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.552175`
- **R₃:** `0.435218`
- **R₆:** `0.571397`
- **R₉:** `0.579087`
- **potencjal_kappa:** `0.300939`
- **masa_semantyczna:** `0.016845`
- **rodzaj_karty:** `0.260112`


## Rola
This module provides the _project function that attempts to project the initial guess

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_project`

## Opis
This module provides the _project function that attempts to project the initial guess
onto the feasible set.

Adapted from the corresponding function in the PDFO package (https://www.pdfo.net) by
Tom M. Ragonneau (https://ragonneau.github.io) and Zaikun Zhang (https://www.zhangzk.net).
