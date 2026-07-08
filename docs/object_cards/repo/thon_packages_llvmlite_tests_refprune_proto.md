# refprune_proto.py — .python_packages/llvmlite/tests/refprune_proto.py

## Tożsamość
- **id_karty:** `REPO-REFPRUNE_PROTO-ADF2`
- **ścieżka:** `.python_packages/llvmlite/tests/refprune_proto.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.493`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/llvmlite/tests/refprune_proto.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.493 |
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
Contains tests and a prototype implementation for the fanout algorithm in

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** FanoutAlgorithm
- **funkcje:** `case1`, `case2`, `case3`, `case4`, `case5`, `case6`, `case7`, `case8`, `case9`, `case10`, `case11`, `case12`, `case13`, `make_predecessor_map`, `check_once`, `check_all`, `run`, `_null_print`, `find_fanout_in_function`, `find_fanout`, `verify_non_overlapping`, `get_successors`, `get_predecessors`, `has_decref`, `walk_child_for_decref`, `find_decref_candidates`

## Opis
Contains tests and a prototype implementation for the fanout algorithm in
the LLVM refprune pass.
