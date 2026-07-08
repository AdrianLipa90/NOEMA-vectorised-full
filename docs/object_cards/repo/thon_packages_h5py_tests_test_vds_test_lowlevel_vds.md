# test_lowlevel_vds.py — .python_packages/h5py/tests/test_vds/test_lowlevel_vds.py

## Tożsamość
- **id_karty:** `REPO-TEST_LOWLEVEL_VDS-0335`
- **ścieżka:** `.python_packages/h5py/tests/test_vds/test_lowlevel_vds.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.689`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/h5py/tests/test_vds/test_lowlevel_vds.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.689 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `WARP_DRIFT`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.47403`
- **R₃:** `0.56672`
- **R₆:** `0.57902`
- **R₉:** `0.540967`
- **potencjal_kappa:** `0.057762`
- **masa_semantyczna:** `0.153958`
- **rodzaj_karty:** `0.289083`


## Rola
Unit test for the low level vds interface for eiger

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestEigerLowLevel, ExcaliburData, TestExcaliburLowLevel, TestPercivalLowLevel
- **funkcje:** `test_virtual_prefix`, `setUp`, `test_eiger_low_level`, `tearDown`, `sensor_module_dimensions`, `fem_stripe_dimensions`, `generate_sensor_module_image`, `generate_fem_stripe_image`, `create_excalibur_fem_stripe_datafile`, `setUp`, `test_excalibur_low_level`, `tearDown`, `setUp`, `test_percival_low_level`, `tearDown`

## Opis
Unit test for the low level vds interface for eiger
https://support.hdfgroup.org/HDF5/docNewFeatures/VDS/HDF5-VDS-requirements-use-cases-2014-12-10.pdf
