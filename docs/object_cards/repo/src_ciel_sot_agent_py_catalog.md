# py_catalog.py — src/ciel_sot_agent/py_catalog.py

## Tożsamość
- **id_karty:** `REPO-PY_CATALOG-F84F`
- **ścieżka:** `src/ciel_sot_agent/py_catalog.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `0.365`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/py_catalog.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 0.365 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

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
