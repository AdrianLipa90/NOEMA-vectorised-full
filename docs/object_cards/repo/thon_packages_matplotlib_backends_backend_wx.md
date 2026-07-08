# backend_wx.py — .python_packages/matplotlib/backends/backend_wx.py

## Tożsamość
- **id_karty:** `REPO-BACKEND_WX-A35B`
- **ścieżka:** `.python_packages/matplotlib/backends/backend_wx.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.054`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/backends/backend_wx.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.054 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `FOLD`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.351212`
- **R₃:** `0.661831`
- **R₆:** `0.649218`
- **R₉:** `0.522246`
- **potencjal_kappa:** `-0.135067`
- **masa_semantyczna:** `-0.137397`
- **rodzaj_karty:** `0.29302`


## Rola
A wxPython backend for matplotlib.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TimerWx, RendererWx, GraphicsContextWx, _FigureCanvasWxBase, FigureCanvasWx, FigureFrameWx, FigureManagerWx, NavigationToolbar2Wx, ToolbarWx, ConfigureSubplotsWx, SaveFigureWx, RubberbandWx, _HelpDialog, HelpWx, ToolCopyToClipboardWx, _BackendWx
- **funkcje:** `_create_wxapp`, `_load_bitmap`, `_set_frame_icon`, `_timer_start`, `_timer_stop`, `_timer_set_interval`, `flipy`, `get_text_width_height_descent`, `get_canvas_width_height`, `handle_clip_rectangle`, `convert_path`, `draw_path`, `draw_image`, `draw_text`, `new_gc`, `get_wx_font`, `points_to_pixels`, `select`, `unselect`, `set_foreground`, `set_linewidth`, `set_capstyle`, `set_joinstyle`, `get_wxcolour`, `Copy_to_Clipboard`, `_update_device_pixel_ratio`, `draw_idle`, `flush_events`, `start_event_loop`, `stop_event_loop`

## Opis
A wxPython backend for matplotlib.

Originally contributed by Jeremy O'Donoghue (jeremy@o-donoghue.com) and John
Hunter (jdhunter@ace.bsd.uchicago.edu).

Copyright (C) Jeremy O'Donoghue & John Hunter, 2003-4.
