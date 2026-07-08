# cielingo_mcp_server.py — scripts/cielingo_mcp_server.py

## Tożsamość
- **id_karty:** `REPO-CIELINGO_MCP_SERVER-75DE`
- **ścieżka:** `scripts/cielingo_mcp_server.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `0.579`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/cielingo_mcp_server.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 0.579 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `FORCE`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.552175`
- **R₃:** `0.435218`
- **R₆:** `0.571397`
- **R₉:** `0.579087`
- **potencjal_kappa:** `0.300939`
- **masa_semantyczna:** `0.016845`
- **rodzaj_karty:** `0.260112`


## Rola
CIELingo MCP server — 7 narzędzi dla opencode przez JSON-RPC over stdio.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TimeoutError_R
- **funkcje:** `_get_knowledge`, `_get_sapiens`, `_tool`, `_binding_cdist`, `_handle_binding_status`, `_handle_knowledge_query`, `_handle_knowledge_coverage`, `_handle_agent_analyze`, `_handle_agent_health`, `_handle_surface_read`, `_handle_daemon_status`, `_handle_list_skills`, `_handle_sapiens_session`, `_handle_orchestrator_status`, `_handle_new_volume`, `_handle_linux_cards`, `_handle_linux_hardware`, `_send`, `_recv`, `main`, `_alarm`

## Opis
CIELingo MCP server — 7 narzędzi dla opencode przez JSON-RPC over stdio.

Usage:
    PYTHONPATH=src .venv/bin/python3 scripts/cielingo_mcp_server.py

Protocol: MCP JSON-RPC over stdio using Content-Length framing.
