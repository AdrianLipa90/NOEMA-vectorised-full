# noema_audit_consolidator.py — scripts/noema_audit_consolidator.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_AUDIT_CONSOLID-DA1C`
- **ścieżka:** `scripts/noema_audit_consolidator.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `3.285`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_audit_consolidator.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 3.285 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

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
NOEMA Audit Consolidator — merge 3 audit systems into state_db.m8_audit.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_read_jsonl`, `_ensure_schema`, `_scan_cielingo_cards`, `_scan_writings_log`, `consolidate`, `snapshot_m8_to_state_db`

## Opis
NOEMA Audit Consolidator — merge 3 audit systems into state_db.m8_audit.

Reads:
  1. MemoryLog JSONL (CIEL_OMEGA/memory/memory_log.jsonl)
  2. M8 AuditJournalMemory (in-memory snapshot via CIEL pipeline)
  3. state_db.m8_audit (SQLite, canonical target)

Writes:
  - Consolidated to state_db.m8_audit with dedup by timestamp+event
  - Summary to stdout

Usage:
  python3 noema_audit_consolidator.py
