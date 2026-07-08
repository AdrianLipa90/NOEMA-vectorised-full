# _linesearch.py — .python_packages/scipy/optimize/_linesearch.py

## Tożsamość
- **id_karty:** `REPO-_LINESEARCH-B57F`
- **ścieżka:** `.python_packages/scipy/optimize/_linesearch.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.930`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/optimize/_linesearch.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.930 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `FORCE`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.552175`
- **R₃:** `0.435218`
- **R₆:** `0.571397`
- **R₉:** `0.579087`
- **potencjal_kappa:** `0.300939`
- **masa_semantyczna:** `0.016845`
- **rodzaj_karty:** `0.260112`


## Rola
Functions

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** LineSearchWarning
- **funkcje:** `_check_c1_c2`, `line_search_wolfe1`, `scalar_search_wolfe1`, `line_search_wolfe2`, `scalar_search_wolfe2`, `_cubicmin`, `_quadmin`, `_zoom`, `line_search_armijo`, `line_search_BFGS`, `scalar_search_armijo`, `_nonmonotone_line_search_cruz`, `_nonmonotone_line_search_cheng`, `phi`, `derphi`, `phi`, `derphi`, `phi`, `extra_condition2`, `extra_condition`

## Opis
Functions
---------
.. autosummary::
   :toctree: generated/

    line_search_armijo
    line_search_wolfe1
    line_search_wolfe2
    scalar_search_wolfe1
    scalar_search_wolfe2
