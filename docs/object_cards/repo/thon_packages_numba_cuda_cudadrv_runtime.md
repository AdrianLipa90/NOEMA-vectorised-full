# runtime.py — .python_packages/numba/cuda/cudadrv/runtime.py

## Tożsamość
- **id_karty:** `REPO-RUNTIME-86BD`
- **ścieżka:** `.python_packages/numba/cuda/cudadrv/runtime.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.086`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/cuda/cudadrv/runtime.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.086 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `IDENTITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.405566`
- **R₃:** `0.499333`
- **R₆:** `0.494094`
- **R₉:** `0.455981`
- **potencjal_kappa:** `0.08965`
- **masa_semantyczna:** `-0.024381`
- **rodzaj_karty:** `0.279273`


## Rola
CUDA Runtime wrapper.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** CudaRuntimeAPIError, Runtime
- **funkcje:** `get_version`, `_initialize`, `_wrap_api_call`, `_check_error`, `_find_api`, `get_version`, `is_supported_version`, `supported_versions`, `safe_cuda_api_call`, `absent_function`

## Opis
CUDA Runtime wrapper.

This provides a very minimal set of bindings, since the Runtime API is not
really used in Numba except for querying the Runtime version.
