# temporalisomorphvf2.py — .python_packages/networkx/algorithms/isomorphism/temporalisomorphvf2.py

## Tożsamość
- **id_karty:** `REPO-TEMPORALISOMORPHVF2-D010`
- **ścieżka:** `.python_packages/networkx/algorithms/isomorphism/temporalisomorphvf2.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.840`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/networkx/algorithms/isomorphism/temporalisomorphvf2.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.840 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_PERMISSION`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.453718`
- **R₃:** `0.541785`
- **R₆:** `0.466054`
- **R₉:** `0.529069`
- **potencjal_kappa:** `0.025212`
- **masa_semantyczna:** `0.161862`
- **rodzaj_karty:** `0.285369`


## Rola
*****************************

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TimeRespectingGraphMatcher, TimeRespectingDiGraphMatcher
- **funkcje:** `one_hop`, `two_hop`, `semantic_feasibility`, `get_pred_dates`, `get_succ_dates`, `one_hop`, `two_hop_pred`, `two_hop_succ`, `preds`, `succs`, `test_one`, `test_two`, `semantic_feasibility`

## Opis
*****************************
Time-respecting VF2 Algorithm
*****************************

An extension of the VF2 algorithm for time-respecting graph isomorphism
testing in temporal graphs.

A temporal graph is one in which edges contain a datetime attribute,
denoting when interaction occurred between the incident nodes. A
time-respecting subgraph of a temporal graph is a subgraph such that
all i
