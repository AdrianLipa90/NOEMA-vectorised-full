# cielingo_phase_memory.py — src/ciel_geometry/cielingo_phase_memory.py

## Tożsamość
- **id_karty:** `REPO-CIELINGO_PHASE_MEMOR-0232`
- **ścieżka:** `src/ciel_geometry/cielingo_phase_memory.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `5.152`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/cielingo_phase_memory.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 5.152 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

## PhaseNav
- **operator:** `AFFECT`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.542195`
- **R₃:** `0.629813`
- **R₆:** `0.534142`
- **R₉:** `0.565106`
- **potencjal_kappa:** `0.141102`
- **masa_semantyczna:** `0.203631`
- **rodzaj_karty:** `0.326785`


## Rola
CIELingo Phase Memory — asocjacyjna pamięć fazowa dla modelu językowego.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** PhaseMemory
- **funkcje:** `save`, `load_or_create`, `_load`, `add`, `_evict_oldest`, `query`, `query_by_text`, `blend`, `explore`, `size`, `coverage`, `stats`

## Opis
CIELingo Phase Memory — asocjacyjna pamięć fazowa dla modelu językowego.

Architektura:
  (text, φ_36) pary przechowywane w numpy array
  Szybkie wyszukiwanie przez cos similarity w 36D
  Persistent storage przez JSON/NPZ
  Online learning: CIELingo sync daemon może dodawać nowe pary

Usage:
    from ciel_geometry.cielingo_phase_memory import PhaseMemory
    pm = PhaseMemory.load_or_create("/tmp/c
