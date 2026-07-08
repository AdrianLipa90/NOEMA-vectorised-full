# build_file_wij.py — scripts/build_file_wij.py

## Tożsamość
- **id_karty:** `REPO-BUILD_FILE_WIJ-3200`
- **ścieżka:** `scripts/build_file_wij.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `0.031`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/build_file_wij.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 0.031 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

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
Build W_{ij} dependency graph for CIEL1 Python files.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_file_id`, `_collect_files`, `_extract_imports`, `_module_to_file`, `_build_module_index`, `_load_call_graph_centrality`, `_horizon_class`, `_euler_phase_metrics`, `_register_in_db`, `main`

## Opis
Build W_{ij} dependency graph for CIEL1 Python files.

Output:
  integration/registries/file_catalog.json   — per-file metadata + W_ij
  integration/registries/file_wij_graph.json — edge list
  nonlocal_graph.db                          — edges registered in nonlocal graph

Run from CIEL1 repo root:
  python3 scripts/build_file_wij.py
