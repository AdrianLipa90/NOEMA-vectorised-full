# deviceufunc.py — .python_packages/numba/cuda/deviceufunc.py

## Tożsamość
- **id_karty:** `REPO-DEVICEUFUNC-33AE`
- **ścieżka:** `.python_packages/numba/cuda/deviceufunc.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.924`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/cuda/deviceufunc.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.924 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CANON_BLOCK`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.593927`
- **R₃:** `0.544645`
- **R₆:** `0.483246`
- **R₉:** `0.501272`
- **potencjal_kappa:** `0.159378`
- **masa_semantyczna:** `-0.256779`
- **rodzaj_karty:** `0.332318`


## Rola
Implements custom ufunc dispatch mechanism for non-CPU devices.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** UFuncMechanism, DeviceVectorize, DeviceGUFuncVectorize, GUFuncEngine, GUFuncSchedule, GeneralizedUFunc, GUFuncCallSteps
- **funkcje:** `_broadcast_axis`, `_pairwise_broadcast`, `_multi_broadcast`, `to_dtype`, `_determine_gufunc_outer_types`, `expand_gufunc_template`, `_gen_src_for_indexing`, `_gen_src_index`, `_fill_arrays`, `_fill_argtypes`, `_resolve_signature`, `_get_actual_args`, `_broadcast`, `get_arguments`, `get_function`, `is_device_array`, `as_device_array`, `broadcast_device`, `force_array_layout`, `call`, `to_device`, `to_host`, `allocate_device_array`, `launch`, `pyfunc`, `add`, `build_ufunc`, `_get_kernel_source`, `_compile_core`, `_get_globals`

## Opis
Implements custom ufunc dispatch mechanism for non-CPU devices.
