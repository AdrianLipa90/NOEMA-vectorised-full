# function_type.py — .python_packages/numba/experimental/function_type.py

## Tożsamość
- **id_karty:** `REPO-FUNCTION_TYPE-1D4C`
- **ścieżka:** `.python_packages/numba/experimental/function_type.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.488`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/experimental/function_type.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.488 |
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
Provides Numba type, FunctionType, that makes functions as

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** FunctionProtoModel, FunctionModel
- **funkcje:** `typeof_function_type`, `lower_constant_dispatcher`, `lower_constant_function_type`, `_get_wrapper_address`, `_get_jit_address`, `_lower_get_address`, `unbox_function_type`, `box_function_type`, `lower_cast_function_type_to_function_type`, `lower_cast_dispatcher_to_function_type`

## Opis
Provides Numba type, FunctionType, that makes functions as
instances of a first-class function type.
