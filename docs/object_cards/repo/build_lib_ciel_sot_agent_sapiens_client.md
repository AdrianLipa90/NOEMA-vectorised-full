# sapiens_client.py — build/lib/ciel_sot_agent/sapiens_client.py

## Tożsamość
- **id_karty:** `REPO-SAPIENS_CLIENT-5DF0`
- **ścieżka:** `build/lib/ciel_sot_agent/sapiens_client.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.086`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_sot_agent/sapiens_client.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.086 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `UNRUH_DRIVE`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.695214`
- **R₃:** `0.356299`
- **R₆:** `0.471302`
- **R₉:** `0.535169`
- **potencjal_kappa:** `0.138014`
- **masa_semantyczna:** `0.204514`
- **rodzaj_karty:** `0.244249`


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
