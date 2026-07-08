# nbody_gravity.py — src/ciel_geometry/nbody_gravity.py

## Tożsamość
- **id_karty:** `REPO-NBODY_GRAVITY-F009`
- **ścieżka:** `src/ciel_geometry/nbody_gravity.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `0.327`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/nbody_gravity.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 0.327 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

## PhaseNav
- **operator:** `SOURCE_REQUIRED`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.509375`
- **R₃:** `0.557002`
- **R₆:** `0.453972`
- **R₉:** `0.573802`
- **potencjal_kappa:** `-0.191054`
- **masa_semantyczna:** `-0.307021`
- **rodzaj_karty:** `0.246226`


## Rola
N-body Newtonian gravitational engine for CIEL orbital dynamics.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** Body, NBodySystem
- **funkcje:** `from_mass_table`, `r`, `v`, `ke`, `add_body`, `_compute_accelerations`, `_total_potential`, `_total_kinetic`, `step`, `evolve`, `energy_error`, `orbital_elements`

## Opis
N-body Newtonian gravitational engine for CIEL orbital dynamics.

Extends the single-body Kepler III (T² = a³/M_sem) with pairwise
gravitational forces F_ij = -G_sem · M_i · M_j / r²_ij.

Uses leapfrog Verlet integration for symplectic stability.

G_sem is the semantic gravitational constant (dimensionless analog),
distinct from the physical G = 6.67430e-11 in ciel0_framework.py.
