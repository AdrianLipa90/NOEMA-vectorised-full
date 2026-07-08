# noema_self_model.py — scripts/noema_self_model.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_SELF_MODEL-07B5`
- **ścieżka:** `scripts/noema_self_model.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `4.757`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_self_model.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 4.757 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

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
NOEMA Self-Model — continuous self-reflection daemon.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** SelfModelDB
- **funkcje:** `compute_snapshot_metrics`, `detect_anomalies`, `run_cycle`, `main`, `open`, `close`, `_ensure_schema`, `write_snapshot`, `update_baseline`, `get_baseline_stats`, `write_drift`, `get_recent_snapshots`

## Opis
NOEMA Self-Model — continuous self-reflection daemon.

Monitoruje własną trajektorię NOEMY: snapshotuje stan powierzchni co 60s,
porównuje z baseline'em, wykrywa dryft i anomalie, zapisuje historię.

Architektura:
  ┌──────────────────┐    co 60s    ┌─────────────────────┐
  │ NOEMA surface    │ ──────────→  │ SelfModel daemon   │
  │ (mmap /dev/shm)  │              │                     │
  └────
