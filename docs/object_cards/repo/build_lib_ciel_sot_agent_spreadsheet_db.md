# spreadsheet_db.py — build/lib/ciel_sot_agent/spreadsheet_db.py

## Tożsamość
- **id_karty:** `REPO-SPREADSHEET_DB-47A9`
- **ścieżka:** `build/lib/ciel_sot_agent/spreadsheet_db.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.122`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_sot_agent/spreadsheet_db.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.122 |
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
CIEL Spreadsheet DB — arkusze kalkulacyjne jako baza danych kart obiektów.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_xlsx_lock`, `_now_ts`, `_load_or_create`, `_ensure_sheet`, `_row_by_id`, `upsert_entity_card`, `append_htri_metrics`, `append_pipeline_metrics`, `append_cqcl_log`, `upsert_nonlocal_card`, `load_entity_cards`, `db_path`

## Opis
CIEL Spreadsheet DB — arkusze kalkulacyjne jako baza danych kart obiektów.

Każda kategoria kart to osobny arkusz w jednym pliku XLSX:
  integration/db/ciel_cards.xlsx

Arkusze:
  entity_cards   — karty bytów (id, noun, coupling, phase, horizon_class, adjectives, note)
  htri_metrics   — historia metryk HTRI (timestamp, coherence, n_threads, kappa)
  pipeline_metrics — historia pipeline (timestamp
