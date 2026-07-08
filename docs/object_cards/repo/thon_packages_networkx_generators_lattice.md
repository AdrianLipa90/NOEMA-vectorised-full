# lattice.py — .python_packages/networkx/generators/lattice.py

## Tożsamość
- **id_karty:** `REPO-LATTICE-8919`
- **ścieżka:** `.python_packages/networkx/generators/lattice.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.228`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/networkx/generators/lattice.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.228 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SOURCE`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.591319`
- **R₃:** `0.39689`
- **R₆:** `0.568492`
- **R₉:** `0.527911`
- **potencjal_kappa:** `0.015345`
- **masa_semantyczna:** `-0.142691`
- **rodzaj_karty:** `0.266598`


## Rola
Functions for generating grid graphs and lattices

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `grid_2d_graph`, `grid_graph`, `hypercube_graph`, `triangular_lattice_graph`, `hexagonal_lattice_graph`

## Opis
Functions for generating grid graphs and lattices

The :func:`grid_2d_graph`, :func:`triangular_lattice_graph`, and
:func:`hexagonal_lattice_graph` functions correspond to the three
`regular tilings of the plane`_, the square, triangular, and hexagonal
tilings, respectively. :func:`grid_graph` and :func:`hypercube_graph`
are similar for arbitrary dimensions. Useful relevant discussion can
be found
