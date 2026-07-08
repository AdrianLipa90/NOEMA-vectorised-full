# _mio5.py — .python_packages/scipy/io/matlab/_mio5.py

## Tożsamość
- **id_karty:** `REPO-_MIO5-0CC5`
- **ścieżka:** `.python_packages/scipy/io/matlab/_mio5.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.243`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/io/matlab/_mio5.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.243 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `TRANSFORM`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.489274`
- **R₃:** `0.512237`
- **R₆:** `0.547669`
- **R₉:** `0.477906`
- **potencjal_kappa:** `0.124323`
- **masa_semantyczna:** `-0.167832`
- **rodzaj_karty:** `0.281825`


## Rola
Classes for read / write of matlab (TM) 5 files

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** MatFile5Reader, EmptyStructMarker, VarWriter5, MatFile5Writer
- **funkcje:** `_has_struct`, `_inspect_cell_array`, `_matstruct_to_dict`, `_simplify_cells`, `varmats_from_mat`, `to_writeable`, `guess_byte_order`, `read_file_header`, `initialize_read`, `read_var_header`, `read_var_array`, `get_variables`, `list_variables`, `write_bytes`, `write_string`, `write_element`, `write_smalldata_element`, `write_regular_element`, `write_header`, `update_matrix_tag`, `write_top`, `write`, `write_numeric`, `write_char`, `write_sparse`, `write_cells`, `write_empty_struct`, `write_struct`, `_write_items`, `write_object`

## Opis
Classes for read / write of matlab (TM) 5 files

The matfile specification last found here:

https://www.mathworks.com/access/helpdesk/help/pdf_doc/matlab/matfile_format.pdf

(as of December 5 2008)

=================================
 Note on functions and mat files
=================================

The document above does not give any hints as to the storage of matlab
function handles, or anonym
