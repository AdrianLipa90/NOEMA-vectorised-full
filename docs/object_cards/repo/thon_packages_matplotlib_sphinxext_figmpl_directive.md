# figmpl_directive.py — .python_packages/matplotlib/sphinxext/figmpl_directive.py

## Tożsamość
- **id_karty:** `REPO-FIGMPL_DIRECTIVE-2230`
- **ścieżka:** `.python_packages/matplotlib/sphinxext/figmpl_directive.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.751`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/sphinxext/figmpl_directive.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.751 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_PERMISSION`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.453718`
- **R₃:** `0.541785`
- **R₆:** `0.466054`
- **R₉:** `0.529069`
- **potencjal_kappa:** `0.025212`
- **masa_semantyczna:** `0.161862`
- **rodzaj_karty:** `0.285369`


## Rola
Add a ``figure-mpl`` directive that is a responsive version of ``figure``.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** figmplnode, FigureMpl
- **funkcje:** `_parse_srcsetNodes`, `_copy_images_figmpl`, `visit_figmpl_html`, `visit_figmpl_latex`, `depart_figmpl_html`, `depart_figmpl_latex`, `figurempl_addnode`, `setup`, `run`

## Opis
Add a ``figure-mpl`` directive that is a responsive version of ``figure``.

This implementation is very similar to ``.. figure::``, except it also allows a
``srcset=`` argument to be passed to the image tag, hence allowing responsive
resolution images.

There is no particular reason this could not be used standalone, but is meant
to be used with :doc:`/api/sphinxext_plot_directive_api`.

Note that
