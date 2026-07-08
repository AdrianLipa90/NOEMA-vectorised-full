# decision_bridge.py — src/ciel_geometry/phasenav/decision_bridge.py

## Tożsamość
- **id_karty:** `REPO-DECISION_BRIDGE-83EC`
- **ścieżka:** `src/ciel_geometry/phasenav/decision_bridge.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `5.052`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/phasenav/decision_bridge.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 5.052 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

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
PhaseNav Decision Bridge — decyzje w TaskPlan DB jako operatory 36D.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** —
- **funkcje:** `decision_to_vector`, `decision_to_operator_id`, `vector_to_decisions`, `phase_nav_decide`, `surface_to_decisions`, `decision_to_surface_seed`, `seed_all_decisions`

## Opis
PhaseNav Decision Bridge — decyzje w TaskPlan DB jako operatory 36D.

Każda decyzja ma wektor operatora PhaseNav.
PhaseNav stan surface → automatyczne podejmowanie decyzji.
Decyzje → seed na surface przez operator vector.

Zamiast if/else na thresholdach — connection(stan, decyzja) ∈ [-1, 1].
