# multiskill.py — build/lib/ciel_geometry/multiskill.py

## Tożsamość
- **id_karty:** `REPO-MULTISKILL-8814`
- **ścieżka:** `build/lib/ciel_geometry/multiskill.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.909`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_geometry/multiskill.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.909 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `IDENTITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.405566`
- **R₃:** `0.499333`
- **R₆:** `0.494094`
- **R₉:** `0.455981`
- **potencjal_kappa:** `0.08965`
- **masa_semantyczna:** `-0.024381`
- **rodzaj_karty:** `0.279273`


## Rola
MultiskillOrchestrator — 291 skilli jako 36D PhaseNav + kompozycja.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** MultiskillOrchestrator
- **funkcje:** `_text_to_phi`, `_load`, `count`, `resolve`, `resolve_chain`, `neighbors`, `cluster`, `save_index`, `describe`

## Opis
MultiskillOrchestrator — 291 skilli jako 36D PhaseNav + kompozycja.

Każdy skill → 36D wektor fazy (jak library_index).
Multiskill = najbliższe wektory w przestrzeni PhaseNav spięte przez operator edges.
