# gridspec.py — .python_packages/matplotlib/gridspec.py

## Tożsamość
- **id_karty:** `REPO-GRIDSPEC-23AF`
- **ścieżka:** `.python_packages/matplotlib/gridspec.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.841`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/gridspec.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.841 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MEMORY`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.481637`
- **R₃:** `0.436994`
- **R₆:** `0.50573`
- **R₉:** `0.517955`
- **potencjal_kappa:** `0.179117`
- **masa_semantyczna:** `0.012321`
- **rodzaj_karty:** `0.236997`


## Rola
:mod:`~matplotlib.gridspec` contains classes that help to layout multiple

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** GridSpecBase, GridSpec, GridSpecFromSubplotSpec, SubplotSpec, SubplotParams
- **funkcje:** `get_geometry`, `get_subplot_params`, `new_subplotspec`, `set_width_ratios`, `get_width_ratios`, `set_height_ratios`, `get_height_ratios`, `get_grid_positions`, `_check_gridspec_exists`, `subplots`, `update`, `get_subplot_params`, `locally_modified_subplot_params`, `tight_layout`, `get_subplot_params`, `get_topmost_subplotspec`, `_from_subplot_args`, `num2`, `num2`, `get_gridspec`, `get_geometry`, `rowspan`, `colspan`, `is_first_row`, `is_last_row`, `is_first_col`, `is_last_col`, `get_position`, `get_topmost_subplotspec`, `subgridspec`

## Opis
:mod:`~matplotlib.gridspec` contains classes that help to layout multiple
`~.axes.Axes` in a grid-like pattern within a figure.

The `GridSpec` specifies the overall grid structure. Individual cells within
the grid are referenced by `SubplotSpec`\s.

Often, users need not access this module directly, and can use higher-level
methods like `~.pyplot.subplots`, `~.pyplot.subplot_mosaic` and
`~.Figure
