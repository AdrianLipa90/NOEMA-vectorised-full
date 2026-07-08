# mathmpl.py — .python_packages/matplotlib/sphinxext/mathmpl.py

## Tożsamość
- **id_karty:** `REPO-MATHMPL-6D45`
- **ścieżka:** `.python_packages/matplotlib/sphinxext/mathmpl.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.032`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/sphinxext/mathmpl.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.032 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `REFUSAL`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.441725`
- **R₃:** `0.537197`
- **R₆:** `0.362678`
- **R₉:** `0.509166`
- **potencjal_kappa:** `0.077364`
- **masa_semantyczna:** `-0.245874`
- **rodzaj_karty:** `0.27107`


## Rola
A role and directive to display mathtext in Sphinx

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** latex_math, MathDirective
- **funkcje:** `fontset_choice`, `math_role`, `latex2png`, `latex2html`, `_config_inited`, `setup`, `run`, `visit_latex_math_html`, `depart_latex_math_html`, `visit_latex_math_latex`, `depart_latex_math_latex`

## Opis
A role and directive to display mathtext in Sphinx
==================================================

The ``mathmpl`` Sphinx extension creates a mathtext image in Matplotlib and
shows it in html output. Thus, it is a true and faithful representation of what
you will see if you pass a given LaTeX string to Matplotlib (see
:ref:`mathtext`).

.. warning::
    In most cases, you will likely want to u
