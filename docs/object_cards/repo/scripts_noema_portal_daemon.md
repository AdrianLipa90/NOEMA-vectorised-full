# noema_portal_daemon.py — scripts/noema_portal_daemon.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_PORTAL_DAEMON-7CF2`
- **ścieżka:** `scripts/noema_portal_daemon.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.788`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_portal_daemon.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.788 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `ORDER`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.408132`
- **R₃:** `0.527143`
- **R₆:** `0.447287`
- **R₉:** `0.516074`
- **potencjal_kappa:** `0.213299`
- **masa_semantyczna:** `0.199346`
- **rodzaj_karty:** `0.279908`


## Rola
NOEMA Portal Daemon — żywy interfejs systemu NOEMA.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** PortalHandler
- **funkcje:** `_get_embeddings`, `init_noema`, `read_surface_value`, `read_mmap_array`, `_read_analog_bus`, `_read_ciel_state`, `_read_agent_hint`, `_read_linux_load`, `_read_cards_index`, `_read_gravity`, `build_bloch_payload`, `scan_registry`, `heartbeat_loop`, `run_daemon`, `_read_1d`, `do_GET`, `_json`, `log_message`, `do_POST`, `do_PUT`, `do_DELETE`, `_stop`, `_get_tp`, `_get_arr`, `deep_merge`

## Opis
NOEMA Portal Daemon — żywy interfejs systemu NOEMA.

Zamiast surowego python3 -m http.server:
  - Rejestracja w daemon registry + heartbeat
  - Surface mmap przez ensure_surface()
  - REST API: /api/live, /api/status, /api/health, /api/metrics/all
  - Serwuje pliki statyczne z site/ na 18888
  - Systemd: noema-portal.service

Usage:
  noema_portal_daemon.py [--port PORT]
