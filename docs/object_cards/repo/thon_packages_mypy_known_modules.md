# known_modules.py — .python_packages/mypy/known_modules.py

## Tożsamość
- **id_karty:** `REPO-KNOWN_MODULES-1124`
- **ścieżka:** `.python_packages/mypy/known_modules.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.263`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/known_modules.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.263 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ASSERTION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.563342`
- **R₃:** `0.601856`
- **R₆:** `0.54039`
- **R₉:** `0.584219`
- **potencjal_kappa:** `-0.098441`
- **masa_semantyczna:** `0.347732`
- **rodzaj_karty:** `0.261593`


## Rola
Known Python module names for fuzzy matching import suggestions.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `reset_known_modules_cache`, `get_stdlib_modules`, `get_known_modules`

## Opis
Known Python module names for fuzzy matching import suggestions.

This module provides a curated list of popular Python package import names
for suggesting corrections when a user mistypes an import statement.

Sources:
- Python standard library (typeshed/stdlib/VERSIONS)
- Top 100 PyPI packages by downloads (https://github.com/hugovk/top-pypi-packages)

Note: These are import names, not PyPI pack
