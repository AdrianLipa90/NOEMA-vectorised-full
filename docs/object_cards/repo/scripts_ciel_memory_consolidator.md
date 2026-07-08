# ciel_memory_consolidator.py — scripts/ciel_memory_consolidator.py

## Tożsamość
- **id_karty:** `REPO-CIEL_MEMORY_CONSOLID-CAFC`
- **ścieżka:** `scripts/ciel_memory_consolidator.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `1.132`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_memory_consolidator.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 1.132 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `COMPOSITION`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.528337`
- **R₃:** `0.492776`
- **R₆:** `0.696453`
- **R₉:** `0.565583`
- **potencjal_kappa:** `0.185923`
- **masa_semantyczna:** `-0.141173`
- **rodzaj_karty:** `0.274318`


## Rola
CIEL Memory Consolidator — autonomiczny konsolidator wspomnień z bazą danych.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_resolve_memories_dir`, `_shared_server_alive`, `_shared_server_port_pids`, `_shared_server_health_ok`, `_shared_server_assessment`, `_ask_api_fallback_permission`, `_get_llm`, `_db_connect`, `init_db`, `_source_type`, `scan_and_register_files`, `get_pending_files`, `mark_file_done`, `reset_db`, `get_queue_summary`, `write_mirror`, `_query_via_server`, `_query_anthropic_api`, `_query_local_llm`, `_query_claude`, `_extract_keywords`, `_read_file_excerpt`, `_strip_thinking`, `_score_consolidation`, `_derive_failure_reason`, `_reconsolidation_prompt`, `_audit_consolidation_row`, `audit_consolidations`, `audit_failure_reasons`, `triage_failure_reason`

## Opis
CIEL Memory Consolidator — autonomiczny konsolidator wspomnień z bazą danych.

Baza danych SQLite (local_test/consolidator.db) śledzi:
  - które pliki zostały przetworzone
  - które czekają w kolejce
  - wyniki każdej konsolidacji

Mirror: local_test/mirror/ — kopie wyników pogrupowane wg źródła

Tryby:
  python3 ciel_memory_consolidator.py --once              # jednorazowy cykl
  python3 ciel_mem
