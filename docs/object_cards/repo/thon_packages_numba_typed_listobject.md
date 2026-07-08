# listobject.py — .python_packages/numba/typed/listobject.py

## Tożsamość
- **id_karty:** `REPO-LISTOBJECT-32A8`
- **ścieżka:** `.python_packages/numba/typed/listobject.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.269`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/typed/listobject.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.269 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SCOPE`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.516458`
- **R₃:** `0.452404`
- **R₆:** `0.493743`
- **R₉:** `0.465851`
- **potencjal_kappa:** `0.026123`
- **masa_semantyczna:** `0.147985`
- **rodzaj_karty:** `0.241584`


## Rola
Compiler-side implementation of the Numba  typed-list.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ListModel, ListIterModel, ListStatus, ErrorHandler, ListIterInstance
- **funkcje:** `_check_for_none_typed`, `_as_meminfo`, `_from_meminfo`, `_list_codegen_set_method_table`, `_list_set_method_table`, `list_is`, `_call_list_free`, `_imp_dtor`, `new_list`, `_add_meminfo`, `_make_list`, `_list_new_codegen`, `_list_new`, `impl_new_list`, `impl_len`, `_list_length`, `impl_allocated`, `_list_allocated`, `impl_is_mutable`, `_list_is_mutable`, `impl_make_mutable`, `impl_make_immutable`, `_list_set_is_mutable`, `_list_append`, `impl_append`, `fix_index`, `handle_index`, `handle_slice`, `_gen_getitem`, `impl_getitem`

## Opis
Compiler-side implementation of the Numba  typed-list.
