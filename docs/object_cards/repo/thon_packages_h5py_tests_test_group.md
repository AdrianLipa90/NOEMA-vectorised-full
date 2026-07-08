# test_group.py — .python_packages/h5py/tests/test_group.py

## Tożsamość
- **id_karty:** `REPO-TEST_GROUP-CFE4`
- **ścieżka:** `.python_packages/h5py/tests/test_group.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.809`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/h5py/tests/test_group.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.809 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `BOUNDARY`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.587016`
- **R₃:** `0.481937`
- **R₆:** `0.525424`
- **R₉:** `0.380572`
- **potencjal_kappa:** `-0.130804`
- **masa_semantyczna:** `0.12548`
- **rodzaj_karty:** `0.280526`


## Rola
Group test module.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** BaseGroup, TestCreate, TestDatasetAssignment, TestDtypeAssignment, TestRequire, TestDelete, TestOpen, TestRepr, BaseMapping, TestLen, TestContains, TestIter, TestTrackOrder, TestPy3Dict, TestAdditionalMappingFuncs, TestGet, TestVisit, TestVisitLinks, Visitor, TestLexicographic
- **funkcje:** `test_get_elink_mode_arg`, `test_get_elink_mode_arg_exception`, `test_get_elink_swmr_arg_from_ro_file`, `test_get_elink_swmr_arg_from_rw_file`, `test_get_elink_swmr_arg_from_rw_swmr_file`, `test_get_elink_locking_arg`, `setUp`, `tearDown`, `test_create_str`, `test_create_bytes`, `test_create_intermediate_str`, `test_create_intermediate_bytes`, `test_create_exception`, `test_unicode`, `test_unicode_default`, `test_type`, `test_appropriate_low_level_id`, `test_ndarray`, `test_name_bytes`, `test_dtype`, `test_name_bytes`, `test_open_existing`, `test_create`, `test_require_exception`, `test_intermediate_create_dataset`, `test_intermediate_create_group`, `test_require_shape`, `test_delete`, `test_nonexisting`, `test_readonly_delete_exception`

## Opis
Group test module.

Tests all methods and properties of Group objects, with the following
exceptions:

1. Method create_dataset is tested in module test_dataset
