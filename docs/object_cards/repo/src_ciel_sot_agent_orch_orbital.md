# orch_orbital.py — src/ciel_sot_agent/orch_orbital.py

## Tożsamość
- **id_karty:** `REPO-ORCH_ORBITAL-B4BA`
- **ścieżka:** `src/ciel_sot_agent/orch_orbital.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `3.743`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/orch_orbital.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 3.743 |
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
