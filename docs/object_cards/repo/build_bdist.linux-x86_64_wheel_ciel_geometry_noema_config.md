# noema_config.py — build/bdist.linux-x86_64/wheel/ciel_geometry/noema_config.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_CONFIG-E478`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_geometry/noema_config.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.690`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_geometry/noema_config.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.690 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SOURCE_REQUIRED`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.509375`
- **R₃:** `0.557002`
- **R₆:** `0.453972`
- **R₉:** `0.573802`
- **potencjal_kappa:** `-0.191054`
- **masa_semantyczna:** `-0.307021`
- **rodzaj_karty:** `0.246226`


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
