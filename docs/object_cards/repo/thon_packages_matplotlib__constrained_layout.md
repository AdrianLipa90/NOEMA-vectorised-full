# _constrained_layout.py — .python_packages/matplotlib/_constrained_layout.py

## Tożsamość
- **id_karty:** `REPO-_CONSTRAINED_LAYOUT-FF00`
- **ścieżka:** `.python_packages/matplotlib/_constrained_layout.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.451`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/_constrained_layout.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.451 |
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
Adjust subplot layouts so that there are no overlapping Axes or Axes

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `do_constrained_layout`, `make_layoutgrids`, `make_layoutgrids_gs`, `check_no_collapsed_axes`, `compress_fixed_aspect`, `get_margin_from_padding`, `make_layout_margins`, `make_margin_suptitles`, `match_submerged_margins`, `get_cb_parent_spans`, `get_pos_and_bbox`, `reposition_axes`, `reposition_colorbar`, `reset_margins`, `colorbar_get_pad`

## Opis
Adjust subplot layouts so that there are no overlapping Axes or Axes
decorations.  All Axes decorations are dealt with (labels, ticks, titles,
ticklabels) and some dependent artists are also dealt with (colorbar,
suptitle).

Layout is done via `~matplotlib.gridspec`, with one constraint per gridspec,
so it is possible to have overlapping Axes if the gridspecs overlap (i.e.
using `~matplotlib.grids
