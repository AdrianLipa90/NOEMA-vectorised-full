# libs.py — .python_packages/numba/cuda/cudadrv/libs.py

## Tożsamość
- **id_karty:** `REPO-LIBS-C6C0`
- **ścieżka:** `.python_packages/numba/cuda/cudadrv/libs.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.866`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/cuda/cudadrv/libs.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.866 |
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
CUDA Toolkit libraries lookup utilities.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `get_libdevice`, `open_libdevice`, `get_cudalib`, `open_cudalib`, `check_static_lib`, `_get_source_variable`, `test`

## Opis
CUDA Toolkit libraries lookup utilities.

CUDA Toolkit libraries can be available via either:

- the `cuda-nvcc` and `cuda-nvrtc` conda packages for CUDA 12,
- the `cudatoolkit` conda package for CUDA 11,
- a user supplied location from CUDA_HOME,
- a system wide location,
- package-specific locations (e.g. the Debian NVIDIA packages),
- or can be discovered by the system loader.
