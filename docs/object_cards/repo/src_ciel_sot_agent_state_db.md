# state_db.py — src/ciel_sot_agent/state_db.py

## Tożsamość
- **id_karty:** `REPO-STATE_DB-C876`
- **ścieżka:** `src/ciel_sot_agent/state_db.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `4.488`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/state_db.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 4.488 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

## PhaseNav
- **operator:** `ADDITION`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.662589`
- **R₃:** `0.614656`
- **R₆:** `0.542851`
- **R₉:** `0.417608`
- **potencjal_kappa:** `0.07638`
- **masa_semantyczna:** `0.206164`
- **rodzaj_karty:** `0.259027`


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
