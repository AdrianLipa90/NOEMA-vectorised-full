# legend.py — .python_packages/matplotlib/legend.py

## Tożsamość
- **id_karty:** `REPO-LEGEND-83A2`
- **ścieżka:** `.python_packages/matplotlib/legend.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.506`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/legend.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.506 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `DIFFERENCE`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.563622`
- **R₃:** `0.51399`
- **R₆:** `0.516024`
- **R₉:** `0.447233`
- **potencjal_kappa:** `-0.196591`
- **masa_semantyczna:** `-0.06476`
- **rodzaj_karty:** `0.313562`


## Rola
The legend module defines the Legend class, which is responsible for

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** DraggableLegend, Legend
- **funkcje:** `_get_legend_handles`, `_get_legend_handles_labels`, `_parse_legend_args`, `finalize_offset`, `_update_loc`, `_update_bbox_to_anchor`, `_set_artist_props`, `set_loc`, `_set_loc`, `set_ncols`, `_get_loc`, `_findoffset`, `draw`, `get_default_handler_map`, `set_default_handler_map`, `update_default_handler_map`, `get_legend_handler_map`, `get_legend_handler`, `_init_legend_box`, `_auto_legend_data`, `get_children`, `get_frame`, `get_lines`, `get_patches`, `get_texts`, `set_alignment`, `get_alignment`, `set_title`, `get_title`, `get_window_extent`

## Opis
The legend module defines the Legend class, which is responsible for
drawing legends associated with Axes and/or figures.

.. important::

    It is unlikely that you would ever create a Legend instance manually.
    Most users would normally create a legend via the `~.Axes.legend`
    function. For more details on legends there is also a :ref:`legend guide
    <legend_guide>`.

The `Legend` class
