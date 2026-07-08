# devices.py — .python_packages/numba/cuda/cudadrv/devices.py

## Tożsamość
- **id_karty:** `REPO-DEVICES-1000`
- **ścieżka:** `.python_packages/numba/cuda/cudadrv/devices.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.348`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/cuda/cudadrv/devices.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.348 |
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
Expose each GPU devices directly.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** _DeviceList, _DeviceContextManager, _Runtime
- **funkcje:** `get_context`, `require_context`, `reset`, `current`, `ensure_context`, `get_or_create_context`, `_get_or_create_context_uncached`, `_activate_context_for`, `_get_attached_context`, `_set_attached_context`, `reset`, `_destroy_all_contexts`, `_require_cuda_context`

## Opis
Expose each GPU devices directly.

This module implements a API that is like the "CUDA runtime" context manager
for managing CUDA context stack and clean up.  It relies on thread-local globals
to separate the context stack management of each thread. Contexts are also
shareable among threads.  Only the main thread can destroy Contexts.

Note:
- This module must be imported by the main-thread.
