# subexpr.py — .python_packages/mypy/server/subexpr.py

## Tożsamość
- **id_karty:** `REPO-SUBEXPR-F0CC`
- **ścieżka:** `.python_packages/mypy/server/subexpr.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.211`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/server/subexpr.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.211 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `TRANSFORM`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.489274`
- **R₃:** `0.512237`
- **R₆:** `0.547669`
- **R₉:** `0.477906`
- **potencjal_kappa:** `0.124323`
- **masa_semantyczna:** `-0.167832`
- **rodzaj_karty:** `0.281825`


## Rola
Find all subexpressions of an AST node.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** SubexpressionFinder
- **funkcje:** `get_subexpressions`, `visit_int_expr`, `visit_name_expr`, `visit_float_expr`, `visit_str_expr`, `visit_bytes_expr`, `visit_unicode_expr`, `visit_complex_expr`, `visit_ellipsis`, `visit_super_expr`, `visit_type_var_expr`, `visit_type_alias_expr`, `visit_namedtuple_expr`, `visit_typeddict_expr`, `visit__promote_expr`, `visit_newtype_expr`, `visit_member_expr`, `visit_yield_from_expr`, `visit_yield_expr`, `visit_call_expr`, `visit_op_expr`, `visit_comparison_expr`, `visit_slice_expr`, `visit_cast_expr`, `visit_type_form_expr`, `visit_assert_type_expr`, `visit_reveal_expr`, `visit_assignment_expr`, `visit_unary_expr`, `visit_list_expr`

## Opis
Find all subexpressions of an AST node.
