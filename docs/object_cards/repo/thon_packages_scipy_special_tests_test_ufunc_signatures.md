# test_ufunc_signatures.py — .python_packages/scipy/special/tests/test_ufunc_signatures.py

## Tożsamość
- **id_karty:** `REPO-TEST_UFUNC_SIGNATURE-792C`
- **ścieżka:** `.python_packages/scipy/special/tests/test_ufunc_signatures.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.234`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/special/tests/test_ufunc_signatures.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.234 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CAUSE`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.440841`
- **R₃:** `0.698384`
- **R₆:** `0.560357`
- **R₉:** `0.385177`
- **potencjal_kappa:** `0.165796`
- **masa_semantyczna:** `0.077602`
- **rodzaj_karty:** `0.2472`


## Rola
Test that all ufuncs have float32-preserving signatures.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `test_ufunc_signatures`, `_get_nan_val`, `test_nep50`

## Opis
Test that all ufuncs have float32-preserving signatures.

This was once guaranteed through the code generation script for
generating ufuncs, `scipy/special/_generate_pyx.py`. Starting with
gh-20260, SciPy developers have begun moving to generate ufuncs
through direct use of the NumPy C API (through C++). Existence of
float32 preserving signatures must now be tested since it is no
longer guaranteed
