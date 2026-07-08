# testsolve.py — .python_packages/mypy/test/testsolve.py

## Tożsamość
- **id_karty:** `REPO-TESTSOLVE-D59A`
- **ścieżka:** `.python_packages/mypy/test/testsolve.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.629`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/test/testsolve.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.629 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ASSERTION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.563342`
- **R₃:** `0.601856`
- **R₆:** `0.54039`
- **R₉:** `0.584219`
- **potencjal_kappa:** `-0.098441`
- **masa_semantyczna:** `0.347732`
- **rodzaj_karty:** `0.261593`


## Rola
Test cases for the constraint solver used in type inference.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** SolveSuite
- **funkcje:** `setUp`, `test_empty_input`, `test_simple_supertype_constraints`, `test_simple_subtype_constraints`, `test_both_kinds_of_constraints`, `test_unsatisfiable_constraints`, `test_exactly_specified_result`, `test_multiple_variables`, `test_no_constraints_for_var`, `test_simple_constraints_with_dynamic_type`, `test_both_normal_and_any_types_in_results`, `test_poly_no_constraints`, `test_poly_trivial_free`, `test_poly_free_pair`, `test_poly_free_pair_with_bounds`, `test_poly_free_pair_with_bounds_uninhabited`, `test_poly_bounded_chain`, `test_poly_reverse_overlapping_chain`, `test_poly_reverse_split_chain`, `test_poly_unsolvable_chain`, `test_simple_chain_closure`, `test_reverse_chain_closure`, `test_secondary_constraint_closure`, `assert_solve`, `assert_transitive_closure`, `supc`, `subc`

## Opis
Test cases for the constraint solver used in type inference.
