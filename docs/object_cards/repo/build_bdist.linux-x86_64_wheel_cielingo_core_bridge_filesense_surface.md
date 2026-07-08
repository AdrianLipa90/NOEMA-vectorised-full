# filesense_surface.py — build/bdist.linux-x86_64/wheel/cielingo_core/bridge/filesense_surface.py

## Tożsamość
- **id_karty:** `REPO-FILESENSE_SURFACE-C67B`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo_core/bridge/filesense_surface.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.506`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo_core/bridge/filesense_surface.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.506 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
FileSense surface for CIELingo GLOBAL v0.4.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** FileSenseHit, FileSenseReport, FileSenseSurface
- **funkcje:** `to_dict`, `to_dict`, `iter_text_files`, `score_line`, `search`, `load_jsonl`, `search_cards`

## Opis
FileSense surface for CIELingo GLOBAL v0.4.

FileSense is treated as a fast search/execution surface:
- local file scanning,
- grep-like retrieval,
- JSONL card loading,
- no SOURCE promotion,
- no NOEMA CURRENT update,
- no memory writeback.

This module is intentionally dependency-free. It can use Python fallback
search everywhere; shell grep/rg can be added later behind the same ABI.
