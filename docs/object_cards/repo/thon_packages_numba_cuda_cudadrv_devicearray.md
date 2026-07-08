# devicearray.py — .python_packages/numba/cuda/cudadrv/devicearray.py

## Tożsamość
- **id_karty:** `REPO-DEVICEARRAY-FAF0`
- **ścieżka:** `.python_packages/numba/cuda/cudadrv/devicearray.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.873`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/cuda/cudadrv/devicearray.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.873 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CONSENT_REQUIRED`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.458017`
- **R₃:** `0.48995`
- **R₆:** `0.569953`
- **R₉:** `0.575041`
- **potencjal_kappa:** `-0.194917`
- **masa_semantyczna:** `0.103166`
- **rodzaj_karty:** `0.278924`


## Rola
A CUDA ND Array is recognized by checking the __cuda_memory__ attribute

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** DeviceNDArrayBase, DeviceRecord, DeviceNDArray, IpcArrayHandle, MappedNDArray, ManagedNDArray
- **funkcje:** `is_cuda_ndarray`, `verify_cuda_ndarray_interface`, `require_cuda_ndarray`, `_assign_kernel`, `from_array_like`, `from_record_like`, `array_core`, `is_contiguous`, `sentry_contiguous`, `auto_device`, `check_array_compatibility`, `requires_attr`, `bind`, `T`, `transpose`, `_default_stream`, `_numba_type_`, `device_ctypes_pointer`, `copy_to_device`, `copy_to_host`, `split`, `as_cuda_arg`, `get_ipc_handle`, `squeeze`, `view`, `nbytes`, `flags`, `_numba_type_`, `getitem`, `_do_getitem`

## Opis
A CUDA ND Array is recognized by checking the __cuda_memory__ attribute
on the object.  If it exists and evaluate to True, it must define shape,
strides, dtype and size attributes similar to a NumPy ndarray.
