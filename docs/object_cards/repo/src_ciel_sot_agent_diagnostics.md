# diagnostics.py — src/ciel_sot_agent/diagnostics.py

## Tożsamość
- **id_karty:** `REPO-DIAGNOSTICS-4B55`
- **ścieżka:** `src/ciel_sot_agent/diagnostics.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `1.814`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/diagnostics.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 1.814 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_OBLIGATION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.59271`
- **R₃:** `0.552945`
- **R₆:** `0.534582`
- **R₉:** `0.582078`
- **potencjal_kappa:** `0.23834`
- **masa_semantyczna:** `-0.091456`
- **rodzaj_karty:** `0.276031`


## Rola
CIEL system diagnostics — structural debt detector.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `check_attractor_rho`, `check_wij_in_holonomy`, `check_n_sectors_match`, `check_noema_card`, `check_purpose_field`, `run_diagnostics`, `diagnostics_summary_line`

## Opis
CIEL system diagnostics — structural debt detector.

Checks four known architectural debts and returns a compact report
suitable for injection into the session hook context string and
for appending to orbital_bridge_report.json.

Usage:
    from ciel_sot_agent.diagnostics import run_diagnostics
    report = run_diagnostics(root)          # dict
    summary = diagnostics_summary_line(report)  # one
