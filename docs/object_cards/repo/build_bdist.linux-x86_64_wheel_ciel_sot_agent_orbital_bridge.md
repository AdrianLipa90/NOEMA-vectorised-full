# orbital_bridge.py — build/bdist.linux-x86_64/wheel/ciel_sot_agent/orbital_bridge.py

## Tożsamość
- **id_karty:** `REPO-ORBITAL_BRIDGE-F13F`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_sot_agent/orbital_bridge.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.883`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_sot_agent/orbital_bridge.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.883 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MEMORY`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.481637`
- **R₃:** `0.436994`
- **R₆:** `0.50573`
- **R₉:** `0.517955`
- **potencjal_kappa:** `0.179117`
- **masa_semantyczna:** `0.012321`
- **rodzaj_karty:** `0.236997`


## Rola
Orbital bridge — runs the global orbital coherence pass and writes

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_load_json_if_exists`, `_build_sync_manifest`, `_build_runtime_gating`, `_bridge_markdown`, `build_orbital_bridge`, `main`

## Opis
Orbital bridge — runs the global orbital coherence pass and writes
bridge state, health, and control-recommendation manifests.

Connects the CIEL integration kernel to the Orbital diagnostic subsystem
living under ``integration/Orbital/``, ensuring phase-coherence and
resource health are reported at each synchronisation cycle.

After the orbital physics pass the bridge routes the resulting state t
