# callconv.py — .python_packages/numba/core/callconv.py

## Tożsamość
- **id_karty:** `REPO-CALLCONV-E50E`
- **ścieżka:** `.python_packages/numba/core/callconv.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.138`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/core/callconv.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.138 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `FOLD`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.351212`
- **R₃:** `0.661831`
- **R₆:** `0.649218`
- **R₉:** `0.522246`
- **potencjal_kappa:** `-0.135067`
- **masa_semantyczna:** `-0.137397`
- **rodzaj_karty:** `0.29302`


## Rola
Calling conventions for Numba-compiled functions.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** BaseCallConv, MinimalCallConv, _MinimalCallHelper, CPUCallConv, ErrorModel, PythonErrorModel, NumpyErrorModel
- **funkcje:** `_const_int`, `create_error_model`, `return_optional_value`, `return_native_none`, `return_exc`, `return_stop_iteration`, `get_return_type`, `init_call_helper`, `_get_call_helper`, `unpack_exception`, `raise_error`, `decode_arguments`, `_get_arg_packer`, `_make_call_helper`, `return_value`, `return_user_exc`, `return_status_propagate`, `_return_errcode_raw`, `_get_return_status`, `get_function_type`, `decorate_function`, `get_arguments`, `call_function`, `_add_exception`, `get_exception`, `_make_call_helper`, `return_value`, `build_excinfo_struct`, `set_static_user_exc`, `return_user_exc`

## Opis
Calling conventions for Numba-compiled functions.
