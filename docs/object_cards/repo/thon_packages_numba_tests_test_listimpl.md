# test_listimpl.py — .python_packages/numba/tests/test_listimpl.py

## Tożsamość
- **id_karty:** `REPO-TEST_LISTIMPL-16E0`
- **ścieżka:** `.python_packages/numba/tests/test_listimpl.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.042`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/tests/test_listimpl.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.042 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `QUESTION`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.394639`
- **R₃:** `0.763677`
- **R₆:** `0.521308`
- **R₉:** `0.466584`
- **potencjal_kappa:** `-0.203086`
- **masa_semantyczna:** `-0.0017`
- **rodzaj_karty:** `0.305584`


## Rola
Testing C implementation of the numba typed-list

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** List, ListIter, TestListImpl
- **funkcje:** `handle_index`, `allocated`, `is_mutable`, `set_mutable`, `set_immutable`, `append`, `pop`, `list_new`, `list_length`, `list_allocated`, `list_is_mutable`, `list_set_is_mutable`, `list_setitem`, `list_getitem`, `list_append`, `list_pop`, `list_delitem`, `list_iter`, `list_iter_next`, `setUp`, `test_simple_c_test`, `test_length`, `test_allocation`, `test_append_get_string`, `test_append_get_int`, `test_append_get_string_realloc`, `test_set_item_getitem_index_error`, `test_iter`, `test_pop`, `test_pop_index_error`

## Opis
Testing C implementation of the numba typed-list
