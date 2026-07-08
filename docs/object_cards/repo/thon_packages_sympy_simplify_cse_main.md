# cse_main.py — .python_packages/sympy/simplify/cse_main.py

## Tożsamość
- **id_karty:** `REPO-CSE_MAIN-712B`
- **ścieżka:** `.python_packages/sympy/simplify/cse_main.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.046`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/simplify/cse_main.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.046 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `NEGATION`
- **odcisk_harmoniczny:** `LHLL`
- **R₁:** `0.425094`
- **R₃:** `0.614676`
- **R₆:** `0.450577`
- **R₉:** `0.387679`
- **potencjal_kappa:** `0.085998`
- **masa_semantyczna:** `-0.143065`
- **rodzaj_karty:** `0.271614`


## Rola
Tools for doing common subexpression elimination.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** FuncArgTracker, Unevaluated
- **funkcje:** `reps_toposort`, `cse_separate`, `cse_release_variables`, `preprocess_for_cse`, `postprocess_for_cse`, `match_common_args`, `opt_cse`, `tree_cse`, `cse`, `_cse_homogeneous`, `get_args_in_value_order`, `get_or_add_value_number`, `stop_arg_tracking`, `get_common_arg_candidates`, `get_subset_candidates`, `update_func_argset`, `as_unevaluated_basic`, `free_symbols`, `_find_opts`, `_find_repeated`, `_rebuild`

## Opis
Tools for doing common subexpression elimination.
