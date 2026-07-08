# sapiens_client.py — src/ciel_sot_agent/sapiens_client.py

## Tożsamość
- **id_karty:** `REPO-SAPIENS_CLIENT-C391`
- **ścieżka:** `src/ciel_sot_agent/sapiens_client.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `4.322`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/sapiens_client.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 4.322 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

## PhaseNav
- **operator:** `ASSERTION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.563342`
- **R₃:** `0.601856`
- **R₆:** `0.54039`
- **R₉:** `0.584219`
- **potencjal_kappa:** `-0.098441`
- **masa_semantyczna:** `0.347732`
- **rodzaj_karty:** `0.261593`


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
