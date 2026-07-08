# analysis.py — .python_packages/numba/core/analysis.py

## Tożsamość
- **id_karty:** `REPO-ANALYSIS-2024`
- **ścieżka:** `.python_packages/numba/core/analysis.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.729`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/core/analysis.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.729 |
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
Utils for IR analysis

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Unknown
- **funkcje:** `compute_use_defs`, `compute_live_map`, `compute_dead_maps`, `compute_live_variables`, `compute_cfg_from_blocks`, `find_top_level_loops`, `_fix_loop_exit`, `dead_branch_prune`, `rewrite_semantic_constants`, `find_literally_calls`, `must_use_alloca`, `fix_point_progress`, `fix_point`, `def_reach`, `liveness`, `fix_point_progress`, `find_branches`, `do_prune`, `prune_by_type`, `prune_by_value`, `prune_by_predicate`, `resolve_input_arg_const`, `rewrite_statement`, `rewrite_array_ndim`, `rewrite_tuple_len`

## Opis
Utils for IR analysis
