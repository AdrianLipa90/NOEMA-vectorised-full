# __init__.py — .python_packages/scipy/optimize/cython_optimize/__init__.py

## Tożsamość
- **id_karty:** `REPO-__INIT__-7B20`
- **ścieżka:** `.python_packages/scipy/optimize/cython_optimize/__init__.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.628`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/optimize/cython_optimize/__init__.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.628 |
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
Cython optimize root finding API

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** —

## Opis
Cython optimize root finding API
================================
The underlying C functions for the following root finders can be accessed
directly using Cython:

- `~scipy.optimize.bisect`
- `~scipy.optimize.ridder`
- `~scipy.optimize.brenth`
- `~scipy.optimize.brentq`

The Cython API for the root finding functions is similar except there is no
``disp`` argument. Import the root finding function
