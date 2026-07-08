# laplacianmatrix.py — .python_packages/networkx/linalg/laplacianmatrix.py

## Tożsamość
- **id_karty:** `REPO-LAPLACIANMATRIX-3B13`
- **ścieżka:** `.python_packages/networkx/linalg/laplacianmatrix.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.842`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/networkx/linalg/laplacianmatrix.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.842 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ACTION_REQUEST`
- **odcisk_harmoniczny:** `LLHL`
- **R₁:** `0.419252`
- **R₃:** `0.442825`
- **R₆:** `0.60198`
- **R₉:** `0.41548`
- **potencjal_kappa:** `-0.118614`
- **masa_semantyczna:** `0.191681`
- **rodzaj_karty:** `0.278922`


## Rola
Laplacian matrix of graphs.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `laplacian_matrix`, `normalized_laplacian_matrix`, `directed_laplacian_matrix`, `directed_combinatorial_laplacian_matrix`, `_transition_matrix`

## Opis
Laplacian matrix of graphs.

All calculations here are done using the out-degree. For Laplacians using
in-degree, use `G.reverse(copy=False)` instead of `G` and take the transpose.

The `laplacian_matrix` function provides an unnormalized matrix,
while `normalized_laplacian_matrix`, `directed_laplacian_matrix`,
and `directed_combinatorial_laplacian_matrix` are all normalized.
