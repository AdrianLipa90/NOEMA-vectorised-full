# _gh_utils.py — build/lib/ciel_sot_agent/_gh_utils.py

## Tożsamość
- **id_karty:** `REPO-_GH_UTILS-4CE7`
- **ścieżka:** `build/lib/ciel_sot_agent/_gh_utils.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.014`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_sot_agent/_gh_utils.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.014 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `UNCERTAINTY`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.435049`
- **R₃:** `0.572136`
- **R₆:** `0.544042`
- **R₉:** `0.477522`
- **potencjal_kappa:** `0.159902`
- **masa_semantyczna:** `-0.053674`
- **rodzaj_karty:** `0.279085`


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
