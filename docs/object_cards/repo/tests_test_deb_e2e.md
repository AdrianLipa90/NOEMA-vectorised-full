# test_deb_e2e.py — tests/test_deb_e2e.py

## Tożsamość
- **id_karty:** `REPO-TEST_DEB_E2E-19A4`
- **ścieżka:** `tests/test_deb_e2e.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.300`
- **φ (phi):** `5.011`
- **masa_semantyczna:** `0.40`

## Kotwice
- `tests/test_deb_e2e.py`

## Atraktor
- **system:** `sync_core`
- **główny_atraktor:** orbital_bridge_core → ent_Mr_Ciel_Apocalyptos

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.300 |
| φ | 5.011 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `sync_core`.

## PhaseNav
- **operator:** `PAUSE`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.508756`
- **R₃:** `0.557009`
- **R₆:** `0.421727`
- **R₉:** `0.55292`
- **potencjal_kappa:** `-0.020552`
- **masa_semantyczna:** `0.206252`
- **rodzaj_karty:** `0.260435`


## Rola
End-to-end smoke tests for the Debian .deb package build.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem sync_core*
- **wyjście:** *wywnioskowane z folderu — podsystem sync_core*

## Zawartość
- **klasy:** TestDebPackageMetadata, TestDebFileLayout
- **funkcje:** `_build_script_is_fast`, `built_deb`, `deb_contents`, `deb_info`, `test_package_name`, `test_version_matches`, `test_architecture_is_not_all`, `test_depends_python_venv`, `test_does_not_depend_on_pip`, `test_expected_file_present`, `test_wheels_directory_present`, `test_wheels_are_bundled`, `test_no_gitkeep_files`, `test_no_build_script_inside`, `test_no_constraints_inside`, `test_no_readme_inside`, `test_models_directory_present`, `test_maintainer_scripts_present`, `test_conffiles_present`

## Opis
End-to-end smoke tests for the Debian .deb package build.

These tests build the actual .deb package using ``build_deb.sh``, then
inspect the resulting archive with ``dpkg-deb`` to verify that the
package contains the expected files and metadata.

The tests are skipped automatically when ``dpkg-deb`` is not available
(e.g. on macOS or non-Debian CI runners) or when ``build_deb.sh`` is too
slow (lo
