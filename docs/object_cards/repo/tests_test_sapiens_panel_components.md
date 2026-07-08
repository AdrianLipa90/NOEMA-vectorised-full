# test_sapiens_panel_components.py — tests/test_sapiens_panel_components.py

## Tożsamość
- **id_karty:** `REPO-TEST_SAPIENS_PANEL_C-B7F9`
- **ścieżka:** `tests/test_sapiens_panel_components.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.300`
- **φ (phi):** `4.251`
- **masa_semantyczna:** `0.40`

## Kotwice
- `tests/test_sapiens_panel_components.py`

## Atraktor
- **system:** `sync_core`
- **główny_atraktor:** orbital_bridge_core → ent_Mr_Ciel_Apocalyptos

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.300 |
| φ | 4.251 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `sync_core`.

## PhaseNav
- **operator:** `ADDITION`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.662589`
- **R₃:** `0.614656`
- **R₆:** `0.542851`
- **R₉:** `0.417608`
- **potencjal_kappa:** `0.07638`
- **masa_semantyczna:** `0.206164`
- **rodzaj_karty:** `0.259027`


## Rola
Extended tests for sapiens panel sub-modules that have no existing coverage.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem sync_core*
- **wyjście:** *wywnioskowane z folderu — podsystem sync_core*

## Zawartość
- **klasy:** —
- **funkcje:** `_bridge_summary`, `_session`, `test_build_support_view_contains_health_manifest`, `test_build_support_view_contains_recommended_control`, `test_build_support_view_contains_source_paths`, `test_build_support_view_includes_artifact_paths_when_provided`, `test_build_support_view_artifact_paths_empty_when_not_provided`, `test_build_support_view_includes_recommended_actions_list`, `_panel_state`, `test_to_render_dict_returns_dict`, `test_to_render_dict_contains_all_tabs`, `test_to_render_dict_control_title_preserved`, `test_to_render_dict_session_fields_present`, `test_build_communication_view_returns_packet`, `test_build_communication_view_latest_user_turn`, `test_build_communication_view_memory_excerpt_present`, `test_build_communication_view_turn_count_is_positive`, `test_build_reduction_state_returns_schema`, `test_build_reduction_state_readiness_score_in_unit_interval`, `test_build_reduction_state_reduction_ready_is_bool`, `test_build_reduction_state_memory_residue_has_identity_anchor`, `test_build_reduction_state_uses_custom_threshold`, `test_build_reduction_state_orchestration_state_present`

## Opis
Extended tests for sapiens panel sub-modules that have no existing coverage.

Covers:
  - sapiens_panel/support.py      (build_support_view)
  - sapiens_panel/render_schema.py (to_render_dict)
  - sapiens_panel/communication.py (build_communication_view)
  - sapiens_panel/reduction.py    (build_reduction_state)
