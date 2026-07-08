# semantic_dynamics.py — src/ciel_sot_agent/semantic_dynamics.py

## Tożsamość
- **id_karty:** `REPO-SEMANTIC_DYNAMICS-66C5`
- **ścieżka:** `src/ciel_sot_agent/semantic_dynamics.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `5.011`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/semantic_dynamics.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 5.011 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

## PhaseNav
- **operator:** `ADDITION`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.662589`
- **R₃:** `0.614656`
- **R₆:** `0.542851`
- **R₉:** `0.417608`
- **potencjal_kappa:** `0.07638`
- **masa_semantyczna:** `0.206164`
- **rodzaj_karty:** `0.259027`


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
