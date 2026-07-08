# widgets.py — .python_packages/matplotlib/widgets.py

## Tożsamość
- **id_karty:** `REPO-WIDGETS-6DC9`
- **ścieżka:** `.python_packages/matplotlib/widgets.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.661`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/widgets.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.661 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_POSSIBILITY`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.565748`
- **R₃:** `0.628966`
- **R₆:** `0.492583`
- **R₉:** `0.589778`
- **potencjal_kappa:** `0.024081`
- **masa_semantyczna:** `-0.294904`
- **rodzaj_karty:** `0.302592`


## Rola
Widgets that are designed to work for any of the GUI backends.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** LockDraw, Widget, AxesWidget, Button, SliderBase, Slider, RangeSlider, _Buttons, CheckButtons, TextBox, RadioButtons, SubplotTool, Cursor, MultiCursor, _SelectorWidget, SpanSelector, ToolLineHandles, ToolHandles, _RectangleSelectorAction, RectangleSelector
- **funkcje:** `_call_with_reparented_event`, `_expand_text_props`, `release`, `available`, `isowner`, `locked`, `set_active`, `get_active`, `ignore`, `connect_event`, `disconnect_events`, `ignore`, `_set_cursor`, `_save_blit_background`, `_load_blit_background`, `wrapper`, `_click`, `_release`, `_motion`, `on_clicked`, `disconnect`, `_stepped_value`, `disconnect`, `reset`, `_value_in_bounds`, `_update`, `_format`, `set_val`, `on_changed`, `_update_selection_poly`

## Opis
Widgets that are designed to work for any of the GUI backends.

All of these widgets require you to predefine an `~.axes.Axes`
instance and pass that as the first parameter.  Matplotlib doesn't try to
be too smart with respect to layout -- you will have to figure out how
wide and tall you want your Axes to be to accommodate your widget.
