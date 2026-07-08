# test_highlevel_vds.py — .python_packages/h5py/tests/test_vds/test_highlevel_vds.py

## Tożsamość
- **id_karty:** `REPO-TEST_HIGHLEVEL_VDS-C71D`
- **ścieżka:** `.python_packages/h5py/tests/test_vds/test_highlevel_vds.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.100`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/h5py/tests/test_vds/test_highlevel_vds.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.100 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_POSSIBILITY`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.565748`
- **R₃:** `0.628966`
- **R₆:** `0.492583`
- **R₉:** `0.589778`
- **potencjal_kappa:** `0.024081`
- **masa_semantyczna:** `-0.294904`
- **rodzaj_karty:** `0.302592`


## Rola
Unit test for the high level vds interface for eiger

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestEigerHighLevel, ExcaliburData, TestExcaliburHighLevel, TestPercivalHighLevel, SlicingTestCase, IndexingTestCase, RelativeLinkTestCase, RelativeLinkBuildVDSTestCase, VDSUnlimitedTestCase
- **funkcje:** `test_no_mappings`, `setUp`, `test_eiger_high_level`, `tearDown`, `sensor_module_dimensions`, `fem_stripe_dimensions`, `generate_sensor_module_image`, `generate_fem_stripe_image`, `create_excalibur_fem_stripe_datafile`, `setUp`, `test_excalibur_high_level`, `tearDown`, `setUp`, `test_percival_high_level`, `test_percival_source_from_dataset`, `tearDown`, `setUp`, `make_virtual_ds`, `test_slice_source`, `test_inspection`, `test_mismatched_selections`, `tearDown`, `setUp`, `test_index_layout`, `tearDown`, `setUp`, `make_vds`, `test_relative_vds`, `tearDown`, `make_vds`

## Opis
Unit test for the high level vds interface for eiger
https://support.hdfgroup.org/HDF5/docNewFeatures/VDS/HDF5-VDS-requirements-use-cases-2014-12-10.pdf
