# cfunc_cache_usecases.py — .python_packages/numba/tests/cfunc_cache_usecases.py

## Tożsamość
- **id_karty:** `REPO-CFUNC_CACHE_USECASES-3C65`
- **ścieżka:** `.python_packages/numba/tests/cfunc_cache_usecases.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.002`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/tests/cfunc_cache_usecases.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.002 |
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
This file will be copied to a temporary directory in order to

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** _TestModule
- **funkcje:** `add_usecase`, `add_nocache_usecase`, `div_usecase`, `inner`, `outer`, `self_test`, `check_module`

## Opis
This file will be copied to a temporary directory in order to
exercise caching compiled C callbacks.

See test_cfunc.py.
