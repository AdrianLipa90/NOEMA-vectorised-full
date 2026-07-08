# axis_artist.py — .python_packages/mpl_toolkits/axisartist/axis_artist.py

## Tożsamość
- **id_karty:** `REPO-AXIS_ARTIST-9A64`
- **ścieżka:** `.python_packages/mpl_toolkits/axisartist/axis_artist.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.086`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mpl_toolkits/axisartist/axis_artist.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.086 |
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
The :mod:`.axis_artist` module implements custom artists to draw axis elements

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** AttributeCopier, Ticks, LabelBase, AxisLabel, TickLabels, GridlinesCollection, AxisArtist
- **funkcje:** `get_ref_artist`, `get_attribute_from_ref_artist`, `get_ref_artist`, `set_color`, `get_color`, `get_markeredgecolor`, `get_markeredgewidth`, `set_tick_direction`, `get_tick_direction`, `set_tick_out`, `get_tick_out`, `set_ticksize`, `get_ticksize`, `set_locs_angles`, `draw`, `_text_ref_angle`, `_offset_ref_angle`, `draw`, `get_window_extent`, `set_pad`, `get_pad`, `get_ref_artist`, `get_text`, `set_default_alignment`, `set_default_angle`, `set_axis_direction`, `get_color`, `draw`, `get_window_extent`, `get_ref_artist`

## Opis
The :mod:`.axis_artist` module implements custom artists to draw axis elements
(axis lines and labels, tick lines and labels, grid lines).

Axis lines and labels and tick lines and labels are managed by the `AxisArtist`
class; grid lines are managed by the `GridlinesCollection` class.

There is one `AxisArtist` per Axis; it can be accessed through
the ``axis`` dictionary of the parent Axes (which
