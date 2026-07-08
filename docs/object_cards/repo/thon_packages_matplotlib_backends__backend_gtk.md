# _backend_gtk.py — .python_packages/matplotlib/backends/_backend_gtk.py

## Tożsamość
- **id_karty:** `REPO-_BACKEND_GTK-CFF8`
- **ścieżka:** `.python_packages/matplotlib/backends/_backend_gtk.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.325`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/backends/_backend_gtk.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.325 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CANON_BLOCK`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.593927`
- **R₃:** `0.544645`
- **R₆:** `0.483246`
- **R₉:** `0.501272`
- **potencjal_kappa:** `0.159378`
- **masa_semantyczna:** `-0.256779`
- **rodzaj_karty:** `0.332318`


## Rola
Common code for GTK3 and GTK4 backends.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TimerGTK, _FigureCanvasGTK, _FigureManagerGTK, _NavigationToolbar2GTK, RubberbandGTK, ConfigureSubplotsGTK, _BackendGTK
- **funkcje:** `_shutdown_application`, `_create_application`, `mpl_to_gtk_cursor_name`, `_timer_start`, `_timer_stop`, `_timer_set_interval`, `_on_timer`, `destroy`, `start_main_loop`, `show`, `full_screen_toggle`, `get_window_title`, `set_window_title`, `resize`, `set_message`, `draw_rubberband`, `remove_rubberband`, `_update_buttons_checked`, `pan`, `zoom`, `set_history_buttons`, `draw_rubberband`, `remove_rubberband`, `trigger`

## Opis
Common code for GTK3 and GTK4 backends.
