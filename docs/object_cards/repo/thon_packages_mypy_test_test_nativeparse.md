# test_nativeparse.py — .python_packages/mypy/test/test_nativeparse.py

## Tożsamość
- **id_karty:** `REPO-TEST_NATIVEPARSE-D9A5`
- **ścieżka:** `.python_packages/mypy/test/test_nativeparse.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.144`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/test/test_nativeparse.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.144 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ATTRACTOR`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.476161`
- **R₃:** `0.526498`
- **R₆:** `0.547584`
- **R₉:** `0.472579`
- **potencjal_kappa:** `4.910705`
- **masa_semantyczna:** `13.031004`
- **rodzaj_karty:** `1.5`


## Rola
Tests for the experimental native mypy parser.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** NativeParserSuite, NativeParserImportsSuite, TestNativeParserBinaryFormat
- **funkcje:** `test_parser`, `format_error`, `format_ignore`, `load_tree`, `test_parser_imports`, `format_reachable_imports`, `temp_source`, `run_case`, `run_case`, `test_trivial_binary_data`, `int_enc`, `locs`

## Opis
Tests for the experimental native mypy parser.

To run these, you will need to manually install ast_serialize from
https://github.com/mypyc/ast_serialize first (see the README for the details).
