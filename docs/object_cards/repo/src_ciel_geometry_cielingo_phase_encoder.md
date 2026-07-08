# cielingo_phase_encoder.py — src/ciel_geometry/cielingo_phase_encoder.py

## Tożsamość
- **id_karty:** `REPO-CIELINGO_PHASE_ENCOD-9187`
- **ścieżka:** `src/ciel_geometry/cielingo_phase_encoder.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `0.874`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/cielingo_phase_encoder.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 0.874 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

## PhaseNav
- **operator:** `FOLD`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.351212`
- **R₃:** `0.661831`
- **R₆:** `0.649218`
- **R₉:** `0.522246`
- **potencjal_kappa:** `-0.135067`
- **masa_semantyczna:** `-0.137397`
- **rodzaj_karty:** `0.29302`


## Rola
CIELingo Phase Encoder — mapuje język na 36D konfigurację oscylatorów.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** —
- **funkcje:** `_resolve_group`, `_token_to_phase_config`, `encode_text_to_phases`, `_get_base_phases`, `_tokenize`, `fast_encode_text`, `_phases_from_frame`, `encode_and_write`, `decode_phases_to_frame`

## Opis
CIELingo Phase Encoder — mapuje język na 36D konfigurację oscylatorów.

Architektura:
  Text → build_lingo_frame() → tokeny z phase_rad, semantic_axes, semantic_mass
    → OSCILLATOR_GROUP_MAP (semantic_axes → M0-M11)
    → agregacja: 36D φ + 36×36 g coupling
    → surface mmap write → Kuramoto ewolucja = "myślenie"

Usage:
    from ciel_geometry.cielingo_phase_encoder import encode_text_to_phase
