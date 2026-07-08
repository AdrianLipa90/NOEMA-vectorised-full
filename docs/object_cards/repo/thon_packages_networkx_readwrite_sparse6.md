# sparse6.py — .python_packages/networkx/readwrite/sparse6.py

## Tożsamość
- **id_karty:** `REPO-SPARSE6-D6CE`
- **ścieżka:** `.python_packages/networkx/readwrite/sparse6.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.434`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/networkx/readwrite/sparse6.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.434 |
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
Functions for reading and writing graphs in the *sparse6* format.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_generate_sparse6_bytes`, `from_sparse6_bytes`, `to_sparse6_bytes`, `read_sparse6`, `write_sparse6`, `enc`, `parseData`

## Opis
Functions for reading and writing graphs in the *sparse6* format.

The *sparse6* file format is a space-efficient format for large sparse
graphs. For small graphs or large dense graphs, use the *graph6* file
format.

For more information, see the `sparse6`_ homepage.

.. _sparse6: https://users.cecs.anu.edu.au/~bdm/data/formats.html
