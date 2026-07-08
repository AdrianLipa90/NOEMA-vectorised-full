# orbital_db_orchestrator.py — build/bdist.linux-x86_64/wheel/ciel_sot_agent/orbital_db_orchestrator.py

## Tożsamość
- **id_karty:** `REPO-ORBITAL_DB_ORCHESTRA-5739`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_sot_agent/orbital_db_orchestrator.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.058`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_sot_agent/orbital_db_orchestrator.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.058 |
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
CIEL Orbital DB Orchestrator — wielki atraktor baz danych.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** DBStatus, OrbitalDBOrchestrator
- **funkcje:** `get_orchestrator`, `status`, `print_status`, `query_tsm`, `write_tsm`, `tsm_row_count`, `query_glossary`, `sync_wo`, `ingest`, `rebuild_noun_index`, `get_noun_index`, `top_words`, `full_sync`, `_tsm_conn`, `_sqlite_row_count`, `_json_count`, `_add`, `_tokenize`

## Opis
CIEL Orbital DB Orchestrator — wielki atraktor baz danych.

Jeden punkt dostępu do wszystkich baz w systemie CIEL.
Każda baza ma przypisaną masę orbitalną M_sem — im wyższa, tym wyższy priorytet
przy konfliktach i synchronizacji.

Bazy:
  TSM     — memory_ledger.db        (SQLite, M_sem~0.929) — pamięć semantyczna
  GLOSSARY— ciel_semantic_glossary  (SQLite, M_sem~0.860) — słownik kart
  WΩ      —
