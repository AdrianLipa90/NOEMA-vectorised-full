# test_nested_calls.py — .python_packages/numba/tests/test_nested_calls.py

## Tożsamość
- **id_karty:** `REPO-TEST_NESTED_CALLS-4378`
- **ścieżka:** `.python_packages/numba/tests/test_nested_calls.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.740`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/tests/test_nested_calls.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.740 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RETURN`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.642878`
- **R₃:** `0.503912`
- **R₆:** `0.555289`
- **R₉:** `0.707983`
- **potencjal_kappa:** `-0.270999`
- **masa_semantyczna:** `-0.074142`
- **rodzaj_karty:** `0.291714`


## Rola
Test problems in nested calls.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestNestedCall
- **funkcje:** `f_inner`, `f`, `g_inner`, `g`, `star_inner`, `star`, `star_call`, `argcast_inner`, `argcast`, `generated_inner`, `ol_generated_inner`, `call_generated`, `nested_annotated`, `inner`, `compile_func`, `test_boolean_return`, `test_named_args`, `test_named_args_objmode`, `test_default_args`, `test_default_args_objmode`, `test_star_args`, `test_star_call`, `test_star_call_objmode`, `test_argcast`, `test_call_generated`, `test_nested_annotated`, `impl`, `impl`, `check`, `inner`

## Opis
Test problems in nested calls.
Usually due to invalid type conversion between function boundaries.
