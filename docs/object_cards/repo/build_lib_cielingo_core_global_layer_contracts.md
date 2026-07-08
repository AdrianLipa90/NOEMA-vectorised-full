# contracts.py — build/lib/cielingo_core/global_layer/contracts.py

## Tożsamość
- **id_karty:** `REPO-CONTRACTS-0EAB`
- **ścieżka:** `build/lib/cielingo_core/global_layer/contracts.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.200`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo_core/global_layer/contracts.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.200 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `COMPOSITION`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.528337`
- **R₃:** `0.492776`
- **R₆:** `0.696453`
- **R₉:** `0.565583`
- **potencjal_kappa:** `0.185923`
- **masa_semantyczna:** `-0.141173`
- **rodzaj_karty:** `0.274318`


## Rola
CIELingo clean-container contracts.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** SourceBindingType, EntryStatus, UniversalRole, UniversalOperatorType, LexicalSlot, LanguageSlotEntry, UniversalOperator, MeaningEquation, SlotProjection, AlignmentResidue, SurfaceSolution, HolonomicJReport, ApocalypOSLinguisticSignal
- **funkcje:** `_bounded01`, `validate`, `to_dict`, `validate`, `to_dict`, `validate`, `validate`, `to_dict`, `validate`, `validate`, `validate`, `J_total`, `validate`, `validate`

## Opis
CIELingo clean-container contracts.

This file defines the isolated Stage 0 ABI. It deliberately avoids importing
ApocalypOS, NOEMA, previous CIELingo modules, or language-specific solvers.

GLOBAL = algebra of slots, relations, equations, projections, residue and J.
REGIONAL = language-local grammar/holonomy, stored under language_spaces/*.
