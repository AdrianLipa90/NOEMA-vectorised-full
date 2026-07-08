# npdatetime_helpers.py — .python_packages/numba/np/npdatetime_helpers.py

## Tożsamość
- **id_karty:** `REPO-NPDATETIME_HELPERS-0A73`
- **ścieżka:** `.python_packages/numba/np/npdatetime_helpers.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.650`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/np/npdatetime_helpers.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.650 |
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
Helper functions for np.timedelta64 and np.datetime64.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `same_kind`, `can_cast_timedelta_units`, `_get_conversion_multiplier`, `get_timedelta_conversion_factor`, `get_datetime_timedelta_conversion`, `combine_datetime_timedelta_units`, `get_best_unit`, `datetime_minimum`, `datetime_maximum`

## Opis
Helper functions for np.timedelta64 and np.datetime64.
For now, multiples-of-units (for example timedeltas expressed in tens
of seconds) are not supported.
