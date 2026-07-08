# transforms.py — .python_packages/numba/core/transforms.py

## Tożsamość
- **id_karty:** `REPO-TRANSFORMS-36B1`
- **ścieżka:** `.python_packages/numba/core/transforms.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.089`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/core/transforms.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.089 |
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
Implement transformation on Numba IR

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_extract_loop_lifting_candidates`, `find_region_inout_vars`, `_loop_lift_get_candidate_infos`, `_loop_lift_modify_call_block`, `_loop_lift_prepare_loop_func`, `_loop_lift_modify_blocks`, `_has_multiple_loop_exits`, `_pre_looplift_transform`, `loop_lifting`, `canonicalize_cfg_single_backedge`, `canonicalize_cfg`, `with_lifting`, `_get_with_contextmanager`, `_legalize_with_head`, `_cfg_nodes_in_region`, `find_setupwiths`, `_rewrite_return`, `_eliminate_nested_withs`, `consolidate_multi_exit_withs`, `_fix_multi_exit_blocks`, `same_exit_point`, `one_entry`, `cannot_yield`, `new_block_id`, `has_multiple_backedges`, `yield_loops_with_multiple_backedges`, `replace_target`, `rewrite_single_backedge`, `dispatcher_factory`, `get_var_dfn`

## Opis
Implement transformation on Numba IR
