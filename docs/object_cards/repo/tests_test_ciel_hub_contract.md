# test_ciel_hub_contract.py — tests/test_ciel_hub_contract.py

## Tożsamość
- **id_karty:** `REPO-TEST_CIEL_HUB_CONTRA-77B7`
- **ścieżka:** `tests/test_ciel_hub_contract.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.300`
- **φ (phi):** `0.957`
- **masa_semantyczna:** `0.40`

## Kotwice
- `tests/test_ciel_hub_contract.py`

## Atraktor
- **system:** `sync_core`
- **główny_atraktor:** orbital_bridge_core → ent_Mr_Ciel_Apocalyptos

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.300 |
| φ | 0.957 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `sync_core`.

## PhaseNav
- **operator:** `ACTION_REQUEST`
- **odcisk_harmoniczny:** `LLHL`
- **R₁:** `0.419252`
- **R₃:** `0.442825`
- **R₆:** `0.60198`
- **R₉:** `0.41548`
- **potencjal_kappa:** `-0.118614`
- **masa_semantyczna:** `0.191681`
- **rodzaj_karty:** `0.278922`


## Rola
Testy kontraktu CIEL Server Hub — Phase 1.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem sync_core*
- **wyjście:** *wywnioskowane z folderu — podsystem sync_core*

## Zawartość
- **klasy:** TestResponseEnvelope, TestEndpointRegistry, TestEndpointParams, TestSnapshotCache, TestHubContractCoverage, TestStaticFileServing
- **funkcje:** `test_ok_has_all_fields`, `test_fail_has_all_fields`, `test_fail_multiple_errors`, `test_error_reply`, `test_ok_default_source`, `setUp`, `test_register_and_resolve`, `test_resolve_wrong_method`, `test_resolve_not_found`, `test_register_convenience_methods`, `test_list_endpoints`, `test_health_endpoint`, `setUp`, `test_int_param`, `test_str_param`, `test_no_match_wrong_type`, `test_short_path`, `test_long_path`, `setUp`, `test_register_and_get`, `test_get_unregistered`, `test_get_all`, `test_refresh_on_interval`, `test_error_handling`, `test_status`, `test_start_stop`, `test_unregister`, `setUp`, `test_all_frontend_endpoints_have_backend`, `test_health_endpoint_returns_ok`

## Opis
Testy kontraktu CIEL Server Hub — Phase 1.

Sprawdza:
1. Response envelope (ok/data/meta/errors)
2. Endpoint registry (rejestracja, resolve, params)
3. Snapshot cache (register, get, refresh)
4. Endpoint coverage — frontend vs backend
