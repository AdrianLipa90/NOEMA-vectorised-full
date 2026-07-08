# multiskill.py — src/ciel_geometry/multiskill.py

## Tożsamość
- **id_karty:** `REPO-MULTISKILL-5D93`
- **ścieżka:** `src/ciel_geometry/multiskill.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `0.638`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/multiskill.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 0.638 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

## PhaseNav
- **operator:** `CONSENT`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.382156`
- **R₃:** `0.389068`
- **R₆:** `0.420273`
- **R₉:** `0.412754`
- **potencjal_kappa:** `-0.014557`
- **masa_semantyczna:** `0.231183`
- **rodzaj_karty:** `0.291598`


## Rola
MultiskillOrchestrator — 291 skilli jako 36D PhaseNav + kompozycja.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** MultiskillOrchestrator
- **funkcje:** `_text_to_phi`, `_load`, `count`, `resolve`, `resolve_chain`, `neighbors`, `cluster`, `save_index`, `describe`

## Opis
MultiskillOrchestrator — 291 skilli jako 36D PhaseNav + kompozycja.

Każdy skill → 36D wektor fazy (jak library_index).
Multiskill = najbliższe wektory w przestrzeni PhaseNav spięte przez operator edges.
