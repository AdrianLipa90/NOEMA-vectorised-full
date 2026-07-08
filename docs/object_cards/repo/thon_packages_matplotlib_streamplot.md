# streamplot.py — .python_packages/matplotlib/streamplot.py

## Tożsamość
- **id_karty:** `REPO-STREAMPLOT-B0E1`
- **ścieżka:** `.python_packages/matplotlib/streamplot.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `6.014`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/streamplot.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 6.014 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CONDITION`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.577442`
- **R₃:** `0.440978`
- **R₆:** `0.50908`
- **R₉:** `0.325439`
- **potencjal_kappa:** `-0.091854`
- **masa_semantyczna:** `-0.064427`
- **rodzaj_karty:** `0.305875`


## Rola
Streamline plotting for 2D vector fields.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** StreamplotSet, DomainMap, Grid, StreamMask, InvalidIndexError, TerminateTrajectory, OutOfBounds
- **funkcje:** `streamplot`, `_get_integrator`, `_integrate_rk12`, `_euler_step`, `interpgrid`, `_gen_starting_points`, `grid2mask`, `mask2grid`, `data2grid`, `grid2data`, `start_trajectory`, `reset_start_point`, `update_trajectory`, `undo_trajectory`, `shape`, `within_grid`, `_start_trajectory`, `_undo_trajectory`, `_update_trajectory`, `forward_time`, `backward_time`, `integrate`

## Opis
Streamline plotting for 2D vector fields.
