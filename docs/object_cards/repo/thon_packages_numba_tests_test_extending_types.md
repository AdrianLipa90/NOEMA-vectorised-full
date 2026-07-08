# test_extending_types.py — .python_packages/numba/tests/test_extending_types.py

## Tożsamość
- **id_karty:** `REPO-TEST_EXTENDING_TYPES-57E5`
- **ścieżka:** `.python_packages/numba/tests/test_extending_types.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.684`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/tests/test_extending_types.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.684 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `IDENTITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.405566`
- **R₃:** `0.499333`
- **R₆:** `0.494094`
- **R₉:** `0.455981`
- **potencjal_kappa:** `0.08965`
- **masa_semantyczna:** `-0.024381`
- **rodzaj_karty:** `0.279273`


## Rola
Test extending types via the numba.extending.* API.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestExtTypDummy, Dummy, DummyType, DummyModel
- **funkcje:** `gen_mock_float`, `mock_float`, `setUp`, `_add_float_overload`, `test_overload_float`, `test_overload_float_error_msg`, `test_unboxing`, `test_boxing`, `test_issue5565_literal_getitem`, `type_dummy`, `impl_dummy`, `typeof_dummy`, `dummy_to_float`, `foo`, `foo`, `foo`, `bar`, `foo`, `dummy_getitem_ovld`, `test_impl`, `typer`, `codegen`, `dummy_getitem_impl`, `dummy_getitem_impl`

## Opis
Test extending types via the numba.extending.* API.
