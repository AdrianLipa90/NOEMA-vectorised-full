# rcode.py — .python_packages/sympy/printing/rcode.py

## Tożsamość
- **id_karty:** `REPO-RCODE-D6DE`
- **ścieżka:** `.python_packages/sympy/printing/rcode.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.270`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/printing/rcode.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.270 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RISK`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.594265`
- **R₃:** `0.468144`
- **R₆:** `0.457554`
- **R₉:** `0.414103`
- **potencjal_kappa:** `0.19508`
- **masa_semantyczna:** `-0.03873`
- **rodzaj_karty:** `0.279007`


## Rola
R code printer

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** RCodePrinter
- **funkcje:** `rcode`, `print_rcode`, `_rate_index_position`, `_get_statement`, `_get_comment`, `_declare_number_const`, `_format_code`, `_traverse_matrix_indices`, `_get_loop_opening_ending`, `_print_Pow`, `_print_Rational`, `_print_Indexed`, `_print_Exp1`, `_print_Pi`, `_print_Infinity`, `_print_NegativeInfinity`, `_print_Assignment`, `_print_Piecewise`, `_print_ITE`, `_print_MatrixElement`, `_print_Symbol`, `_print_Relational`, `_print_AugmentedAssignment`, `_print_For`, `indent_code`

## Opis
R code printer

The RCodePrinter converts single SymPy expressions into single R expressions,
using the functions defined in math.h where possible.
