# phase_control.py — build/lib/integration/Orbital/main/phase_control.py

## Tożsamość
- **id_karty:** `REPO-PHASE_CONTROL-C40E`
- **ścieżka:** `build/lib/integration/Orbital/main/phase_control.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.256`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/integration/Orbital/main/phase_control.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.256 |
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
Phase control — integration layer re-export.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

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
