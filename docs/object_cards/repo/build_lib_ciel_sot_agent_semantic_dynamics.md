# semantic_dynamics.py — build/lib/ciel_sot_agent/semantic_dynamics.py

## Tożsamość
- **id_karty:** `REPO-SEMANTIC_DYNAMICS-1E54`
- **ścieżka:** `build/lib/ciel_sot_agent/semantic_dynamics.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.072`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_sot_agent/semantic_dynamics.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.072 |
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
Information dynamics: Hamiltonian H, Kuramoto step on TSM, timeline vector.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `compute_H`, `kuramoto_step_tsm`, `append_timeline`, `_extract_pipeline_tags`, `last_H_total`

## Opis
Information dynamics: Hamiltonian H, Kuramoto step on TSM, timeline vector.

Faza 4 of the CIEL orbital architecture.

Three functions form the core:
  compute_H        — H_kinetic + H_potential + H_attractor (no arbitrary thresholds)
  kuramoto_step_tsm — one Kuramoto nudge on top-N TSM nodes, persists phi_berry
  append_timeline  — sliding-window timeline.json (max 500 entries)

Called from noem
