# driver.py — .python_packages/numba/cuda/cudadrv/driver.py

## Tożsamość
- **id_karty:** `REPO-DRIVER-5187`
- **ścieżka:** `.python_packages/numba/cuda/cudadrv/driver.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.333`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/cuda/cudadrv/driver.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.333 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_OBLIGATION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.59271`
- **R₃:** `0.552945`
- **R₆:** `0.534582`
- **R₉:** `0.582078`
- **potencjal_kappa:** `0.23834`
- **masa_semantyczna:** `-0.091456`
- **rodzaj_karty:** `0.276031`


## Rola
CUDA driver bridge implementation

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** DeadMemoryError, LinkerError, CudaAPIError, Driver, _ActiveContext, Device, BaseCUDAMemoryManager, HostOnlyCUDAMemoryManager, GetIpcHandleMixin, NumbaCUDAMemoryManager, _SizeNotSet, _PendingDeallocs, Context, _CudaIpcImpl, _StagedIpcImpl, IpcHandle, MemoryPointer, AutoFreePointer, MappedMemory, PinnedMemory
- **funkcje:** `make_logger`, `locate_driver_and_loader`, `load_driver`, `find_driver`, `_raise_driver_not_found`, `_raise_driver_error`, `_build_reverse_error_map`, `_getpid`, `_build_reverse_device_attrs`, `met_requirement_for_device`, `_ensure_memory_manager`, `set_memory_manager`, `load_module_image`, `load_module_image_ctypes`, `load_module_image_cuda_python`, `_alloc_finalizer`, `_hostalloc_finalizer`, `_pin_finalizer`, `_event_finalizer`, `_stream_finalizer`, `_module_finalizer`, `event_elapsed_time`, `launch_kernel`, `get_devptr_for_active_ctx`, `device_extents`, `device_memory_size`, `_is_datetime_dtype`, `_workaround_for_datetime`, `host_pointer`, `host_memory_extents`

## Opis
CUDA driver bridge implementation

NOTE:
The new driver implementation uses a *_PendingDeallocs* that help prevents a
crashing the system (particularly OSX) when the CUDA context is corrupted at
resource deallocation.  The old approach ties resource management directly
into the object destructor; thus, at corruption of the CUDA context,
subsequent deallocation could further corrupt the CUDA contex
