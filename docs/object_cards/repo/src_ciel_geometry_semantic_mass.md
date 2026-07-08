# semantic_mass.py — src/ciel_geometry/semantic_mass.py

## Tożsamość
- **id_karty:** `REPO-SEMANTIC_MASS-FB36`
- **ścieżka:** `src/ciel_geometry/semantic_mass.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `0.920`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/semantic_mass.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 0.920 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

## PhaseNav
- **operator:** `FOLD`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.351212`
- **R₃:** `0.661831`
- **R₆:** `0.649218`
- **R₉:** `0.522246`
- **potencjal_kappa:** `-0.135067`
- **masa_semantyczna:** `-0.137397`
- **rodzaj_karty:** `0.29302`


## Rola
Semantic mass operator — Foundation Pack P3.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** SemanticMassRecord
- **funkcje:** `compute_sector_mass`, `compute_entity_mass`, `compute_repo_mass`, `build_mass_table`, `fuse_semantic_mass`

## Opis
Semantic mass operator — Foundation Pack P3.

M_sem(f) = α·M_EC(f) + β·M_ZS(f) + χ·C_dep(f) + δ·C_prov(f) + ε·C_exec(f)
         + ζ·C_nov(f) + ξ·C_conf(f)

For sectors and entities we proxy the components from available data:
  M_EC  — Euler-Collatz mass: based on info_mass and coupling strength (closure affinity)
  M_ZS  — Zeta-Schrödinger mass: based on coherence_weight and spectral resonance (
