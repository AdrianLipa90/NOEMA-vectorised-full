# inference_gate.py — src/ciel_lingophysics_lns_repo_v2_3/src/lingophysics/inference_gate.py

## Tożsamość
- **id_karty:** `REPO-INFERENCE_GATE-153B`
- **ścieżka:** `src/ciel_lingophysics_lns_repo_v2_3/src/lingophysics/inference_gate.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.201`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/ciel_lingophysics_lns_repo_v2_3/src/lingophysics/inference_gate.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.201 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `DIFFERENCE`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.563622`
- **R₃:** `0.51399`
- **R₆:** `0.516024`
- **R₉:** `0.447233`
- **potencjal_kappa:** `-0.196591`
- **masa_semantyczna:** `-0.06476`
- **rodzaj_karty:** `0.313562`


## Rola
Inference gate for deciding when GGUF teacher-validation is needed.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `load_inference_gate_policy`, `gguf_is_advisory`, `decide_gate`

## Opis
Inference gate for deciding when GGUF teacher-validation is needed.
