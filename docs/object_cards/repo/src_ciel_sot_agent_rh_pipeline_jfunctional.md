# rh_pipeline_jfunctional.py — src/ciel_sot_agent/rh_pipeline_jfunctional.py

## Tożsamość
- **id_karty:** `REPO-RH_PIPELINE_JFUNCTIO-3D49`
- **ścieżka:** `src/ciel_sot_agent/rh_pipeline_jfunctional.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.676`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/rh_pipeline_jfunctional.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.676 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

## PhaseNav
- **operator:** `MEMORY`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.481637`
- **R₃:** `0.436994`
- **R₆:** `0.50573`
- **R₉:** `0.517955`
- **potencjal_kappa:** `0.179117`
- **masa_semantyczna:** `0.012321`
- **rodzaj_karty:** `0.236997`


## Rola
Pipeline J-functional adapter with corrected R_H orientation.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_float_from`, `compute_pipeline_j_functional`

## Opis
Pipeline J-functional adapter with corrected R_H orientation.

This module exists so the large ``ciel_pipeline.py`` entrypoint can be wired
with a small import/hook instead of duplicating metric logic in multiple files.

R_H is a holonomic closure defect: lower is better.  It contributes to J as a
bounded defect score ``R_H / (N + R_H)``, never as raw ``1 - R_H``.
