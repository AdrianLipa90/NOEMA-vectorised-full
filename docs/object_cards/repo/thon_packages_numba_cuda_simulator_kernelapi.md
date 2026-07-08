# kernelapi.py — .python_packages/numba/cuda/simulator/kernelapi.py

## Tożsamość
- **id_karty:** `REPO-KERNELAPI-5080`
- **ścieżka:** `.python_packages/numba/cuda/simulator/kernelapi.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.665`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/cuda/simulator/kernelapi.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.665 |
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
Implements the cuda module as called from within an executing kernel

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Dim3, GridGroup, FakeCUDACg, FakeCUDALocal, FakeCUDAConst, FakeCUDAShared, FakeCUDAAtomic, FakeCUDAFp16, FakeCUDAModule
- **funkcje:** `swapped_cuda_module`, `sync`, `this_grid`, `array`, `array_like`, `array`, `add`, `sub`, `and_`, `or_`, `xor`, `inc`, `dec`, `exch`, `max`, `min`, `nanmax`, `nanmin`, `compare_and_swap`, `cas`, `hadd`, `hsub`, `hmul`, `hdiv`, `hfma`, `hneg`, `habs`, `hsin`, `hcos`, `hlog`

## Opis
Implements the cuda module as called from within an executing kernel
(@cuda.jit-decorated function).
