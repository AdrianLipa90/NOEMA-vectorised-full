# inset.py — .python_packages/matplotlib/inset.py

## Tożsamość
- **id_karty:** `REPO-INSET-4E4C`
- **ścieżka:** `.python_packages/matplotlib/inset.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.225`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/inset.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.225 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ADDITION`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.662589`
- **R₃:** `0.614656`
- **R₆:** `0.542851`
- **R₉:** `0.417608`
- **potencjal_kappa:** `0.07638`
- **masa_semantyczna:** `0.206164`
- **rodzaj_karty:** `0.259027`


## Rola
The inset module defines the InsetIndicator class, which draws the rectangle and

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** InsetIndicator
- **funkcje:** `_shared_setter`, `axes`, `set_alpha`, `set_edgecolor`, `set_color`, `set_linewidth`, `set_linestyle`, `_bounds_from_inset_ax`, `_update_connectors`, `rectangle`, `connectors`, `draw`

## Opis
The inset module defines the InsetIndicator class, which draws the rectangle and
connectors required for `.Axes.indicate_inset` and `.Axes.indicate_inset_zoom`.
