# rh_pipeline_jfunctional.py — build/lib/ciel_sot_agent/rh_pipeline_jfunctional.py

## Tożsamość
- **id_karty:** `REPO-RH_PIPELINE_JFUNCTIO-02CE`
- **ścieżka:** `build/lib/ciel_sot_agent/rh_pipeline_jfunctional.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.560`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_sot_agent/rh_pipeline_jfunctional.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.560 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
