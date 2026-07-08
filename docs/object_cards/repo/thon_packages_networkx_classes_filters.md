# filters.py — .python_packages/networkx/classes/filters.py

## Tożsamość
- **id_karty:** `REPO-FILTERS-DA79`
- **ścieżka:** `.python_packages/networkx/classes/filters.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.738`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/networkx/classes/filters.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.738 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SOURCE_REQUIRED`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.509375`
- **R₃:** `0.557002`
- **R₆:** `0.453972`
- **R₉:** `0.573802`
- **potencjal_kappa:** `-0.191054`
- **masa_semantyczna:** `-0.307021`
- **rodzaj_karty:** `0.246226`


## Rola
Filter factories to hide or show sets of nodes and edges.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** show_nodes
- **funkcje:** `no_filter`, `hide_nodes`, `hide_diedges`, `hide_edges`, `hide_multidiedges`, `hide_multiedges`, `show_diedges`, `show_edges`, `show_multidiedges`, `show_multiedges`

## Opis
Filter factories to hide or show sets of nodes and edges.

These filters return the function used when creating `SubGraph`.
