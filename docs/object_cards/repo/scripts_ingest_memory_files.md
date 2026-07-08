# ingest_memory_files.py — scripts/ingest_memory_files.py

## Tożsamość
- **id_karty:** `REPO-INGEST_MEMORY_FILES-9B42`
- **ścieżka:** `scripts/ingest_memory_files.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `1.685`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ingest_memory_files.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 1.685 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `QUESTION`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.394639`
- **R₃:** `0.763677`
- **R₆:** `0.521308`
- **R₉:** `0.466584`
- **potencjal_kappa:** `-0.203086`
- **masa_semantyczna:** `-0.0017`
- **rodzaj_karty:** `0.305584`


## Rola
Ingest all memory files (md, txt, json, jsonl, yaml, pdf, docx, db) into TSM.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_load_direct`, `_chunks`, `parse_md`, `parse_txt`, `parse_json`, `parse_jsonl`, `parse_yaml`, `parse_pdf`, `parse_docx`, `parse_db`, `collect_files`, `already_ingested`, `main`

## Opis
Ingest all memory files (md, txt, json, jsonl, yaml, pdf, docx, db) into TSM.

Parses each file into text chunks, encodes with CIELEncoder → phi_berry,
then stamps into holonomic_memory TSM (only new entries, never overwrites).

Usage:
    python3 scripts/ingest_memory_files.py [--dry-run] [--sources PATH ...]

Default sources:
    ~//media/adrian/New Volume1/CIEL_memories/          (md, jsonl, js
