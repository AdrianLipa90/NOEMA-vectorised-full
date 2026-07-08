# nbody_gravity.py — build/lib/ciel_geometry/nbody_gravity.py

## Tożsamość
- **id_karty:** `REPO-NBODY_GRAVITY-260C`
- **ścieżka:** `build/lib/ciel_geometry/nbody_gravity.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.857`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_geometry/nbody_gravity.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.857 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `UNRUH_DRIVE`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.695214`
- **R₃:** `0.356299`
- **R₆:** `0.471302`
- **R₉:** `0.535169`
- **potencjal_kappa:** `0.138014`
- **masa_semantyczna:** `0.204514`
- **rodzaj_karty:** `0.244249`


## Rola
N-body Newtonian gravitational engine for CIEL orbital dynamics.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

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
