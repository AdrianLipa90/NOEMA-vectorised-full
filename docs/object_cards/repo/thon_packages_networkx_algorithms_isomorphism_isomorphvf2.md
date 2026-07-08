# isomorphvf2.py — .python_packages/networkx/algorithms/isomorphism/isomorphvf2.py

## Tożsamość
- **id_karty:** `REPO-ISOMORPHVF2-C3B5`
- **ścieżka:** `.python_packages/networkx/algorithms/isomorphism/isomorphvf2.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.180`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/networkx/algorithms/isomorphism/isomorphvf2.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.180 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `QUESTION`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.394639`
- **R₃:** `0.763677`
- **R₆:** `0.521308`
- **R₉:** `0.466584`
- **potencjal_kappa:** `-0.203086`
- **masa_semantyczna:** `-0.0017`
- **rodzaj_karty:** `0.305584`


## Rola
*************

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** GraphMatcher, DiGraphMatcher, GMState, DiGMState
- **funkcje:** `_is_directed_matcher`, `reset_recursion_limit`, `candidate_pairs_iter`, `initialize`, `is_isomorphic`, `isomorphisms_iter`, `match`, `semantic_feasibility`, `subgraph_is_isomorphic`, `subgraph_is_monomorphic`, `subgraph_isomorphisms_iter`, `subgraph_monomorphisms_iter`, `syntactic_feasibility`, `_is_directed_matcher`, `candidate_pairs_iter`, `initialize`, `syntactic_feasibility`, `subgraph_is_isomorphic`, `subgraph_is_monomorphic`, `subgraph_isomorphisms_iter`, `subgraph_monomorphisms_iter`, `restore`, `restore`

## Opis
*************
VF2 Algorithm
*************

An implementation of VF2 algorithm for graph isomorphism testing.

The simplest interface to use this module is to call the
:func:`is_isomorphic <networkx.algorithms.isomorphism.is_isomorphic>`
function.

Introduction
------------

The GraphMatcher and DiGraphMatcher are responsible for matching
graphs or directed graphs in a predetermined manner.  This
u
