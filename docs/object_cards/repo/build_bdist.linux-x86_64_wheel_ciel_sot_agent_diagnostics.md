# diagnostics.py — build/bdist.linux-x86_64/wheel/ciel_sot_agent/diagnostics.py

## Tożsamość
- **id_karty:** `REPO-DIAGNOSTICS-4B1E`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_sot_agent/diagnostics.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.905`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_sot_agent/diagnostics.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.905 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
