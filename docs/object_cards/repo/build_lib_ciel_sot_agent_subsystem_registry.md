# subsystem_registry.py — build/lib/ciel_sot_agent/subsystem_registry.py

## Tożsamość
- **id_karty:** `REPO-SUBSYSTEM_REGISTRY-01A5`
- **ścieżka:** `build/lib/ciel_sot_agent/subsystem_registry.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.859`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_sot_agent/subsystem_registry.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.859 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `IDENTITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.405566`
- **R₃:** `0.499333`
- **R₆:** `0.494094`
- **R₉:** `0.455981`
- **potencjal_kappa:** `0.08965`
- **masa_semantyczna:** `-0.024381`
- **rodzaj_karty:** `0.279273`


## Rola
SubsystemRegistry — zarządza per-subsystem DB i kartami NOEMA.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_rho_from_theta`, `_init_db`, `_write_noema_card`, `_write_defaults`, `init_subsystem`, `init_all`, `write_metric`, `read_latest_metrics`, `status`, `get_noema_cards`

## Opis
SubsystemRegistry — zarządza per-subsystem DB i kartami NOEMA.

Każdy subsystem Poziomu 1 (CORE) dostaje:
  - integration/subsystems/{id}/state.db   — SQLite: metrics, events, config_defaults
  - integration/subsystems/{id}/noema_card.json
  - integration/subsystems/{id}/defaults.json

Usage:
    python -m ciel_sot_agent.subsystem_registry --init-all
    python -m ciel_sot_agent.subsystem_registry
