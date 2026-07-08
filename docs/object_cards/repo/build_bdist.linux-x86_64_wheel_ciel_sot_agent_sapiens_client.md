# sapiens_client.py — build/bdist.linux-x86_64/wheel/ciel_sot_agent/sapiens_client.py

## Tożsamość
- **id_karty:** `REPO-SAPIENS_CLIENT-EA10`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_sot_agent/sapiens_client.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.869`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_sot_agent/sapiens_client.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.869 |
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
Sapiens client — packet-aware human-model interaction interface.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** SapiensIdentity, SapiensTurn, SapiensSession
- **funkcje:** `_now`, `_state_geometry`, `_surface_policy`, `initialize_session`, `append_turn`, `build_model_packet`, `persist_session`, `run_sapiens_client`, `main`

## Opis
Sapiens client — packet-aware human-model interaction interface.

Builds, validates, and persists interaction packets between human operators
and the CIEL model layer.  Writes session transcripts and latest-packet
snapshots to ``integration/reports/sapiens_client/``.
