# unicode_support.py — .python_packages/numba/cpython/unicode_support.py

## Tożsamość
- **id_karty:** `REPO-UNICODE_SUPPORT-219F`
- **ścieżka:** `.python_packages/numba/cpython/unicode_support.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.264`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/cpython/unicode_support.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.264 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `REFUSAL`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.441725`
- **R₃:** `0.537197`
- **R₆:** `0.362678`
- **R₉:** `0.509166`
- **potencjal_kappa:** `0.077364`
- **masa_semantyczna:** `-0.245874`
- **rodzaj_karty:** `0.27107`


## Rola
This module contains support functions for more advanced unicode operations.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** _PyUnicode_TyperecordMasks, _PY_CTF, _PY_CTF_LB
- **funkcje:** `_PyUnicode_gettyperecord`, `_gettyperecord_impl`, `gettyperecord_impl`, `_PyUnicode_ExtendedCase`, `_PyUnicode_ToTitlecase`, `_PyUnicode_IsTitlecase`, `_PyUnicode_IsXidStart`, `_PyUnicode_IsXidContinue`, `_PyUnicode_ToDecimalDigit`, `_PyUnicode_ToDigit`, `_PyUnicode_IsNumeric`, `_PyUnicode_IsPrintable`, `_PyUnicode_IsLowercase`, `_PyUnicode_IsUppercase`, `_PyUnicode_IsLineBreak`, `_PyUnicode_ToUppercase`, `_PyUnicode_ToLowercase`, `_PyUnicode_ToLowerFull`, `_PyUnicode_ToTitleFull`, `_PyUnicode_ToUpperFull`, `_PyUnicode_ToFoldedFull`, `_PyUnicode_IsCased`, `_PyUnicode_IsCaseIgnorable`, `_PyUnicode_IsDigit`, `_PyUnicode_IsDecimalDigit`, `_PyUnicode_IsSpace`, `_PyUnicode_IsAlpha`, `_Py_CHARMASK`, `_Py_TOUPPER`, `_Py_TOLOWER`

## Opis
This module contains support functions for more advanced unicode operations.
This is not a public API and is for Numba internal use only. Most of the
functions are relatively straightforward translations of the functions with the
same name in CPython.
