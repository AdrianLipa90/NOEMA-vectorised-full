# rh_pipeline_jfunctional.py — build/bdist.linux-x86_64/wheel/ciel_sot_agent/rh_pipeline_jfunctional.py

## Tożsamość
- **id_karty:** `REPO-RH_PIPELINE_JFUNCTIO-019C`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_sot_agent/rh_pipeline_jfunctional.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.183`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_sot_agent/rh_pipeline_jfunctional.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.183 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
