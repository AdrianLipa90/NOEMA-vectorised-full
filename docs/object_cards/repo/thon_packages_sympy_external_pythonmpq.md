# pythonmpq.py — .python_packages/sympy/external/pythonmpq.py

## Tożsamość
- **id_karty:** `REPO-PYTHONMPQ-E93B`
- **ścieżka:** `.python_packages/sympy/external/pythonmpq.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.250`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/external/pythonmpq.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.250 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_PERMISSION`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.453718`
- **R₃:** `0.541785`
- **R₆:** `0.466054`
- **R₉:** `0.529069`
- **potencjal_kappa:** `0.025212`
- **masa_semantyczna:** `0.161862`
- **rodzaj_karty:** `0.285369`


## Rola
PythonMPQ: Rational number type based on Python integers.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** PythonMPQ
- **funkcje:** `_new_check`, `_new`, `_cmp`

## Opis
PythonMPQ: Rational number type based on Python integers.

This class is intended as a pure Python fallback for when gmpy2 is not
installed. If gmpy2 is installed then its mpq type will be used instead. The
mpq type is around 20x faster. We could just use the stdlib Fraction class
here but that is slower:

    from fractions import Fraction
    from sympy.external.pythonmpq import PythonMPQ
    nu
