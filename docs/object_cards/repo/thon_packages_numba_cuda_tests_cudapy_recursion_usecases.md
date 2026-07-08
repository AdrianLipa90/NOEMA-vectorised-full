# recursion_usecases.py — .python_packages/numba/cuda/tests/cudapy/recursion_usecases.py

## Tożsamość
- **id_karty:** `REPO-RECURSION_USECASES-B6BA`
- **ścieżka:** `.python_packages/numba/cuda/tests/cudapy/recursion_usecases.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.597`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/cuda/tests/cudapy/recursion_usecases.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.597 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ADDITION`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.662589`
- **R₃:** `0.614656`
- **R₆:** `0.542851`
- **R₉:** `0.417608`
- **potencjal_kappa:** `0.07638`
- **masa_semantyczna:** `0.206164`
- **rodzaj_karty:** `0.259027`


## Rola
Usecases of recursive functions in the CUDA target, many derived from

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `fib1`, `make_fib2`, `type_change_self`, `fib3`, `runaway_self`, `raise_self`, `raise_self_kernel`, `make_optional_return_case`, `make_growing_tuple_case`, `fib2`, `foo`, `bar`, `make_list`

## Opis
Usecases of recursive functions in the CUDA target, many derived from
numba/tests/recursion_usecases.py.

Some functions are compiled at import time, hence a separate module.
