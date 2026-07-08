# suggestions.py — .python_packages/mypy/suggestions.py

## Tożsamość
- **id_karty:** `REPO-SUGGESTIONS-6436`
- **ścieżka:** `.python_packages/mypy/suggestions.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.661`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/suggestions.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.661 |
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
Mechanisms for inferring function types based on callsites.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** PyAnnotateSignature, Callsite, SuggestionPlugin, ReturnFinder, ArgUseFinder, SuggestionFailure, SuggestionEngine, TypeFormatter, MakeSuggestionAny
- **funkcje:** `get_return_types`, `get_arg_uses`, `is_explicit_any`, `is_implicit_any`, `_arg_accepts_function`, `any_score_type`, `any_score_callable`, `is_tricky_callable`, `make_suggestion_anys`, `generate_type_combinations`, `count_errors`, `refine_type`, `refine_union`, `refine_callable`, `dedup`, `get_function_hook`, `get_method_hook`, `log`, `visit_return_stmt`, `visit_func_def`, `visit_call_expr`, `suggest`, `suggest_callsites`, `restore_after`, `with_export_types`, `get_trivial_type`, `get_starting_type`, `get_args`, `get_default_arg_types`, `get_guesses`

## Opis
Mechanisms for inferring function types based on callsites.

Currently works by collecting all argument types at callsites,
synthesizing a list of possible function types from that, trying them
all, and picking the one with the fewest errors that we think is the
"best".

Can return JSON that pyannotate can use to apply the annotations to code.

There are a bunch of TODOs here:
 * Maybe want a way
