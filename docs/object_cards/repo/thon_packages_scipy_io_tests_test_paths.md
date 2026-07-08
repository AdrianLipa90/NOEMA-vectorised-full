# test_paths.py — .python_packages/scipy/io/tests/test_paths.py

## Tożsamość
- **id_karty:** `REPO-TEST_PATHS-0EF8`
- **ścieżka:** `.python_packages/scipy/io/tests/test_paths.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.061`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/io/tests/test_paths.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.061 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SOURCE`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.591319`
- **R₃:** `0.39689`
- **R₆:** `0.568492`
- **R₉:** `0.527911`
- **potencjal_kappa:** `0.015345`
- **masa_semantyczna:** `-0.142691`
- **rodzaj_karty:** `0.266598`


## Rola
Ensure that we can use pathlib.Path objects in all relevant IO functions.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestPaths
- **funkcje:** `test_savemat`, `test_loadmat`, `test_whosmat`, `test_readsav`, `test_hb_read`, `test_hb_write`, `test_mmio_read`, `test_mmio_write`, `test_netcdf_file`, `test_wavfile_read`, `test_wavfile_write`

## Opis
Ensure that we can use pathlib.Path objects in all relevant IO functions.
