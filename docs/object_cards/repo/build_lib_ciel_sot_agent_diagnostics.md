# diagnostics.py — build/lib/ciel_sot_agent/diagnostics.py

## Tożsamość
- **id_karty:** `REPO-DIAGNOSTICS-6159`
- **ścieżka:** `build/lib/ciel_sot_agent/diagnostics.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.137`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_sot_agent/diagnostics.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.137 |
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
