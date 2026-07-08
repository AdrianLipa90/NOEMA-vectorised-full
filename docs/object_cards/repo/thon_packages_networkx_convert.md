# convert.py — .python_packages/networkx/convert.py

## Tożsamość
- **id_karty:** `REPO-CONVERT-0332`
- **ścieżka:** `.python_packages/networkx/convert.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.546`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/networkx/convert.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.546 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `BOUNDARY`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.587016`
- **R₃:** `0.481937`
- **R₆:** `0.525424`
- **R₉:** `0.380572`
- **potencjal_kappa:** `-0.130804`
- **masa_semantyczna:** `0.12548`
- **rodzaj_karty:** `0.280526`


## Rola
Functions to convert NetworkX graphs to and from other formats.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `to_networkx_graph`, `to_dict_of_lists`, `from_dict_of_lists`, `to_dict_of_dicts`, `from_dict_of_dicts`, `to_edgelist`, `from_edgelist`

## Opis
Functions to convert NetworkX graphs to and from other formats.

The preferred way of converting data to a NetworkX graph is through the
graph constructor.  The constructor calls the to_networkx_graph() function
which attempts to guess the input type and convert it automatically.

Examples
--------
Create a graph with a single edge from a dictionary of dictionaries

>>> d = {0: {1: 1}}  # dict-of-
