# noema_settings.py — src/ciel_geometry/noema_settings.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_SETTINGS-70E8`
- **ścieżka:** `src/ciel_geometry/noema_settings.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `6.257`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/noema_settings.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 6.257 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

## PhaseNav
- **operator:** `MODAL_PERMISSION`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.453718`
- **R₃:** `0.541785`
- **R₆:** `0.466054`
- **R₉:** `0.529069`
- **potencjal_kappa:** `0.025212`
- **masa_semantyczna:** `0.161862`
- **rodzaj_karty:** `0.285369`


## Rola
NOEMA Settings — hierarchiczny system konfiguracji z walidacją.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** PathsConfig, KuramotoConfig, CielingoSyncConfig, PhaseNavConfig, NeutrinoConfig, ResonanceBridgeConfig, LinuxSensorConfig, NonlocalProxyConfig, SonicConfig, ConsolidatorConfig, PortalConfig, CouplingConfig, MetricsConfig, DaemonsConfig, NoemaSettings
- **funkcje:** `_path`, `validate`, `_default_config_path`, `_deep_merge`, `_resolve_type`, `_from_dict`, `_to_dict`, `load`, `_migrate_v1_to_v2`, `dump`, `save`, `get_settings`

## Opis
NOEMA Settings — hierarchiczny system konfiguracji z walidacją.

Zastępuje rozproszone noema_config.py, ciel_config.py i inne ad-hoc configi.
Jeden punkt prawdy dla wszystkich ustawień NOEMY.

Usage:
    from ciel_geometry.noema_settings import load, validate, dump, NOEMA_DEFAULTS

    settings = load()                    # z domyślnej ścieżki (noema_config.json)
    settings = load("/path/to/conf
