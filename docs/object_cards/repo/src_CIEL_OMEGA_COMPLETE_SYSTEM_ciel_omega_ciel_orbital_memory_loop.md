# orbital_memory_loop.py — src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/ciel/orbital_memory_loop.py

## Tożsamość
- **id_karty:** `REPO-ORBITAL_MEMORY_LOOP-0203`
- **ścieżka:** `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/ciel/orbital_memory_loop.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.150`
- **φ (phi):** `2.208`
- **masa_semantyczna:** `0.80`

## Kotwice
- `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/ciel/orbital_memory_loop.py`

## Atraktor
- **system:** `ciel_omega_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via ciel_omega_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.150 |
| φ | 2.208 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.80 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `ciel_omega_core`.

## PhaseNav
- **operator:** `SIMULATION_BOUNDARY`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.575665`
- **R₃:** `0.306554`
- **R₆:** `0.381064`
- **R₉:** `0.528951`
- **potencjal_kappa:** `-0.226686`
- **masa_semantyczna:** `-0.021063`
- **rodzaj_karty:** `0.269599`


## Rola
Bridge orbital diagnostics into runtime and durable memory.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem ciel_omega_core*
- **wyjście:** *wywnioskowane z folderu — podsystem ciel_omega_core*

## Zawartość
- **klasy:** RuntimeOrbitalSignals, OrbitalLoopConfig, OrbitalLoopResult
- **funkcje:** `_clamp`, `derive_runtime_orbital_params`, `run_orbital_loop`, `_coherence_flags`, `build_memory_meta`, `build_wave_attrs`, `build_runtime_policy`, `to_dict`

## Opis
Bridge orbital diagnostics into runtime and durable memory.

This module turns the previously detached orbital subsystem into a runtime loop:

input -> orbital snapshot -> control recommendation -> memory capture/promotion

The bridge is intentionally conservative:
- orbital failures never crash the engine; they are surfaced in-band,
- memory metadata carries topological health and policy state,
-
