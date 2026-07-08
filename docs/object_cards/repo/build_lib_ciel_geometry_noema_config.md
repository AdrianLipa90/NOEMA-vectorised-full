# noema_config.py — build/lib/ciel_geometry/noema_config.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_CONFIG-F6C6`
- **ścieżka:** `build/lib/ciel_geometry/noema_config.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.869`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_geometry/noema_config.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.869 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ORDER`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.408132`
- **R₃:** `0.527143`
- **R₆:** `0.447287`
- **R₉:** `0.516074`
- **potencjal_kappa:** `0.213299`
- **masa_semantyczna:** `0.199346`
- **rodzaj_karty:** `0.279908`


## Rola
Unified configuration for all NOEMA daemons.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** KuramotoConfig, CielingoSyncConfig, NeutrinoConfig, ResonanceBridgeConfig, LinuxSensorConfig, PhaseNavConfig, NonlocalProxyConfig, SonicConfig, ConsolidatorConfig, NoemaConfig
- **funkcje:** `_default_config_path`, `load_config`, `_merge`

## Opis
Unified configuration for all NOEMA daemons.

Usage:
    from ciel_geometry.noema_config import config

    interval = config.kuramoto.interval
    dt = config.kuramoto.dt
