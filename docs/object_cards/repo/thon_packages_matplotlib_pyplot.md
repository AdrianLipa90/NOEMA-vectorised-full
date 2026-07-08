# pyplot.py — .python_packages/matplotlib/pyplot.py

## Tożsamość
- **id_karty:** `REPO-PYPLOT-8C4F`
- **ścieżka:** `.python_packages/matplotlib/pyplot.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.637`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/pyplot.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.637 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SOURCE`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.591319`
- **R₃:** `0.39689`
- **R₆:** `0.568492`
- **R₉:** `0.527911`
- **potencjal_kappa:** `0.015345`
- **masa_semantyczna:** `-0.142691`
- **rodzaj_karty:** `0.266598`


## Rola
`matplotlib.pyplot` is a state-based interface to matplotlib. It provides

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** backend_mod
- **funkcje:** `_copy_docstring_and_deprecators`, `_copy_docstring_and_deprecators`, `_copy_docstring_and_deprecators`, `_add_pyplot_note`, `_draw_all_if_interactive`, `install_repl_displayhook`, `uninstall_repl_displayhook`, `set_loglevel`, `findobj`, `_get_backend_mod`, `switch_backend`, `_warn_if_gui_out_of_main_thread`, `new_figure_manager`, `draw_if_interactive`, `show`, `show`, `show`, `isinteractive`, `ioff`, `ion`, `pause`, `rc`, `rc_context`, `rcdefaults`, `getp`, `get`, `setp`, `xkcd`, `figure`, `_auto_draw_if_interactive`

## Opis
`matplotlib.pyplot` is a state-based interface to matplotlib. It provides
an implicit,  MATLAB-like, way of plotting.  It also opens figures on your
screen, and acts as the figure GUI manager.

pyplot is mainly intended for interactive plots and simple cases of
programmatic plot generation::

    import numpy as np
    import matplotlib.pyplot as plt

    x = np.arange(0, 5, 0.1)
    y = np.sin(x)
