# _mio4.py — .python_packages/scipy/io/matlab/_mio4.py

## Tożsamość
- **id_karty:** `REPO-_MIO4-23FB`
- **ścieżka:** `.python_packages/scipy/io/matlab/_mio4.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.436`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/io/matlab/_mio4.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.436 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `UNRUH_DRIVE`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.695214`
- **R₃:** `0.356299`
- **R₆:** `0.471302`
- **R₉:** `0.535169`
- **potencjal_kappa:** `0.138014`
- **masa_semantyczna:** `0.204514`
- **rodzaj_karty:** `0.244249`


## Rola
Classes for read / write of matlab (TM) 4 files

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** VarHeader4, VarReader4, MatFile4Reader, VarWriter4, MatFile4Writer
- **funkcje:** `arr_to_2d`, `read_header`, `array_from_header`, `read_sub_array`, `read_full_array`, `read_char_array`, `read_sparse_array`, `shape_from_header`, `guess_byte_order`, `initialize_read`, `read_var_header`, `read_var_array`, `get_variables`, `list_variables`, `write_bytes`, `write_string`, `write_header`, `write`, `write_numeric`, `write_char`, `write_sparse`, `put_variables`

## Opis
Classes for read / write of matlab (TM) 4 files
