# py_catalog.py — build/lib/ciel_sot_agent/py_catalog.py

## Tożsamość
- **id_karty:** `REPO-PY_CATALOG-FF6E`
- **ścieżka:** `build/lib/ciel_sot_agent/py_catalog.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.160`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_sot_agent/py_catalog.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.160 |
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
py_catalog — SQLite catalog of all .py files in the CIEL system.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_orbital_level`, `_msem_proxy`, `_tag_what`, `_tag_input`, `_tag_output`, `_tag_weight`, `_subsystem`, `_discover`, `_count_lines`, `_open_db`, `_rebuild_cooccurrence`, `build`, `_export_json`, `query`, `status`

## Opis
py_catalog — SQLite catalog of all .py files in the CIEL system.

Classifies ~600 real .py files using path and filename only (zero content reads).
Four tag dimensions: what / input / output / weight.
Tracks lines_of_code (wc -l), tag co-occurrence graph, and temporal delta.

Usage:
    python -m ciel_sot_agent.py_catalog --build
    python -m ciel_sot_agent.py_catalog --status
    python -m ciel_
