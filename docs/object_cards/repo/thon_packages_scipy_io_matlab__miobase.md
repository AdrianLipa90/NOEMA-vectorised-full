# _miobase.py — .python_packages/scipy/io/matlab/_miobase.py

## Tożsamość
- **id_karty:** `REPO-_MIOBASE-0316`
- **ścieżka:** `.python_packages/scipy/io/matlab/_miobase.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.289`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/io/matlab/_miobase.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.289 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CONSENT_REQUIRED`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.458017`
- **R₃:** `0.48995`
- **R₆:** `0.569953`
- **R₉:** `0.575041`
- **potencjal_kappa:** `-0.194917`
- **masa_semantyczna:** `0.103166`
- **rodzaj_karty:** `0.278924`


## Rola
Base classes for MATLAB file stream reading.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** MatReadError, MatWriteError, MatReadWarning, MatWriteWarning, MatVarReader, MatFileReader
- **funkcje:** `convert_dtypes`, `read_dtype`, `matfile_version`, `_get_matfile_version`, `matdims`, `arr_dtype_number`, `arr_to_chars`, `read_header`, `array_from_header`, `set_matlab_compatible`, `guess_byte_order`, `end_of_stream`

## Opis
Base classes for MATLAB file stream reading.

MATLAB is a registered trademark of the Mathworks inc.
