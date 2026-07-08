# gap_report.py — build/lib/cielingo_core/architecture/gap_report.py

## Tożsamość
- **id_karty:** `REPO-GAP_REPORT-CEEC`
- **ścieżka:** `build/lib/cielingo_core/architecture/gap_report.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.641`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo_core/architecture/gap_report.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.641 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `UNCERTAINTY`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.435049`
- **R₃:** `0.572136`
- **R₆:** `0.544042`
- **R₉:** `0.477522`
- **potencjal_kappa:** `0.159902`
- **masa_semantyczna:** `-0.053674`
- **rodzaj_karty:** `0.279085`


## Rola
Architecture Gap Map v1.1C.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** GapSeverity, GapType, ArchitectureGap, ArchitectureGapReport
- **funkcje:** `build_default_architecture_gap_report`, `validate`, `to_dict`, `severity_weight`, `validate`, `gap_load`, `blocker_count`, `expected_vs_actual_delta`, `to_dict`, `stable_hash`

## Opis
Architecture Gap Map v1.1C.

Maps actual state vs expected state for GLOBAL -> REGIONAL -> EXPRESSIVE
and reverse codecs.

This is an audit artifact, not SOURCE/canon/NOEMA writeback.
