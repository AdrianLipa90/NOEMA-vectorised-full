# subconscious_bridge.py — src/cielingo_core/bridge/subconscious_bridge.py

## Tożsamość
- **id_karty:** `REPO-SUBCONSCIOUS_BRIDGE-6C58`
- **ścieżka:** `src/cielingo_core/bridge/subconscious_bridge.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.132`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/bridge/subconscious_bridge.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.132 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `PAUSE`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.508756`
- **R₃:** `0.557009`
- **R₆:** `0.421727`
- **R₉:** `0.55292`
- **potencjal_kappa:** `-0.020552`
- **masa_semantyczna:** `0.206252`
- **rodzaj_karty:** `0.260435`


## Rola
SubconsciousBridge — CIELingo ↔ 12D subconscious connection.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** SubconsciousEnrichment, SubconsciousBridge, SubconsciousState
- **funkcje:** `_ott_antonsen`, `_euler_gap`, `_pancharatnam_berry`, `to_inject`, `to_dict`, `feed`, `_interpret`, `enrich_ciel_inject`, `to_dict`, `from_bridge`

## Opis
SubconsciousBridge — CIELingo ↔ 12D subconscious connection.

Takes subconscious oscillator state (11 PhaseNav + 1 agent),
feeds through MeaningLoop + intention_frame, returns enriched
semantic context for AI response generation.

Protocol:
  bridge = SubconsciousBridge()
  result = bridge.feed(subconscious_state, prompt_text)
  # result.subconscious_enrichment -> goes into CIEL inject
