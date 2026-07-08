# state_db.py — build/lib/ciel_sot_agent/state_db.py

## Tożsamość
- **id_karty:** `REPO-STATE_DB-3544`
- **ścieżka:** `build/lib/ciel_sot_agent/state_db.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.278`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_sot_agent/state_db.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.278 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CANON_BLOCK`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.593927`
- **R₃:** `0.544645`
- **R₆:** `0.483246`
- **R₉:** `0.501272`
- **potencjal_kappa:** `0.159378`
- **masa_semantyczna:** `-0.256779`
- **rodzaj_karty:** `0.332318`


## Rola
Unified SQLite state store for CIEL system.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `get_db`, `_ensure_schema`, `save_report`, `load_report`, `load_report_freshness`, `load_metrics_history`, `extract_lingo_metrics`, `save_orchestrator_state`, `load_orchestrator_state`, `load_holonomy`, `accumulate_berry`, `accumulate_subjective_winding`, `get_or_create_identity_seed`, `load_identity_seed`, `append_audit`, `_read_cycle_from_pickle`, `save_bridge_snapshot`, `db_path`

## Opis
Unified SQLite state store for CIEL system.

Single source of truth for: orchestrator state, M0-M8 metrics, JSON reports,
intentions, and metrics history. Replaces scattered pickle + 72 JSON files.

DB location: ~/.claude/ciel_state.db
WAL mode for concurrent read/write safety.
