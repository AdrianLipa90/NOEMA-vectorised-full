# _array_api_no_0d.py — .python_packages/scipy/_lib/_array_api_no_0d.py

## Tożsamość
- **id_karty:** `REPO-_ARRAY_API_NO_0D-9355`
- **ścieżka:** `.python_packages/scipy/_lib/_array_api_no_0d.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.702`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/_lib/_array_api_no_0d.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.702 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CAUSE`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.440841`
- **R₃:** `0.698384`
- **R₆:** `0.560357`
- **R₉:** `0.385177`
- **potencjal_kappa:** `0.165796`
- **masa_semantyczna:** `0.077602`
- **rodzaj_karty:** `0.2472`


## Rola
Extra testing functions that forbid 0d-input, see #21044

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_check_scalar`, `xp_assert_equal`, `xp_assert_close`, `xp_assert_less`, `assert_array_almost_equal`, `assert_almost_equal`

## Opis
Extra testing functions that forbid 0d-input, see #21044

While the xp_assert_* functions generally aim to follow the conventions of the
underlying `xp` library, NumPy in particular is inconsistent in its handling
of scalars vs. 0d-arrays, see https://github.com/numpy/numpy/issues/24897.

For example, this means that the following operations (as of v2.0.1) currently
return scalars, even though a 0
