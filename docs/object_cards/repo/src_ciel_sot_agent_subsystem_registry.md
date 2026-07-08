# subsystem_registry.py — src/ciel_sot_agent/subsystem_registry.py

## Tożsamość
- **id_karty:** `REPO-SUBSYSTEM_REGISTRY-470C`
- **ścieżka:** `src/ciel_sot_agent/subsystem_registry.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `1.835`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/subsystem_registry.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 1.835 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

## PhaseNav
- **operator:** `ATTRACTOR`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.476161`
- **R₃:** `0.526498`
- **R₆:** `0.547584`
- **R₉:** `0.472579`
- **potencjal_kappa:** `4.910705`
- **masa_semantyczna:** `13.031004`
- **rodzaj_karty:** `1.5`


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
