# specialize.py — .python_packages/mypyc/irbuild/specialize.py

## Tożsamość
- **id_karty:** `REPO-SPECIALIZE-06DA`
- **ścieżka:** `.python_packages/mypyc/irbuild/specialize.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.718`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/irbuild/specialize.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.718 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MEMORY`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.481637`
- **R₃:** `0.436994`
- **R₆:** `0.50573`
- **R₉:** `0.517955`
- **potencjal_kappa:** `0.179117`
- **masa_semantyczna:** `0.012321`
- **rodzaj_karty:** `0.236997`


## Rola
Special case IR generation of calls to specific builtin functions.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_apply_specialization`, `apply_function_specialization`, `apply_method_specialization`, `specialize_function`, `specialize_dunder`, `apply_dunder_specialization`, `translate_globals`, `translate_builtins_with_unary_dunder`, `translate_len`, `translate_vec_to_list`, `dict_methods_fast_path`, `translate_list_from_generator_call`, `translate_vec_to_tuple`, `translate_tuple_from_generator_call`, `translate_set_from_generator_call`, `faster_min_max`, `translate_safe_generator_call`, `translate_any_call`, `translate_all_call`, `any_all_helper`, `translate_sum_call`, `translate_dataclasses_field_call`, `translate_next_call`, `translate_isinstance`, `translate_dict_setdefault`, `translate_str_format`, `translate_fstring`, `str_encode_fast_path`, `bytes_decode_fast_path`, `translate_i64`

## Opis
Special case IR generation of calls to specific builtin functions.

Most special cases should be handled using the data driven "primitive
ops" system, but certain operations require special handling that has
access to the AST/IR directly and can make decisions/optimizations
based on it. These special cases can be implemented here.

For example, we use specializers to statically emit the length of
