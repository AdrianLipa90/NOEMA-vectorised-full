# htri_phase_bus.py — build/lib/cielingo/htri_phase_bus.py

## Tożsamość
- **id_karty:** `REPO-HTRI_PHASE_BUS-9C20`
- **ścieżka:** `build/lib/cielingo/htri_phase_bus.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.897`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo/htri_phase_bus.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.897 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `UNCERTAINTY`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.435049`
- **R₃:** `0.572136`
- **R₆:** `0.544042`
- **R₉:** `0.477522`
- **potencjal_kappa:** `0.159902`
- **masa_semantyczna:** `-0.053674`
- **rodzaj_karty:** `0.279085`


## Rola
CIELingo HTRI phase bus.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** PhaseBusNode, PhaseBusReport
- **funkcje:** `_bounded`, `_stable_float`, `_registry_digest`, `_phase_lane`, `_cqcl_variables`, `bind_card_to_phase_bus`, `select_phase_bus_cards`, `phase_bus_report`, `as_dict`, `as_dict`

## Opis
CIELingo HTRI phase bus.

This module binds CIELingo language cards to the shared HTRI phase carrier used
by J-functionals, CQCL-shaped intention variables, NOEMA provenance and
OrchORbital card traces.

It is deliberately a *bus* layer, not a rejection/quarantine layer: cards remain
on the semantic surface and receive a lane/action describing how much phase
assistance they need before heavier inf
