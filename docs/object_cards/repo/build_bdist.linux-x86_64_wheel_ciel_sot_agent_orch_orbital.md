# orch_orbital.py — build/bdist.linux-x86_64/wheel/ciel_sot_agent/orch_orbital.py

## Tożsamość
- **id_karty:** `REPO-ORCH_ORBITAL-848C`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_sot_agent/orch_orbital.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.964`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_sot_agent/orch_orbital.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.964 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CAUSE`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.440841`
- **R₃:** `0.698384`
- **R₆:** `0.560357`
- **R₉:** `0.385177`
- **potencjal_kappa:** `0.165796`
- **masa_semantyczna:** `0.077602`
- **rodzaj_karty:** `0.2472`


## Rola
OrchOrbital — CIEL entity cards reader, orbital metrics exporter,

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `load_entity_cards`, `entity_orbital_summary`, `canonical_entity_id`, `_entity_sector_name`, `_rho_from_theta`, `_card_to_sector_dict`, `_phase_coupling`, `build_entity_injection`, `entity_orbital_metrics`, `run_entity_mini_pass`, `dynamic_adjectives`, `enrich_entity_cards_with_dynamics`

## Opis
OrchOrbital — CIEL entity cards reader, orbital metrics exporter,
and entity sector injector for the orbital bridge.

Loads ciel_entity_cards.yaml and:
  1. Exposes entity coupling/phase metrics for SessionStart context.
  2. Injects entity cards as Sector nodes into the OrbitalSystem,
     enabling their phases and couplings to influence orbital dynamics.

Entity → Sector mapping:
  phi
