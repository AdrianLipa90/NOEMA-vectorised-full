# consolidate_raw_logs_to_tsm.py — scripts/consolidate_raw_logs_to_tsm.py

## Tożsamość
- **id_karty:** `REPO-CONSOLIDATE_RAW_LOGS-566E`
- **ścieżka:** `scripts/consolidate_raw_logs_to_tsm.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.786`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/consolidate_raw_logs_to_tsm.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.786 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

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
Bridge raw chat logs → TSM via CIELingo frame.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_phase_from_text`, `_w_s`, `_ensure_schema`, `_ensure_raw_schema`, `store_live_prompt`, `store_live_response`, `consolidate_session`, `_normalise_space`, `_keywords`, `_deterministic_compression`, `_chunk_text`, `_iter_raw_log_files`, `consolidate_raw_log_files`, `audit_tsm_raw_log_consolidation`, `main`

## Opis
Bridge raw chat logs → TSM via CIELingo frame.

Usage:
    # Historical: consolidate archives into TSM
    python scripts/consolidate_raw_logs_to_tsm.py
    python scripts/consolidate_raw_logs_to_tsm.py --source opencode --limit 3

    # Live: store a single prompt+analysis+response in raw DB (for portal Memory Hub)
    python scripts/consolidate_raw_logs_to_tsm.py --live \
        --prompt "hello
