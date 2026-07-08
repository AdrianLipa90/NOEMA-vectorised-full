# repr.py — .python_packages/sympy/printing/repr.py

## Tożsamość
- **id_karty:** `REPO-REPR-50AD`
- **ścieżka:** `.python_packages/sympy/printing/repr.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.488`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/printing/repr.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.488 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SOURCE_REQUIRED`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.509375`
- **R₃:** `0.557002`
- **R₆:** `0.453972`
- **R₉:** `0.573802`
- **potencjal_kappa:** `-0.191054`
- **masa_semantyczna:** `-0.307021`
- **rodzaj_karty:** `0.246226`


## Rola
A Printer for generating executable code.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ReprPrinter
- **funkcje:** `srepr`, `reprify`, `emptyPrinter`, `_print_Add`, `_print_Cycle`, `_print_Permutation`, `_print_Function`, `_print_Heaviside`, `_print_FunctionClass`, `_print_Half`, `_print_RationalConstant`, `_print_AtomicExpr`, `_print_NumberSymbol`, `_print_Integer`, `_print_Complexes`, `_print_Integers`, `_print_Naturals`, `_print_Naturals0`, `_print_Rationals`, `_print_Reals`, `_print_EmptySet`, `_print_UniversalSet`, `_print_EmptySequence`, `_print_list`, `_print_dict`, `_print_set`, `_print_MatrixBase`, `_print_BooleanTrue`, `_print_BooleanFalse`, `_print_NaN`

## Opis
A Printer for generating executable code.

The most important function here is srepr that returns a string so that the
relation eval(srepr(expr))=expr holds in an appropriate environment.
