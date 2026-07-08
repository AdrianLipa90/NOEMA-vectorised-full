# htri_phase_bus.py — src/cielingo/htri_phase_bus.py

## Tożsamość
- **id_karty:** `REPO-HTRI_PHASE_BUS-FB30`
- **ścieżka:** `src/cielingo/htri_phase_bus.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.693`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo/htri_phase_bus.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.693 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CONSENT`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.382156`
- **R₃:** `0.389068`
- **R₆:** `0.420273`
- **R₉:** `0.412754`
- **potencjal_kappa:** `-0.014557`
- **masa_semantyczna:** `0.231183`
- **rodzaj_karty:** `0.291598`


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
