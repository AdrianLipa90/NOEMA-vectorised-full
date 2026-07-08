# noema_settings.py — build/lib/ciel_geometry/noema_settings.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_SETTINGS-8871`
- **ścieżka:** `build/lib/ciel_geometry/noema_settings.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.058`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_geometry/noema_settings.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.058 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `AFFECT`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.542195`
- **R₃:** `0.629813`
- **R₆:** `0.534142`
- **R₉:** `0.565106`
- **potencjal_kappa:** `0.141102`
- **masa_semantyczna:** `0.203631`
- **rodzaj_karty:** `0.326785`


## Rola
NOEMA Settings — hierarchiczny system konfiguracji z walidacją.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

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
