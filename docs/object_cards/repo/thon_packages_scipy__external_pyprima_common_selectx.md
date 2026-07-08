# selectx.py — .python_packages/scipy/_external/pyprima/common/selectx.py

## Tożsamość
- **id_karty:** `REPO-SELECTX-3B65`
- **ścieżka:** `.python_packages/scipy/_external/pyprima/common/selectx.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.727`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/_external/pyprima/common/selectx.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.727 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `UNCERTAINTY`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.435049`
- **R₃:** `0.572136`
- **R₆:** `0.544042`
- **R₉:** `0.477522`
- **potencjal_kappa:** `0.159902`
- **masa_semantyczna:** `-0.053674`
- **rodzaj_karty:** `0.279085`


## Rola
This module provides subroutines that ensure the returned X is optimal among all the calculated

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `isbetter`, `savefilt`, `selectx`

## Opis
This module provides subroutines that ensure the returned X is optimal among all the calculated
points in the sense that no other point achieves both lower function value and lower constraint
violation at the same time. This module is needed only in the constrained case.

Translated from Zaikun Zhang's modern-Fortran reference implementation in PRIMA.

Dedicated to late Professor M. J. D. Powell F
