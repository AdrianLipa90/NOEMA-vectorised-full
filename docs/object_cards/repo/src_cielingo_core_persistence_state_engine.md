# state_engine.py — src/cielingo_core/persistence/state_engine.py

## Tożsamość
- **id_karty:** `REPO-STATE_ENGINE-4AE0`
- **ścieżka:** `src/cielingo_core/persistence/state_engine.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.661`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/persistence/state_engine.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.661 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SIMULATION_BOUNDARY`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.575665`
- **R₃:** `0.306554`
- **R₆:** `0.381064`
- **R₉:** `0.528951`
- **potencjal_kappa:** `-0.226686`
- **masa_semantyczna:** `-0.021063`
- **rodzaj_karty:** `0.269599`


## Rola
—

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** CIELingoStateEngine
- **funkcje:** `_ensure_db`, `_db`, `save_loop`, `_save_scar`, `get_loops`, `get_scars`, `save_repair`, `resolve_repair`, `get_pending_repairs`, `log_experience`, `get_recent_experience`, `update_metric`, `get_metric`, `get_all_metrics`, `write_knowledge_relation`, `export_state`, `close`

## Opis
—
