# backend_tools.py — .python_packages/matplotlib/backend_tools.py

## Tożsamość
- **id_karty:** `REPO-BACKEND_TOOLS-2326`
- **ścieżka:** `.python_packages/matplotlib/backend_tools.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.430`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/backend_tools.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.430 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `UNCERTAINTY`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.435049`
- **R₃:** `0.572136`
- **R₆:** `0.544042`
- **R₉:** `0.477522`
- **potencjal_kappa:** `0.159902`
- **masa_semantyczna:** `-0.053674`
- **rodzaj_karty:** `0.279085`


## Rola
Abstract base classes define the primitives for Tools.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Cursors, ToolBase, ToolToggleBase, ToolSetCursor, ToolCursorPosition, RubberbandBase, ToolQuit, ToolQuitAll, ToolGrid, ToolMinorGrid, ToolFullScreen, AxisScaleBase, ToolYScale, ToolXScale, ToolViewsPositions, ViewsPositionsBase, ToolHome, ToolBack, ToolForward, ConfigureSubplotsBase
- **funkcje:** `_register_tool_class`, `_find_tool_class`, `add_tools_to_manager`, `add_tools_to_container`, `set_figure`, `_make_classic_style_pseudo_toolbar`, `trigger`, `trigger`, `enable`, `disable`, `toggled`, `set_figure`, `set_figure`, `_add_tool_cbk`, `_tool_trigger_cbk`, `_set_cursor_cbk`, `set_figure`, `send_message`, `trigger`, `draw_rubberband`, `remove_rubberband`, `trigger`, `trigger`, `trigger`, `trigger`, `trigger`, `trigger`, `enable`, `disable`, `set_scale`

## Opis
Abstract base classes define the primitives for Tools.
These tools are used by `matplotlib.backend_managers.ToolManager`

:class:`ToolBase`
    Simple stateless tool

:class:`ToolToggleBase`
    Tool that has two states, only one Toggle tool can be
    active at any given time for the same
    `matplotlib.backend_managers.ToolManager`
