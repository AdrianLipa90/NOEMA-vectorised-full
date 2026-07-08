# test_packaging.py — tests/test_packaging.py

## Tożsamość
- **id_karty:** `REPO-TEST_PACKAGING-C49A`
- **ścieżka:** `tests/test_packaging.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.300`
- **φ (phi):** `1.299`
- **masa_semantyczna:** `0.40`

## Kotwice
- `tests/test_packaging.py`

## Atraktor
- **system:** `sync_core`
- **główny_atraktor:** orbital_bridge_core → ent_Mr_Ciel_Apocalyptos

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.300 |
| φ | 1.299 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `sync_core`.

## PhaseNav
- **operator:** `ORDER`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.408132`
- **R₃:** `0.527143`
- **R₆:** `0.447287`
- **R₉:** `0.516074`
- **potencjal_kappa:** `0.213299`
- **masa_semantyczna:** `0.199346`
- **rodzaj_karty:** `0.279908`


## Rola
Tests for the CIEL SOT Agent platform packaging.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem sync_core*
- **wyjście:** *wywnioskowane z folderu — podsystem sync_core*

## Zawartość
- **klasy:** TestDebianPackageStructure, TestDebianControlFile, TestDebianScripts, TestDebianConffiles, TestDebianConfigFile, TestDebianServiceFile, TestDebianLauncher, TestBuildScript, TestConstraintsFile, TestAndroidPackagingStructure, TestBuildozerSpec, TestAndroidMainModule
- **funkcje:** `test_debian_dir_exists`, `test_control_file_exists`, `test_postinst_exists`, `test_prerm_exists`, `test_postrm_exists`, `test_conffiles_exists`, `test_launcher_exists`, `test_model_installer_launcher_exists`, `test_service_file_exists`, `test_wheels_dir_exists`, `test_models_dir_exists`, `test_config_file_exists`, `test_constraints_file_exists`, `test_readme_exists`, `test_build_script_exists`, `load_control`, `_field`, `test_package_name`, `test_version_present`, `test_architecture`, `test_depends_python`, `test_depends_python_venv`, `test_does_not_depend_on_pip`, `test_description_not_empty`, `test_postinst_is_shell_script`, `test_postinst_creates_venv`, `test_postinst_contains_pip_install`, `test_postinst_installs_offline`, `test_postinst_uses_bundled_wheels`, `test_postinst_does_not_global_pip_install`

## Opis
Tests for the CIEL SOT Agent platform packaging.

These tests verify:
- The Debian package structure is complete and well-formed
- The Android Buildozer spec is valid and contains required fields
- The Android Kivy main module is importable and has the expected API
- The build_deb.sh script exists and is a valid shell script
