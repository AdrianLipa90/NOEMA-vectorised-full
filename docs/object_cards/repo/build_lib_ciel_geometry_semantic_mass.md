# semantic_mass.py — build/lib/ciel_geometry/semantic_mass.py

## Tożsamość
- **id_karty:** `REPO-SEMANTIC_MASS-EF15`
- **ścieżka:** `build/lib/ciel_geometry/semantic_mass.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.866`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_geometry/semantic_mass.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.866 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
Semantic mass operator — Foundation Pack P3.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

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
