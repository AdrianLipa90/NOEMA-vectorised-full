# orbital_db_orchestrator.py — build/lib/ciel_sot_agent/orbital_db_orchestrator.py

## Tożsamość
- **id_karty:** `REPO-ORBITAL_DB_ORCHESTRA-E616`
- **ścieżka:** `build/lib/ciel_sot_agent/orbital_db_orchestrator.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.528`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_sot_agent/orbital_db_orchestrator.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.528 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `UNCERTAINTY`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.435049`
- **R₃:** `0.572136`
- **R₆:** `0.544042`
- **R₉:** `0.477522`
- **potencjal_kappa:** `0.159902`
- **masa_semantyczna:** `-0.053674`
- **rodzaj_karty:** `0.279085`


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
