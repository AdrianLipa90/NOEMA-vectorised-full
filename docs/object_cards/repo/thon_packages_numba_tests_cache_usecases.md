# cache_usecases.py — .python_packages/numba/tests/cache_usecases.py

## Tożsamość
- **id_karty:** `REPO-CACHE_USECASES-ADF8`
- **ścieżka:** `.python_packages/numba/tests/cache_usecases.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `6.040`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/tests/cache_usecases.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 6.040 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `REFUSAL`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.441725`
- **R₃:** `0.537197`
- **R₆:** `0.362678`
- **R₉:** `0.509166`
- **potencjal_kappa:** `0.077364`
- **masa_semantyczna:** `-0.245874`
- **rodzaj_karty:** `0.27107`


## Rola
This file will be copied to a temporary directory in order to

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** _TestModule
- **funkcje:** `simple_usecase`, `simple_usecase_caller`, `add_usecase`, `add_objmode_usecase`, `add_nocache_usecase`, `inner`, `outer`, `outer_uncached`, `looplifted`, `use_c_sin`, `use_c_sin_nest1`, `use_c_sin_nest2`, `ambiguous_function`, `ambiguous_function`, `make_closure`, `use_big_array`, `record_return`, `first_class_function_mul`, `first_class_function_add`, `first_class_function_usecase`, `self_test`, `parfor_usecase`, `closure`, `check_module`

## Opis
This file will be copied to a temporary directory in order to
exercise caching compiled Numba functions.

See test_dispatcher.py.
