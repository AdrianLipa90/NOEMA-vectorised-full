# test_cython_abi.py — .python_packages/scipy/optimize/tests/test_cython_abi.py

## Tożsamość
- **id_karty:** `REPO-TEST_CYTHON_ABI-ADF3`
- **ścieżka:** `.python_packages/scipy/optimize/tests/test_cython_abi.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.392`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/optimize/tests/test_cython_abi.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.392 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `IDENTITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.405566`
- **R₃:** `0.499333`
- **R₆:** `0.494094`
- **R₉:** `0.455981`
- **potencjal_kappa:** `0.08965`
- **masa_semantyczna:** `-0.024381`
- **rodzaj_karty:** `0.279273`


## Rola
Regression test for the cython_optimize binary interface.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_extract_capi`, `test_cython_optimize_abi_stability`

## Opis
Regression test for the cython_optimize binary interface.

The __pyx_capi__ dict of each module contains PyCapsule objects whose
*name* string encodes the C-level function signature that Cython checks
at import time when another module does ``cimport``.  Any change to
those strings is a binary incompatibility that breaks every downstream
package (e.g., scikit-learn, statsmodels) compiled against t
