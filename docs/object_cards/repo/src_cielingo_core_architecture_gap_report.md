# gap_report.py — src/cielingo_core/architecture/gap_report.py

## Tożsamość
- **id_karty:** `REPO-GAP_REPORT-B044`
- **ścieżka:** `src/cielingo_core/architecture/gap_report.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.912`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/architecture/gap_report.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.912 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CONDITION`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.577442`
- **R₃:** `0.440978`
- **R₆:** `0.50908`
- **R₉:** `0.325439`
- **potencjal_kappa:** `-0.091854`
- **masa_semantyczna:** `-0.064427`
- **rodzaj_karty:** `0.305875`


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
