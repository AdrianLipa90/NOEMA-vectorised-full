# plot_directive.py — .python_packages/matplotlib/sphinxext/plot_directive.py

## Tożsamość
- **id_karty:** `REPO-PLOT_DIRECTIVE-92B9`
- **ścieżka:** `.python_packages/matplotlib/sphinxext/plot_directive.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.952`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/sphinxext/plot_directive.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.952 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CONDITION`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.577442`
- **R₃:** `0.440978`
- **R₆:** `0.50908`
- **R₉:** `0.325439`
- **potencjal_kappa:** `-0.091854`
- **masa_semantyczna:** `-0.064427`
- **rodzaj_karty:** `0.305875`


## Rola
A directive for including a Matplotlib plot in a Sphinx document

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** PlotDirective, _FilenameCollector, ImageFile, PlotError
- **funkcje:** `_option_boolean`, `_option_context`, `_option_format`, `mark_plot_labels`, `_copy_css_file`, `setup`, `init_filename_registry`, `contains_doctest`, `_split_code_at_show`, `out_of_date`, `_run_code`, `clear_state`, `get_plot_formats`, `_parse_srcset`, `check_output_base_name`, `render_figures`, `run`, `run`, `process_doc`, `clear_doc`, `merge_other`, `filename`, `filenames`, `out_of_date_one`

## Opis
A directive for including a Matplotlib plot in a Sphinx document
================================================================

This is a Sphinx extension providing a reStructuredText directive
``.. plot::`` for including a plot in a Sphinx document.

In HTML output, ``.. plot::`` will include a .png file with a link
to a high-res .png and .pdf.  In LaTeX output, it will include a .pdf.

The pl
