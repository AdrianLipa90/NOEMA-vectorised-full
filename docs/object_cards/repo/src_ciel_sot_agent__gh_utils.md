# _gh_utils.py — src/ciel_sot_agent/_gh_utils.py

## Tożsamość
- **id_karty:** `REPO-_GH_UTILS-DAD0`
- **ścieżka:** `src/ciel_sot_agent/_gh_utils.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `0.938`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/_gh_utils.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 0.938 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_POSSIBILITY`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.565748`
- **R₃:** `0.628966`
- **R₆:** `0.492583`
- **R₉:** `0.589778`
- **potencjal_kappa:** `0.024081`
- **masa_semantyczna:** `-0.294904`
- **rodzaj_karty:** `0.302592`


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
