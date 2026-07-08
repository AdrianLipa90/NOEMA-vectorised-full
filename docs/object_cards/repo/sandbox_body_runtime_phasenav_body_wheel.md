# phasenav_body_wheel.py — sandbox_body/runtime/phasenav_body_wheel.py

## Tożsamość
- **id_karty:** `REPO-PHASENAV_BODY_WHEEL-D5D4`
- **ścieżka:** `sandbox_body/runtime/phasenav_body_wheel.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.119`
- **masa_semantyczna:** `0.40`

## Kotwice
- `sandbox_body/runtime/phasenav_body_wheel.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.119 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `WARP_DRIFT`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.47403`
- **R₃:** `0.56672`
- **R₆:** `0.57902`
- **R₉:** `0.540967`
- **potencjal_kappa:** `0.057762`
- **masa_semantyczna:** `0.153958`
- **rodzaj_karty:** `0.289083`


## Rola
phasenav_body_wheel.py — PhaseNav Wheel Engine

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** PhaseNavEmbedder, PhaseNavWheel, WheelMemory, PhaseNavComposer, PhaseNavWheelEngine
- **funkcje:** `_build_operator_vectors`, `run_test`, `run_interactive`, `main`, `embed`, `operator_similarity`, `apply_operator`, `compute_coherence`, `compute_uncertainty`, `compute_semantic_mass`, `spin`, `query_by_phi`, `_embed_text`, `compose`, `process`

## Opis
phasenav_body_wheel.py — PhaseNav Wheel Engine

Offline cognition engine using PhaseNav 36D vector operations.
No LLM/API required — pure numpy + PhaseNav operator algebra.

The wheel is a cognitive cycle that rotates through operator phases:
  PRIME → CAUSE → FORCE → AFFECT → BIND → ATTRACTOR → WARP → EVALUATE → COMPOSE → SETTLE

Each phase applies the corresponding operator to evolve the 36D pha
