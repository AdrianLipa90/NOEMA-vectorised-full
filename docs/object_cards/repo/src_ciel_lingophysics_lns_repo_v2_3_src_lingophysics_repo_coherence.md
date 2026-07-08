# repo_coherence.py — src/ciel_lingophysics_lns_repo_v2_3/src/lingophysics/repo_coherence.py

## Tożsamość
- **id_karty:** `REPO-REPO_COHERENCE-C331`
- **ścieżka:** `src/ciel_lingophysics_lns_repo_v2_3/src/lingophysics/repo_coherence.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.577`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/ciel_lingophysics_lns_repo_v2_3/src/lingophysics/repo_coherence.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.577 |
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
Repository coherence utilities for CIELingo v1.6.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `iter_files`, `classify_path`, `count_by_type`, `yaml_json_pair_audit`, `required_path_status`, `load_coherence_summary`

## Opis
Repository coherence utilities for CIELingo v1.6.

The module intentionally avoids heavyweight dependencies. It scans files,
classifies repository layers, audits YAML/JSON pairs, and checks required
paths. It is a repo-level safety rail: missing or unresolved objects should be
visible rather than silently absorbed.
