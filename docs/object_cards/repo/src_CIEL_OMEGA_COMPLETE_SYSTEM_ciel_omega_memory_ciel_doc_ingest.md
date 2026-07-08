# ciel_doc_ingest.py — src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/ciel_doc_ingest.py

## Tożsamość
- **id_karty:** `REPO-CIEL_DOC_INGEST-DC43`
- **ścieżka:** `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/ciel_doc_ingest.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.150`
- **φ (phi):** `1.674`
- **masa_semantyczna:** `0.80`

## Kotwice
- `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/ciel_doc_ingest.py`

## Atraktor
- **system:** `ciel_omega_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via ciel_omega_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.150 |
| φ | 1.674 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.80 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `ciel_omega_core`.

## PhaseNav
- **operator:** `MODAL_PERMISSION`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.453718`
- **R₃:** `0.541785`
- **R₆:** `0.466054`
- **R₉:** `0.529069`
- **potencjal_kappa:** `0.025212`
- **masa_semantyczna:** `0.161862`
- **rodzaj_karty:** `0.285369`


## Rola
CIEL Document Ingestor — PDF / DOCX / MD / TXT → BlochEncoder online update.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem ciel_omega_core*
- **wyjście:** *wywnioskowane z folderu — podsystem ciel_omega_core*

## Zawartość
- **klasy:** —
- **funkcje:** `_apply_heisenberg_clip`, `_parse_txt`, `_parse_md`, `_parse_pdf`, `_parse_docx`, `_parse_file`, `_chunk_text`, `_write_chunks_to_tsm`, `_update_encoder`, `ingest_file`, `ingest_directory`

## Opis
CIEL Document Ingestor — PDF / DOCX / MD / TXT → BlochEncoder online update.

Parsuje dokumenty, segmentuje na chunki, wpina w online_update BlochEncodera.
Każdy chunk = jeden tekst do nauki. Chunki są też zapisywane do TSM jako
nowe wpisy pamięci (D_type='document').

Użycie:
    python -m ciel_doc_ingest /ścieżka/do/pliku.pdf
    python -m ciel_doc_ingest /ścieżka/do/folderu/

Lub z kodu:
    fr
