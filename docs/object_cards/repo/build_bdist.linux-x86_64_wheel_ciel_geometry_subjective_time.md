# subjective_time.py — build/bdist.linux-x86_64/wheel/ciel_geometry/subjective_time.py

## Tożsamość
- **id_karty:** `REPO-SUBJECTIVE_TIME-5F96`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_geometry/subjective_time.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.798`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_geometry/subjective_time.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.798 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RISK`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.594265`
- **R₃:** `0.468144`
- **R₆:** `0.457554`
- **R₉:** `0.414103`
- **potencjal_kappa:** `0.19508`
- **masa_semantyczna:** `-0.03873`
- **rodzaj_karty:** `0.279007`


## Rola
Subjective time operator — Foundation Pack P3.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

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
