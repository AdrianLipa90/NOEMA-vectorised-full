# test_interval_example.py — .python_packages/numba/tests/doc_examples/test_interval_example.py

## Tożsamość
- **id_karty:** `REPO-TEST_INTERVAL_EXAMPL-992C`
- **ścieżka:** `.python_packages/numba/tests/doc_examples/test_interval_example.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.937`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/tests/doc_examples/test_interval_example.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.937 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RISK`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.594265`
- **R₃:** `0.468144`
- **R₆:** `0.457554`
- **R₉:** `0.414103`
- **potencjal_kappa:** `0.19508`
- **masa_semantyczna:** `-0.03873`
- **rodzaj_karty:** `0.279007`


## Rola
This test is used by `docs/source/extending/interval-example.rst`.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** IntervalExampleTest, Interval, IntervalType, IntervalModel, NotAFloat
- **funkcje:** `test_interval_class_usage`, `typeof_index`, `type_interval`, `get_width`, `impl_interval`, `unbox_interval`, `box_interval`, `inside_interval`, `interval_width`, `sum_intervals`, `check_equal_intervals`, `width`, `typer`, `getter`

## Opis
This test is used by `docs/source/extending/interval-example.rst`.

The "magictoken" comments are used as markers for the beginning and ending of
example code.
