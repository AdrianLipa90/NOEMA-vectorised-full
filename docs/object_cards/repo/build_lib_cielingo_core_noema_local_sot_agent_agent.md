# agent.py — build/lib/cielingo_core/noema_local_sot_agent/agent.py

## Tożsamość
- **id_karty:** `REPO-AGENT-5898`
- **ścieżka:** `build/lib/cielingo_core/noema_local_sot_agent/agent.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.533`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo_core/noema_local_sot_agent/agent.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.533 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `DIFFERENCE`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.563622`
- **R₃:** `0.51399`
- **R₆:** `0.516024`
- **R₉:** `0.447233`
- **potencjal_kappa:** `-0.196591`
- **masa_semantyczna:** `-0.06476`
- **rodzaj_karty:** `0.313562`


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
