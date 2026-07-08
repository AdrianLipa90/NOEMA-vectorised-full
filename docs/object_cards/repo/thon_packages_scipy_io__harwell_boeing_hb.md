# hb.py — .python_packages/scipy/io/_harwell_boeing/hb.py

## Tożsamość
- **id_karty:** `REPO-HB-0D51`
- **ścieżka:** `.python_packages/scipy/io/_harwell_boeing/hb.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.979`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/io/_harwell_boeing/hb.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.979 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_OBLIGATION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.59271`
- **R₃:** `0.552945`
- **R₆:** `0.534582`
- **R₉:** `0.582078`
- **potencjal_kappa:** `0.23834`
- **masa_semantyczna:** `-0.091456`
- **rodzaj_karty:** `0.276031`


## Rola
Implementation of Harwell-Boeing read/write.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** MalformedHeader, LineOverflow, HBInfo, HBMatrixType, HBFile
- **funkcje:** `_nbytes_full`, `_expect_int`, `_read_hb_data`, `_write_data`, `hb_read`, `hb_write`, `from_data`, `from_file`, `dump`, `write_array`, `from_fortran`, `fortran_format`, `title`, `key`, `type`, `structure`, `storage`, `read_matrix`, `write_matrix`, `_get_matrix`, `_set_matrix`, `_nlines`

## Opis
Implementation of Harwell-Boeing read/write.

At the moment not the full Harwell-Boeing format is supported. Supported
features are:

    - assembled, non-symmetric, real matrices
    - integer for pointer/indices
    - exponential format for float values, and int format
