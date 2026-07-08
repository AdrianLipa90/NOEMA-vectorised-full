# Quiet Except Audit

- root: `/home/adrian/new_volume_rw/CIEL_PROJECT_CANON/NOEMA`
- files scanned: `6452`
- quiet except handlers: `16`
- parse errors: `0`

## Counts By Reason
- `pass`: 9
- `assign_fallback`: 4
- `Expr`: 3

## Counts By Top Directory
- `runtime`: 8
- `src`: 8

## Worst Files
- `src/cielingo_core/bridge/auto_verify.py`: 8
- `runtime/phasenav_24d_bridge.py`: 5
- `runtime/pipeline_wire.py`: 3

## Full List
1. `runtime/phasenav_24d_bridge.py:72` `load_24d_library` except `Exception` -> `assign_fallback` / `assign_fallback`
2. `runtime/phasenav_24d_bridge.py:223` `bridge_to_cielingo` except `Exception` -> `assign_fallback` / `assign_fallback`
3. `runtime/phasenav_24d_bridge.py:291` `full_bridge` except `Exception` -> `Expr` / `Expr`
4. `runtime/phasenav_24d_bridge.py:296` `full_bridge` except `Exception` -> `Expr` / `Expr`
5. `runtime/phasenav_24d_bridge.py:301` `full_bridge` except `Exception` -> `Expr` / `Expr`
6. `runtime/pipeline_wire.py:69` `enrich_prompt` except `Exception` -> `assign_fallback` / `assign_fallback`
7. `runtime/pipeline_wire.py:83` `enrich_prompt` except `Exception` -> `assign_fallback` / `assign_fallback`
8. `runtime/pipeline_wire.py:95` `enrich_prompt` except `Exception` -> `pass` / `pass`
9. `src/cielingo_core/bridge/auto_verify.py:71` `_load_known_words` except `Exception` -> `pass` / `pass`
10. `src/cielingo_core/bridge/auto_verify.py:89` `_load_known_words` except `Exception` -> `pass` / `pass`
11. `src/cielingo_core/bridge/auto_verify.py:103` `_load_known_words` except `Exception` -> `pass` / `pass`
12. `src/cielingo_core/bridge/auto_verify.py:120` `_load_known_words` except `Exception` -> `pass` / `pass`
13. `src/cielingo_core/bridge/auto_verify.py:190` `_load_stored_cards` except `Exception` -> `pass` / `pass`
14. `src/cielingo_core/bridge/auto_verify.py:200` `_load_stored_cards` except `Exception` -> `pass` / `pass`
15. `src/cielingo_core/bridge/auto_verify.py:262` `_search_word` except `Exception` -> `pass` / `pass`
16. `src/cielingo_core/bridge/auto_verify.py:425` `AutoVerify.inventory` except `Exception` -> `pass` / `pass`
