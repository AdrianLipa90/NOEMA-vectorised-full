# test_update_data.py — .python_packages/mypy/test/meta/test_update_data.py

## Tożsamość
- **id_karty:** `REPO-TEST_UPDATE_DATA-C662`
- **ścieżka:** `.python_packages/mypy/test/meta/test_update_data.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.570`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/test/meta/test_update_data.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.570 |
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
A "meta test" which tests the `--update-data` feature for updating .test files.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** UpdateDataSuite
- **funkcje:** `_run_pytest_update_data`, `test_update_data`

## Opis
A "meta test" which tests the `--update-data` feature for updating .test files.
Updating the expected output, especially when it's in the form of inline (comment) assertions,
can be brittle, which is why we're "meta-testing" here.
