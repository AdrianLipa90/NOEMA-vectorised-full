# build.py — .python_packages/mypyc/build.py

## Tożsamość
- **id_karty:** `REPO-BUILD-1975`
- **ścieżka:** `.python_packages/mypyc/build.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.161`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/build.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.161 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `QUESTION`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.394639`
- **R₃:** `0.763677`
- **R₆:** `0.521308`
- **R₉:** `0.466584`
- **potencjal_kappa:** `-0.203086`
- **masa_semantyczna:** `-0.0017`
- **rodzaj_karty:** `0.305584`


## Rola
Support for building extensions using mypyc with distutils or setuptools

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ModDesc
- **funkcje:** `get_extension`, `setup_mypycify_vars`, `fail`, `emit_messages`, `get_mypy_config`, `is_package_source`, `generate_c_extension_shim`, `group_name`, `include_dir`, `generate_c`, `build_using_shared_lib`, `build_single_module`, `write_file`, `_patch_setuptools_copy_extensions_to_source`, `construct_groups`, `get_header_deps`, `mypyc_build`, `get_cflags`, `mypycify`, `_files_match`, `patched`, `is_redundant`

## Opis
Support for building extensions using mypyc with distutils or setuptools

The main entry point is mypycify, which produces a list of extension
modules to be passed to setup. A trivial setup.py for a mypyc built
project, then, looks like:

    from setuptools import setup
    from mypyc.build import mypycify

    setup(name='test_module',
          ext_modules=mypycify(['foo.py']),
    )

See the m
