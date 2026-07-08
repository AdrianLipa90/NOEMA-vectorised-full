# nx_latex.py — .python_packages/networkx/drawing/nx_latex.py

## Tożsamość
- **id_karty:** `REPO-NX_LATEX-434C`
- **ścieżka:** `.python_packages/networkx/drawing/nx_latex.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.912`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/networkx/drawing/nx_latex.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.912 |
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
*****

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `to_latex_raw`, `to_latex`, `write_latex`

## Opis
*****
LaTeX
*****

Export NetworkX graphs in LaTeX format using the TikZ library within TeX/LaTeX.
Usually, you will want the drawing to appear in a figure environment so
you use ``to_latex(G, caption="A caption")``. If you want the raw
drawing commands without a figure environment use :func:`to_latex_raw`.
And if you want to write to a file instead of just returning the latex
code as a string, us
