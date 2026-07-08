# agent.py — src/cielingo_core/noema_local_sot_agent/agent.py

## Tożsamość
- **id_karty:** `REPO-AGENT-818A`
- **ścieżka:** `src/cielingo_core/noema_local_sot_agent/agent.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.145`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/noema_local_sot_agent/agent.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.145 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
Local SOT_Agent backed by NoemaSurface.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** LocalSOTBoundary, LocalSOTAgentState, LocalSOTAgentNoemaSurface
- **funkcje:** `utc_now`, `canonical_json`, `sha256_text`, `to_dict`, `to_dict`, `current_path`, `event_log_path`, `canonize`, `discover`, `verify_current`, `_write_json`, `_append_event`

## Opis
Local SOT_Agent backed by NoemaSurface.

This module canonizes a *local* working branch as SOT_Agent_NoemaSurface.
It does not claim external NOEMA SoT, account-global GPT access, ACK, or
USER007 disk writeback. The word canon here means local artifact canon only.
