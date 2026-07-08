# test_module_imports.py — .python_packages/sympy/testing/tests/test_module_imports.py

## Tożsamość
- **id_karty:** `REPO-TEST_MODULE_IMPORTS-0131`
- **ścieżka:** `.python_packages/sympy/testing/tests/test_module_imports.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.648`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/testing/tests/test_module_imports.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.648 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RETURN`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.642878`
- **R₃:** `0.503912`
- **R₆:** `0.555289`
- **R₉:** `0.707983`
- **potencjal_kappa:** `-0.270999`
- **masa_semantyczna:** `-0.074142`
- **rodzaj_karty:** `0.291714`


## Rola
Checks that SymPy does not contain indirect imports.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `test_module_imports_are_direct`

## Opis
Checks that SymPy does not contain indirect imports.

An indirect import is importing a symbol from a module that itself imported the
symbol from elsewhere. Such a constellation makes it harder to diagnose
inter-module dependencies and import order problems, and is therefore strongly
discouraged.

(Indirect imports from end-user code is fine and in fact a best practice.)

Implementation note: Forc
