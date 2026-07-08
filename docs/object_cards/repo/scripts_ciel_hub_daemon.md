# ciel_hub_daemon.py — scripts/ciel_hub_daemon.py

## Tożsamość
- **id_karty:** `REPO-CIEL_HUB_DAEMON-1342`
- **ścieżka:** `scripts/ciel_hub_daemon.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `0.468`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_hub_daemon.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 0.468 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `BOUNDARY`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.587016`
- **R₃:** `0.481937`
- **R₆:** `0.525424`
- **R₉:** `0.380572`
- **potencjal_kappa:** `-0.130804`
- **masa_semantyczna:** `0.12548`
- **rodzaj_karty:** `0.280526`


## Rola
CIEL Server Hub Daemon — Phase 1.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `init_surface`, `read_mmap_array`, `_read_gravity`, `_read_analog_bus`, `_read_ciel_state`, `_read_agent_hint`, `_read_linux_load`, `scan_registry`, `_read_cards_index`, `hub_health`, `hub_snapshot`, `hub_contracts`, `ciel_state`, `ciel_identity`, `ciel_mode`, `noema_surface`, `noema_phase`, `noema_gravity`, `noema_daemons`, `noema_modules`, `api_live`, `api_bloch`, `api_metrics`, `api_metrics_all`, `api_status`, `api_status_summary`, `api_settings_get`, `api_settings_post`, `api_knowledge_stats`, `api_knowledge_search`

## Opis
CIEL Server Hub Daemon — Phase 1.

ThreadingHTTPServer + kontrakt API + snapshot cache.
Zastępuje noema_portal_daemon.py jako główny serwer huba.

Usage:
  ciel_hub_daemon.py [--port PORT] [--host HOST]
