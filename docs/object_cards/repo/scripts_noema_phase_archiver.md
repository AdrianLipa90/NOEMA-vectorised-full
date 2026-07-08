# noema_phase_archiver.py — scripts/noema_phase_archiver.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_PHASE_ARCHIVER-76A8`
- **ścieżka:** `scripts/noema_phase_archiver.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `5.310`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_phase_archiver.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 5.310 |
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
NOEMA Phase Archiver — capture surface state snapshots to persistent storage.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_ensure_h5`, `_create_datasets`, `_ensure_npz`, `write_snapshot`, `snapshot_once`, `run_daemon`, `_stop`

## Opis
NOEMA Phase Archiver — capture surface state snapshots to persistent storage.

Reads the live NOEMA surface from /dev/shm/ciel_noema every N ticks and
archives to HDF5 on the phase data drive.

Usage:
    .venv/bin/python3 scripts/noema_phase_archiver.py          # daemon mode
    .venv/bin/python3 scripts/noema_phase_archiver.py --once   # single snapshot
    .venv/bin/python3 scripts/noema_phase
