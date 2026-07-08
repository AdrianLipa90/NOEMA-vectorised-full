# local.py — .python_packages/networkx/algorithms/community/local.py

## Tożsamość
- **id_karty:** `REPO-LOCAL-493D`
- **ścieżka:** `.python_packages/networkx/algorithms/community/local.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.923`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/networkx/algorithms/community/local.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.923 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `COMPOSITION`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.528337`
- **R₃:** `0.492776`
- **R₆:** `0.696453`
- **R₉:** `0.565583`
- **potencjal_kappa:** `0.185923`
- **masa_semantyczna:** `-0.141173`
- **rodzaj_karty:** `0.274318`


## Rola
Local Community Detection Algorithms

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_clauset_greedy_source_expansion`, `_calculate_local_modularity_for_candidate`, `greedy_source_expansion`

## Opis
Local Community Detection Algorithms

Local Community Detection (LCD) aims to detected one or a few communities
starting from certain source nodes in the network. This differs from Global
Community Detection (GCD), which aims to partition an entire network into
communities.

LCD is often useful when only a portion of the graph is known or the
graph is large enough that GCD is infeasable

[1]_ Give
