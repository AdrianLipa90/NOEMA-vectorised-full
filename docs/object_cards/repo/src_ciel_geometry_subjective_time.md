# subjective_time.py — src/ciel_geometry/subjective_time.py

## Tożsamość
- **id_karty:** `REPO-SUBJECTIVE_TIME-389E`
- **ścieżka:** `src/ciel_geometry/subjective_time.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `4.802`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/subjective_time.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 4.802 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

## PhaseNav
- **operator:** `ACTION_REQUEST`
- **odcisk_harmoniczny:** `LLHL`
- **R₁:** `0.419252`
- **R₃:** `0.442825`
- **R₆:** `0.60198`
- **R₉:** `0.41548`
- **potencjal_kappa:** `-0.118614`
- **masa_semantyczna:** `0.191681`
- **rodzaj_karty:** `0.278922`


## Rola
Subjective time operator — Foundation Pack P3.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** SubjectiveTimeRecord
- **funkcje:** `orbit_index`, `_g`, `compute_subjective_times`, `compute_from_bridge`

## Opis
Subjective time operator — Foundation Pack P3.

Δτ_i(k) = Δt · g(r_i, C_i, Δ_i, m_i, A_i)

where:
  r_i  — Poincaré radius (orbit position, 0=center, 1=boundary)
  C_i  — coherence contribution of this entity
  Δ_i  — local holonomy defect contribution
  m_i  — semantic mass M_sem
  A_i  — attractor weight (coupling to system attractor)

g(r, C, Δ, m, A) = (1 / τ_ref) · (1 - r²) · (C / (1 + Δ)) ·
