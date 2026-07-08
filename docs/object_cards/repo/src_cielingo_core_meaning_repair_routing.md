# repair_routing.py — src/cielingo_core/meaning/repair_routing.py

## Tożsamość
- **id_karty:** `REPO-REPAIR_ROUTING-78EE`
- **ścieżka:** `src/cielingo_core/meaning/repair_routing.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.209`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/meaning/repair_routing.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.209 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
MeaningLoop repair-candidate routing v0.7B.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** RepairRouteKind, MeaningRepairCandidate, MeaningRepairRoutingReport
- **funkcje:** `_candidate`, `route_repairs_for_meaning_loop`, `validate`, `to_dict`, `validate`, `to_dict`, `stable_hash`

## Opis
MeaningLoop repair-candidate routing v0.7B.

Maps SemanticScar diagnostics to explicit repair candidates.

Boundary:
- routing suggests repairs; it does not execute them;
- routing does not write NOEMA;
- routing does not update CURRENT;
- routing does not promote SOURCE or canon.
