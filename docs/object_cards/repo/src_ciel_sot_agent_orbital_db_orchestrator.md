# orbital_db_orchestrator.py — src/ciel_sot_agent/orbital_db_orchestrator.py

## Tożsamość
- **id_karty:** `REPO-ORBITAL_DB_ORCHESTRA-4569`
- **ścieżka:** `src/ciel_sot_agent/orbital_db_orchestrator.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `0.333`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/orbital_db_orchestrator.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 0.333 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

## PhaseNav
- **operator:** `CONSENT_REQUIRED`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.458017`
- **R₃:** `0.48995`
- **R₆:** `0.569953`
- **R₉:** `0.575041`
- **potencjal_kappa:** `-0.194917`
- **masa_semantyczna:** `0.103166`
- **rodzaj_karty:** `0.278924`


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
