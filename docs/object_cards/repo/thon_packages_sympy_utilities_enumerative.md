# enumerative.py — .python_packages/sympy/utilities/enumerative.py

## Tożsamość
- **id_karty:** `REPO-ENUMERATIVE-03DC`
- **ścieżka:** `.python_packages/sympy/utilities/enumerative.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.786`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/utilities/enumerative.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.786 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CAUSE`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.440841`
- **R₃:** `0.698384`
- **R₆:** `0.560357`
- **R₉:** `0.385177`
- **potencjal_kappa:** `0.165796`
- **masa_semantyczna:** `0.077602`
- **rodzaj_karty:** `0.2472`


## Rola
Algorithms and classes to support enumerative combinatorics.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** PartComponent, MultisetPartitionTraverser
- **funkcje:** `multiset_partitions_taocp`, `factoring_visitor`, `list_visitor`, `part_key`, `db_trace`, `_initialize_enumeration`, `decrement_part`, `decrement_part_small`, `decrement_part_large`, `decrement_part_range`, `spread_part_multiplicity`, `top_part`, `enum_all`, `enum_small`, `enum_large`, `enum_range`, `count_partitions_slow`, `count_partitions`

## Opis
Algorithms and classes to support enumerative combinatorics.

Currently just multiset partitions, but more could be added.

Terminology (following Knuth, algorithm 7.1.2.5M TAOCP)
*multiset* aaabbcccc has a *partition* aaabc | bccc

The submultisets, aaabc and bccc of the partition are called
*parts*, or sometimes *vectors*.  (Knuth notes that multiset
partitions can be thought of as partitions of
