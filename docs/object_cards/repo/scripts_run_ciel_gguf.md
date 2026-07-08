# run_ciel_gguf.py — scripts/run_ciel_gguf.py

## Tożsamość
- **id_karty:** `REPO-RUN_CIEL_GGUF-A4A9`
- **ścieżka:** `scripts/run_ciel_gguf.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `6.005`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/run_ciel_gguf.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 6.005 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `NEGATION`
- **odcisk_harmoniczny:** `LHLL`
- **R₁:** `0.425094`
- **R₃:** `0.614676`
- **R₆:** `0.450577`
- **R₉:** `0.387679`
- **potencjal_kappa:** `0.085998`
- **masa_semantyczna:** `-0.143065`
- **rodzaj_karty:** `0.271614`


## Rola
run_ciel_gguf.py — CIEL geometry + semantic algorithm injected into local GGUF.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_pull_ciel_metrics`, `_orbital_mode`, `_build_geometry_prompt`, `_find_model`, `main`, `_reply`

## Opis
run_ciel_gguf.py — CIEL geometry + semantic algorithm injected into local GGUF.

Usage:
    python scripts/run_ciel_gguf.py [--model PATH] [--prompt TEXT]

Pulls live CIEL metrics from the pipeline, builds a geometric system prompt
(Kähler manifold state, Berry holonomy, L_rel, orbital mode), and runs
inference on a local GGUF model.
