# fnodes.py — .python_packages/sympy/codegen/fnodes.py

## Tożsamość
- **id_karty:** `REPO-FNODES-E21C`
- **ścieżka:** `.python_packages/sympy/codegen/fnodes.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.275`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/codegen/fnodes.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.275 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `QUESTION`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.394639`
- **R₃:** `0.763677`
- **R₆:** `0.521308`
- **R₉:** `0.466584`
- **potencjal_kappa:** `-0.203086`
- **masa_semantyczna:** `-0.0017`
- **rodzaj_karty:** `0.305584`


## Rola
AST nodes specific to Fortran.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Program, use_rename, use, Module, Subroutine, SubroutineCall, Do, ArrayConstructor, ImpliedDoLoop, Extent, GoTo, FortranReturn, FFunction, F95Function, isign, dsign, cmplx, kind, merge, _literal
- **funkcje:** `_name`, `dimension`, `array`, `_printable`, `allocated`, `lbound`, `ubound`, `shape`, `size`, `reshape`, `bind_C`, `_construct_declarations`, `_construct_body`, `_sympystr`, `_fcode`, `_fcode`

## Opis
AST nodes specific to Fortran.

The functions defined in this module allows the user to express functions such as ``dsign``
as a SymPy function for symbolic manipulation.
