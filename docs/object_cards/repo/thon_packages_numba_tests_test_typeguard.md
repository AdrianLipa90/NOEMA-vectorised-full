# test_typeguard.py — .python_packages/numba/tests/test_typeguard.py

## Tożsamość
- **id_karty:** `REPO-TEST_TYPEGUARD-D3E2`
- **ścieżka:** `.python_packages/numba/tests/test_typeguard.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.552`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/tests/test_typeguard.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.552 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `REFUSAL`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.441725`
- **R₃:** `0.537197`
- **R₆:** `0.362678`
- **R₉:** `0.509166`
- **potencjal_kappa:** `0.077364`
- **masa_semantyczna:** `-0.245874`
- **rodzaj_karty:** `0.27107`


## Rola
Tests to ensure that typeguard is working as expected.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestTypeGuard
- **funkcje:** `guard_args`, `guard_ret`, `setUp`, `test_check_args`, `test_check_ret`, `test_check_does_not_work_with_inner_func`, `guard`

## Opis
Tests to ensure that typeguard is working as expected.
This mostly contains negative tests as proof that typeguard can catch errors.
