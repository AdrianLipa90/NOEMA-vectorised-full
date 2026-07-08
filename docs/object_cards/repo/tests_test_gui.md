# test_gui.py — tests/test_gui.py

## Tożsamość
- **id_karty:** `REPO-TEST_GUI-67C0`
- **ścieżka:** `tests/test_gui.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.300`
- **φ (phi):** `3.882`
- **masa_semantyczna:** `0.40`

## Kotwice
- `tests/test_gui.py`

## Atraktor
- **system:** `sync_core`
- **główny_atraktor:** orbital_bridge_core → ent_Mr_Ciel_Apocalyptos

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.300 |
| φ | 3.882 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `sync_core`.

## PhaseNav
- **operator:** `IDENTITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.405566`
- **R₃:** `0.499333`
- **R₆:** `0.494094`
- **R₉:** `0.455981`
- **potencjal_kappa:** `0.08965`
- **masa_semantyczna:** `-0.024381`
- **rodzaj_karty:** `0.279273`


## Rola
Tests for the Flask-based CIEL Quiet Orbital Control GUI.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem sync_core*
- **wyjście:** *wywnioskowane z folderu — podsystem sync_core*

## Zawartość
- **klasy:** TestIndexRoute, TestApiStatus, TestApiPanel, TestApiModels, TestApiContracts, TestErrorHandlers, TestAppFactory, TestGuiCaching, Result
- **funkcje:** `app`, `client`, `test_index_returns_200`, `test_index_returns_html`, `test_index_contains_ciel_brand`, `test_index_contains_nav_sections`, `test_index_contains_quiet_orbital_identity`, `test_status_returns_200`, `test_status_returns_json`, `test_status_schema`, `test_status_has_required_fields`, `test_status_coherence_is_float`, `test_status_health_is_float`, `test_panel_returns_200`, `test_panel_returns_json`, `test_panel_schema`, `test_panel_has_control_section`, `test_panel_has_communication_section`, `test_panel_has_support_section`, `test_models_returns_200_or_500`, `test_models_returns_json`, `test_models_has_schema_on_success`, `test_models_ensure_post_method_required`, `test_intentions_returns_canonical_shape`, `test_consolidator_results_returns_canonical_shape`, `test_critical_routes_are_unique`, `test_404_returns_json`, `test_create_app_with_explicit_root`, `test_create_app_debug_mode`, `test_create_app_registers_routes`

## Opis
Tests for the Flask-based CIEL Quiet Orbital Control GUI.

These tests use Flask's built-in test client and do not require a running
server.  They verify:
- App factory creates a valid Flask app
- All registered routes return expected HTTP status codes
- API endpoints return correct JSON schemas
- The index route renders HTML containing key UI elements
