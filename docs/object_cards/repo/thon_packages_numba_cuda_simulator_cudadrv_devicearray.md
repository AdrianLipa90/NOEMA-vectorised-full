# devicearray.py — .python_packages/numba/cuda/simulator/cudadrv/devicearray.py

## Tożsamość
- **id_karty:** `REPO-DEVICEARRAY-296B`
- **ścieżka:** `.python_packages/numba/cuda/simulator/cudadrv/devicearray.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.664`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/cuda/simulator/cudadrv/devicearray.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.664 |
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
The Device Array API is not implemented in the simulator. This module provides

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** FakeShape, FakeWithinKernelCUDAArray, FakeCUDAArray
- **funkcje:** `array_core`, `is_contiguous`, `sentry_contiguous`, `check_array_compatibility`, `to_device`, `pinned`, `mapped_array`, `pinned_array`, `managed_array`, `device_array`, `_contiguous_strides_like_array`, `_order_like_array`, `device_array_like`, `pinned_array_like`, `auto_device`, `is_cuda_ndarray`, `verify_cuda_ndarray_interface`, `require_cuda_ndarray`, `alloc_size`, `nbytes`, `bind`, `T`, `transpose`, `copy_to_host`, `copy_to_device`, `shape`, `ravel`, `reshape`, `view`, `is_c_contiguous`

## Opis
The Device Array API is not implemented in the simulator. This module provides
stubs to allow tests to import correctly.
