# code_concept_bridge.py — src/noema_learned/code_concept_bridge.py

## Tożsamość
- **id_karty:** `REPO-CODE_CONCEPT_BRIDGE-E540`
- **ścieżka:** `src/noema_learned/code_concept_bridge.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.804`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/noema_learned/code_concept_bridge.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.804 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
NOEMA Code→Concept Bridge — mapuje kod Python na koncepty PhaseNav.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** CodeConcept
- **funkcje:** `_nearest_operator`, `_harmonic_fingerprint`, `analyze_code`, `seed_to_surface`, `surface_response`

## Opis
NOEMA Code→Concept Bridge — mapuje kod Python na koncepty PhaseNav.

Pipeline:
    AST → operator mapping → 24D concept vector → surface seeding → coherence check

Bez zależności poza numpy + stdlib. Żadnego CIELingo core.
