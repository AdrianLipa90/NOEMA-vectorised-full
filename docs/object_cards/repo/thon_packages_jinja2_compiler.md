# compiler.py — .python_packages/jinja2/compiler.py

## Tożsamość
- **id_karty:** `REPO-COMPILER-52CD`
- **ścieżka:** `.python_packages/jinja2/compiler.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.731`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/jinja2/compiler.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.731 |
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
Compiles nodes from the parser into Python code.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** MacroRef, Frame, VisitorExit, DependencyFinderVisitor, UndeclaredNameVisitor, CompilerExit, CodeGenerator, _FinalizeInfo
- **funkcje:** `optimizeconst`, `_make_binop`, `_make_unop`, `generate`, `has_safe_repr`, `find_undeclared`, `new_func`, `visitor`, `visitor`, `copy`, `inner`, `soft`, `visit_Filter`, `visit_Test`, `visit_Block`, `visit_Name`, `visit_Block`, `optimized`, `fail`, `temporary_identifier`, `buffer`, `return_buffer_contents`, `indent`, `outdent`, `start_write`, `end_write`, `simple_write`, `blockvisit`, `write`, `writeline`

## Opis
Compiles nodes from the parser into Python code.
