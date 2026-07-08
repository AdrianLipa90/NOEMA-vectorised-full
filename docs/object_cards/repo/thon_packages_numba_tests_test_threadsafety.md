# test_threadsafety.py — .python_packages/numba/tests/test_threadsafety.py

## Tożsamość
- **id_karty:** `REPO-TEST_THREADSAFETY-9CEF`
- **ścieżka:** `.python_packages/numba/tests/test_threadsafety.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.915`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/tests/test_threadsafety.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.915 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CAUSE`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.440841`
- **R₃:** `0.698384`
- **R₆:** `0.560357`
- **R₉:** `0.385177`
- **potencjal_kappa:** `0.165796`
- **masa_semantyczna:** `0.077602`
- **rodzaj_karty:** `0.2472`


## Rola
Test threadsafety for compiler.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestThreadSafety
- **funkcje:** `foo`, `ufunc_foo`, `gufunc_foo`, `run_jit`, `run_compile`, `test_concurrent_jit`, `test_concurrent_jit_cache`, `run_vectorize`, `test_concurrent_vectorize`, `test_concurrent_vectorize_cache`, `run_guvectorize`, `test_concurrent_guvectorize`, `test_concurrent_guvectorize_cache`, `test_concurrent_mix_use`, `runner`, `runner`, `runner`, `chooser`

## Opis
Test threadsafety for compiler.
These tests will cause segfault if fail.
