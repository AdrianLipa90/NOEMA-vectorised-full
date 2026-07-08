# agent.py — build/bdist.linux-x86_64/wheel/cielingo_core/noema_local_sot_agent/agent.py

## Tożsamość
- **id_karty:** `REPO-AGENT-CEC4`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo_core/noema_local_sot_agent/agent.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.686`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo_core/noema_local_sot_agent/agent.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.686 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
