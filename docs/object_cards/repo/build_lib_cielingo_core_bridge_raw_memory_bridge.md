# raw_memory_bridge.py — build/lib/cielingo_core/bridge/raw_memory_bridge.py

## Tożsamość
- **id_karty:** `REPO-RAW_MEMORY_BRIDGE-9B87`
- **ścieżka:** `build/lib/cielingo_core/bridge/raw_memory_bridge.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.672`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo_core/bridge/raw_memory_bridge.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.672 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `BOUNDARY`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.587016`
- **R₃:** `0.481937`
- **R₆:** `0.525424`
- **R₉:** `0.380572`
- **potencjal_kappa:** `-0.130804`
- **masa_semantyczna:** `0.12548`
- **rodzaj_karty:** `0.280526`


## Rola
Raw Memory Bridge — cienki adapter do consolidate_raw_logs_to_tsm.py.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** CIELingoBridge, MemoryHub
- **funkcje:** `main`, `analyze`, `_detect_emotion`, `session_id`, `process_prompt`, `store_response`, `get_analysis`

## Opis
Raw Memory Bridge — cienki adapter do consolidate_raw_logs_to_tsm.py.

Zamiast osobnej bazy danych, deleguje do istniejącego pipeline'u:
  consolidate_raw_logs_to_tsm.py --live --prompt ... --response ... --analysis ...

Każda wiadomość:
  1. build_lingo_frame() przez CIELingoBridge
  2. consolidate_raw_logs_to_tsm.store_live_prompt() → raw DB
  3. Agent generuje odpowiedź → consolidate_raw_logs_t
