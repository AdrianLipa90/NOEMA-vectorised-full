# subsystem_registry.py — build/bdist.linux-x86_64/wheel/ciel_sot_agent/subsystem_registry.py

## Tożsamość
- **id_karty:** `REPO-SUBSYSTEM_REGISTRY-14CA`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_sot_agent/subsystem_registry.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.451`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_sot_agent/subsystem_registry.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.451 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `NEGATION`
- **odcisk_harmoniczny:** `LHLL`
- **R₁:** `0.425094`
- **R₃:** `0.614676`
- **R₆:** `0.450577`
- **R₉:** `0.387679`
- **potencjal_kappa:** `0.085998`
- **masa_semantyczna:** `-0.143065`
- **rodzaj_karty:** `0.271614`


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
