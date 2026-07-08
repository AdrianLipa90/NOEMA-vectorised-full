# _basinhopping.py — .python_packages/scipy/optimize/_basinhopping.py

## Tożsamość
- **id_karty:** `REPO-_BASINHOPPING-F7A9`
- **ścieżka:** `.python_packages/scipy/optimize/_basinhopping.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.347`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/optimize/_basinhopping.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.347 |
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
basinhopping: The basinhopping global optimization algorithm

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Storage, BasinHoppingRunner, AdaptiveStepsize, RandomDisplacement, MinimizerWrapper, Metropolis
- **funkcje:** `basinhopping`, `_add`, `update`, `get_lowest`, `_monte_carlo_step`, `one_cycle`, `print_report`, `_adjust_step_size`, `take_step`, `report`, `accept_reject`

## Opis
basinhopping: The basinhopping global optimization algorithm
