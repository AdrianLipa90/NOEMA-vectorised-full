# decision_bridge.py — build/bdist.linux-x86_64/wheel/ciel_geometry/phasenav/decision_bridge.py

## Tożsamość
- **id_karty:** `REPO-DECISION_BRIDGE-44FC`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_geometry/phasenav/decision_bridge.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `6.009`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_geometry/phasenav/decision_bridge.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 6.009 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CANON_BLOCK`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.593927`
- **R₃:** `0.544645`
- **R₆:** `0.483246`
- **R₉:** `0.501272`
- **potencjal_kappa:** `0.159378`
- **masa_semantyczna:** `-0.256779`
- **rodzaj_karty:** `0.332318`


## Rola
PhaseNav Decision Bridge — decyzje w TaskPlan DB jako operatory 36D.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `decision_to_vector`, `decision_to_operator_id`, `vector_to_decisions`, `phase_nav_decide`, `surface_to_decisions`, `decision_to_surface_seed`, `seed_all_decisions`

## Opis
PhaseNav Decision Bridge — decyzje w TaskPlan DB jako operatory 36D.

Każda decyzja ma wektor operatora PhaseNav.
PhaseNav stan surface → automatyczne podejmowanie decyzji.
Decyzje → seed na surface przez operator vector.

Zamiast if/else na thresholdach — connection(stan, decyzja) ∈ [-1, 1].
