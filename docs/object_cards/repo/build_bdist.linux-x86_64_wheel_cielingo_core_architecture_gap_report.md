# gap_report.py — build/bdist.linux-x86_64/wheel/cielingo_core/architecture/gap_report.py

## Tożsamość
- **id_karty:** `REPO-GAP_REPORT-02A6`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo_core/architecture/gap_report.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.762`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo_core/architecture/gap_report.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.762 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ORDER`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.408132`
- **R₃:** `0.527143`
- **R₆:** `0.447287`
- **R₉:** `0.516074`
- **potencjal_kappa:** `0.213299`
- **masa_semantyczna:** `0.199346`
- **rodzaj_karty:** `0.279908`


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
