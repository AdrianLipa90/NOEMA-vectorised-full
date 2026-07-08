# repair_routing.py — build/bdist.linux-x86_64/wheel/cielingo_core/meaning/repair_routing.py

## Tożsamość
- **id_karty:** `REPO-REPAIR_ROUTING-8CE8`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo_core/meaning/repair_routing.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.998`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo_core/meaning/repair_routing.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.998 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_NECESSITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.449701`
- **R₃:** `0.392905`
- **R₆:** `0.402231`
- **R₉:** `0.439135`
- **potencjal_kappa:** `-0.089486`
- **masa_semantyczna:** `-0.210953`
- **rodzaj_karty:** `0.286192`


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
