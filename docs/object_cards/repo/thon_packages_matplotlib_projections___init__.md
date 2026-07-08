# __init__.py — .python_packages/matplotlib/projections/__init__.py

## Tożsamość
- **id_karty:** `REPO-__INIT__-1AC5`
- **ścieżka:** `.python_packages/matplotlib/projections/__init__.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.793`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/projections/__init__.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.793 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `IDENTITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.405566`
- **R₃:** `0.499333`
- **R₆:** `0.494094`
- **R₉:** `0.455981`
- **potencjal_kappa:** `0.08965`
- **masa_semantyczna:** `-0.024381`
- **rodzaj_karty:** `0.279273`


## Rola
Non-separable transforms that map from data space to screen space.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ProjectionRegistry
- **funkcje:** `register_projection`, `get_projection_class`, `register`, `get_projection_class`, `get_projection_names`

## Opis
Non-separable transforms that map from data space to screen space.

Projections are defined as `~.axes.Axes` subclasses.  They include the
following elements:

- A transformation from data coordinates into display coordinates.

- An inverse of that transformation.  This is used, for example, to convert
  mouse positions from screen space back into data space.

- Transformations for the gridlines,
