# _netcdf.py — .python_packages/scipy/io/_netcdf.py

## Tożsamość
- **id_karty:** `REPO-_NETCDF-ACEA`
- **ścieżka:** `.python_packages/scipy/io/_netcdf.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.007`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/io/_netcdf.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.007 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `UNCERTAINTY`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.435049`
- **R₃:** `0.572136`
- **R₆:** `0.544042`
- **R₉:** `0.477522`
- **potencjal_kappa:** `0.159902`
- **masa_semantyczna:** `-0.053674`
- **rodzaj_karty:** `0.279085`


## Rola
NetCDF reader/writer module.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** netcdf_file, netcdf_variable
- **funkcje:** `close`, `createDimension`, `createVariable`, `flush`, `_write`, `_write_numrecs`, `_write_dim_array`, `_write_gatt_array`, `_write_att_array`, `_write_var_array`, `_write_var_metadata`, `_write_var_data`, `_write_var_padding`, `_write_att_values`, `_read`, `_read_numrecs`, `_read_dim_array`, `_read_gatt_array`, `_read_att_array`, `_read_var_array`, `_read_var`, `_read_att_values`, `_pack_begin`, `_pack_int`, `_unpack_int`, `_pack_int64`, `_unpack_int64`, `_pack_string`, `_unpack_string`, `isrec`

## Opis
NetCDF reader/writer module.

This module is used to read and create NetCDF files. NetCDF files are
accessed through the `netcdf_file` object. Data written to and from NetCDF
files are contained in `netcdf_variable` objects. Attributes are given
as member variables of the `netcdf_file` and `netcdf_variable` objects.

This module implements the Scientific.IO.NetCDF API to read and create
NetCDF fil
