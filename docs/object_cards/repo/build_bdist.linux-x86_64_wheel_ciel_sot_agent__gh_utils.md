# _gh_utils.py — build/bdist.linux-x86_64/wheel/ciel_sot_agent/_gh_utils.py

## Tożsamość
- **id_karty:** `REPO-_GH_UTILS-3757`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_sot_agent/_gh_utils.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.663`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_sot_agent/_gh_utils.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.663 |
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
Shared GitHub API utilities for the coupling subsystems.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** UpstreamConfig
- **funkcje:** `wrap_angle`, `_github_json`, `fetch_head`, `load_upstreams`, `load_runtime_state`, `propagate_phase_changes`

## Opis
Shared GitHub API utilities for the coupling subsystems.

Provides the ``UpstreamConfig`` dataclass, HTTP helpers, upstream loading,
runtime-state loading, and the phase-propagation algorithm that are shared
between ``gh_coupling`` (v1) and ``gh_coupling_v2``.
