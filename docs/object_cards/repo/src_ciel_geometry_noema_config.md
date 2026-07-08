# noema_config.py — src/ciel_geometry/noema_config.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_CONFIG-E203`
- **ścieżka:** `src/ciel_geometry/noema_config.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `5.613`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/noema_config.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 5.613 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

## PhaseNav
- **operator:** `QUESTION`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.394639`
- **R₃:** `0.763677`
- **R₆:** `0.521308`
- **R₉:** `0.466584`
- **potencjal_kappa:** `-0.203086`
- **masa_semantyczna:** `-0.0017`
- **rodzaj_karty:** `0.305584`


## Rola
Unified configuration for all NOEMA daemons.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** KuramotoConfig, CielingoSyncConfig, NeutrinoConfig, ResonanceBridgeConfig, LinuxSensorConfig, PhaseNavConfig, NonlocalProxyConfig, SonicConfig, ConsolidatorConfig, NoemaConfig
- **funkcje:** `_default_config_path`, `load_config`, `_merge`

## Opis
Unified configuration for all NOEMA daemons.

Usage:
    from ciel_geometry.noema_config import config

    interval = config.kuramoto.interval
    dt = config.kuramoto.dt
