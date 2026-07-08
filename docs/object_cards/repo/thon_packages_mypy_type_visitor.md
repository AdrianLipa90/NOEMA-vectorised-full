# type_visitor.py — .python_packages/mypy/type_visitor.py

## Tożsamość
- **id_karty:** `REPO-TYPE_VISITOR-557D`
- **ścieżka:** `.python_packages/mypy/type_visitor.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.479`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/type_visitor.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.479 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ATTRACTOR`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.476161`
- **R₃:** `0.526498`
- **R₆:** `0.547584`
- **R₉:** `0.472579`
- **potencjal_kappa:** `4.910705`
- **masa_semantyczna:** `13.031004`
- **rodzaj_karty:** `1.5`


## Rola
Type visitor classes.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TypeVisitor, SyntheticTypeVisitor, TypeTranslator, TypeQuery, BoolTypeQuery
- **funkcje:** `visit_unbound_type`, `visit_any`, `visit_none_type`, `visit_uninhabited_type`, `visit_erased_type`, `visit_deleted_type`, `visit_type_var`, `visit_param_spec`, `visit_parameters`, `visit_type_var_tuple`, `visit_instance`, `visit_callable_type`, `visit_overloaded`, `visit_tuple_type`, `visit_typeddict_type`, `visit_literal_type`, `visit_union_type`, `visit_partial_type`, `visit_type_type`, `visit_type_alias_type`, `visit_unpack_type`, `visit_type_list`, `visit_callable_argument`, `visit_ellipsis_type`, `visit_raw_expression_type`, `visit_placeholder_type`, `get_cached`, `set_cached`, `visit_unbound_type`, `visit_any`

## Opis
Type visitor classes.

This module defines the type visitors that are intended to be
subclassed by other code.  They have been separated out into their own
module to ease converting mypy to run under mypyc, since currently
mypyc-extension classes can extend interpreted classes but not the
other way around. Separating them out, then, allows us to compile
types before we can compile everything that
