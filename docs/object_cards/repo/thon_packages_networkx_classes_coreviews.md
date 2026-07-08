# coreviews.py — .python_packages/networkx/classes/coreviews.py

## Tożsamość
- **id_karty:** `REPO-COREVIEWS-385A`
- **ścieżka:** `.python_packages/networkx/classes/coreviews.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.244`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/networkx/classes/coreviews.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.244 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_OBLIGATION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.59271`
- **R₃:** `0.552945`
- **R₆:** `0.534582`
- **R₉:** `0.582078`
- **potencjal_kappa:** `0.23834`
- **masa_semantyczna:** `-0.091456`
- **rodzaj_karty:** `0.276031`


## Rola
Views of core data structures such as nested Mappings (e.g. dict-of-dicts).

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** AtlasView, AdjacencyView, MultiAdjacencyView, UnionAtlas, UnionAdjacency, UnionMultiInner, UnionMultiAdjacency, FilterAtlas, FilterAdjacency, FilterMultiInner, FilterMultiAdjacency
- **funkcje:** `copy`, `copy`, `copy`, `copy`, `copy`, `copy`, `new_node_ok`, `new_node_ok`, `edge_ok`

## Opis
Views of core data structures such as nested Mappings (e.g. dict-of-dicts).
These ``Views`` often restrict element access, with either the entire view or
layers of nested mappings being read-only.
