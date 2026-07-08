# structref.py — .python_packages/numba/experimental/structref.py

## Tożsamość
- **id_karty:** `REPO-STRUCTREF-B7E9`
- **ścieżka:** `.python_packages/numba/experimental/structref.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.968`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/experimental/structref.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.968 |
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
Utilities for defining a mutable struct.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** _Utils, StructRefProxy, StructAttribute
- **funkcje:** `define_attributes`, `define_boxing`, `define_constructor`, `define_proxy`, `register`, `new`, `structref_is`, `new_struct_ref`, `get_struct_ref`, `get_data_pointer`, `get_data_struct`, `struct_getattr_impl`, `struct_setattr_impl`, `box_struct_ref`, `unbox_struct_ref`, `codegen`, `_numba_box_`, `_numba_type_`, `generic_resolve`, `ctor`

## Opis
Utilities for defining a mutable struct.

A mutable struct is passed by reference;
hence, structref (a reference to a struct).
