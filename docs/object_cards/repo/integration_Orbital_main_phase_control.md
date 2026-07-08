# phase_control.py — integration/Orbital/main/phase_control.py

## Tożsamość
- **id_karty:** `REPO-PHASE_CONTROL-4E11`
- **ścieżka:** `integration/Orbital/main/phase_control.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.200`
- **φ (phi):** `3.547`
- **masa_semantyczna:** `0.90`

## Kotwice
- `integration/Orbital/main/phase_control.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.200 |
| φ | 3.547 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `orbital_bridge_core`.

## PhaseNav
- **operator:** `SCOPE`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.516458`
- **R₃:** `0.452404`
- **R₆:** `0.493743`
- **R₉:** `0.465851`
- **potencjal_kappa:** `0.026123`
- **masa_semantyczna:** `0.147985`
- **rodzaj_karty:** `0.241584`


## Rola
Phase control — integration layer re-export.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** —
- **funkcje:** `_obs`, `coherence_index_from_snapshot`, `topological_charge_global`, `phase_lock_error`, `mode_norm`, `_mode_from_psi`, `_continuous_params`, `recommend_control`, `build_state_manifest`, `build_health_manifest`

## Opis
Phase control — integration layer re-export.

Delegates to the canonical implementation in
``src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/orbital/phase_control``
when that package is on sys.path (i.e. after ciel_pipeline bootstraps it),
and falls back to the local copy otherwise so that orbital_bridge continues
to work standalone.

All callers (orbital_bridge, orbital_memory_loop, etc.) import from h
