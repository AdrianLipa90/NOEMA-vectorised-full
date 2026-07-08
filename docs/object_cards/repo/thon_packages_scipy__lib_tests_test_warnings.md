# test_warnings.py — .python_packages/scipy/_lib/tests/test_warnings.py

## Tożsamość
- **id_karty:** `REPO-TEST_WARNINGS-9946`
- **ścieżka:** `.python_packages/scipy/_lib/tests/test_warnings.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.808`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/_lib/tests/test_warnings.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.808 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CONDITION`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.577442`
- **R₃:** `0.440978`
- **R₆:** `0.50908`
- **R₉:** `0.325439`
- **potencjal_kappa:** `-0.091854`
- **masa_semantyczna:** `-0.064427`
- **rodzaj_karty:** `0.305875`


## Rola
Tests which scan for certain occurrences in the code, they may not find

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ParseCall, FindFuncs
- **funkcje:** `warning_calls`, `test_warning_calls_filters`, `visit_Attribute`, `visit_Name`, `visit_Call`

## Opis
Tests which scan for certain occurrences in the code, they may not find
all of these occurrences but should catch almost all. This file was adapted
from NumPy.
