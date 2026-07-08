# routes.py — src/ciel_sot_agent/gui/routes.py

## Tożsamość
- **id_karty:** `REPO-ROUTES-1286`
- **ścieżka:** `src/ciel_sot_agent/gui/routes.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `1.632`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/gui/routes.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 1.632 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

## PhaseNav
- **operator:** `QUESTION`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.394639`
- **R₃:** `0.763677`
- **R₆:** `0.521308`
- **R₉:** `0.466584`
- **potencjal_kappa:** `-0.203086`
- **masa_semantyczna:** `-0.0017`
- **rodzaj_karty:** `0.305584`


## Rola
Flask route handlers for the CIEL Quiet Orbital Control GUI.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_broadcast_sse`, `_scan_local_models`, `_find_gguf`, `_orbital_mode`, `_compute_groove_metrics`, `_load_wave_memory`, `_load_memory_stats`, `_load_repo_tensions`, `_load_pipeline_report`, `_is_small_model`, `_build_compact_prompt`, `_anchor_dialogue`, `_build_identity_preamble`, `_build_geometry_prompt`, `_parse_think_speak`, `_save_to_wave_archive`, `_handle_ciel_engine_message`, `_get_or_init_backend`, `_root`, `_load_orbital_bridge_report`, `_load_satellite_authority`, `_load_manifest`, `register_routes`, `index`, `_build_status_dict`, `api_sse_metrics`, `api_status`, `api_panel`, `api_models`, `api_models_ensure`

## Opis
Flask route handlers for the CIEL Quiet Orbital Control GUI.

Routes
------
GET  /               — Main dashboard (HTML)
GET  /api/status     — System status JSON (top status bar data)
GET  /api/panel      — Full panel state JSON
GET  /api/models     — Installed GGUF models JSON
POST /api/models/ensure  — Ensure the default model is installed (async-safe)
POST /api/chat/message  — Send message to
