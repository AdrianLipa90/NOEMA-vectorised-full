# rh_control.py — integration/Orbital/main/rh_control.py

## Tożsamość
- **id_karty:** `REPO-RH_CONTROL-C73B`
- **ścieżka:** `integration/Orbital/main/rh_control.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.200`
- **φ (phi):** `1.229`
- **masa_semantyczna:** `0.90`

## Kotwice
- `integration/Orbital/main/rh_control.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.200 |
| φ | 1.229 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `orbital_bridge_core`.

## PhaseNav
- **operator:** `CONSENT_REQUIRED`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.458017`
- **R₃:** `0.48995`
- **R₆:** `0.569953`
- **R₉:** `0.575041`
- **potencjal_kappa:** `-0.194917`
- **masa_semantyczna:** `0.103166`
- **rodzaj_karty:** `0.278924`


## Rola
—

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** ThresholdProfile, RHDecision, RHController
- **funkcje:** `_obs`, `_phase_gap`, `effective_rh`, `validate`, `classify`, `evaluate`, `evaluate_snapshot`

## Opis
—
