# axislines.py — .python_packages/mpl_toolkits/axisartist/axislines.py

## Tożsamość
- **id_karty:** `REPO-AXISLINES-E3FA`
- **ścieżka:** `.python_packages/mpl_toolkits/axisartist/axislines.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.752`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mpl_toolkits/axisartist/axislines.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.752 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `FORCE`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.552175`
- **R₃:** `0.435218`
- **R₆:** `0.571397`
- **R₉:** `0.579087`
- **potencjal_kappa:** `0.300939`
- **masa_semantyczna:** `0.016845`
- **rodzaj_karty:** `0.260112`


## Rola
Axislines includes modified implementation of the Axes class. The

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** _AxisArtistHelperBase, _FixedAxisArtistHelperBase, _FloatingAxisArtistHelperBase, FixedAxisArtistHelperRectilinear, FloatingAxisArtistHelperRectilinear, AxisArtistHelper, AxisArtistHelperRectlinear, GridHelperBase, GridHelperRectlinear, Axes, AxesZero
- **funkcje:** `update_lim`, `get_nth_coord`, `_to_xy`, `get_line`, `get_line_transform`, `get_axislabel_transform`, `get_axislabel_pos_angle`, `get_tick_transform`, `get_line`, `get_tick_iterators`, `get_line`, `get_line_transform`, `get_axislabel_transform`, `get_axislabel_pos_angle`, `get_tick_transform`, `get_tick_iterators`, `update_lim`, `_update_grid`, `get_gridlines`, `new_fixed_axis`, `new_floating_axis`, `get_gridlines`, `toggle_axisline`, `axis`, `clear`, `get_grid_helper`, `grid`, `get_children`, `new_fixed_axis`, `new_floating_axis`

## Opis
Axislines includes modified implementation of the Axes class. The
biggest difference is that the artists responsible for drawing the axis spine,
ticks, ticklabels and axis labels are separated out from Matplotlib's Axis
class. Originally, this change was motivated to support curvilinear
grid. Here are a few reasons that I came up with a new axes class:

* "top" and "bottom" x-axis (or "left" and "
