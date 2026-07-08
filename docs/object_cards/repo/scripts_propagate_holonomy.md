# propagate_holonomy.py — scripts/propagate_holonomy.py

## Tożsamość
- **id_karty:** `REPO-PROPAGATE_HOLONOMY-91F4`
- **ścieżka:** `scripts/propagate_holonomy.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `4.445`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/propagate_holonomy.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 4.445 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `IDENTITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.405566`
- **R₃:** `0.499333`
- **R₆:** `0.494094`
- **R₉:** `0.455981`
- **potencjal_kappa:** `0.08965`
- **masa_semantyczna:** `-0.024381`
- **rodzaj_karty:** `0.279273`


## Rola
Propagate holonomy (winding_n, closure_score) across all TSM entries.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_load`, `_cyclic_dist`, `_local_closure_score`, `main`

## Opis
Propagate holonomy (winding_n, closure_score) across all TSM entries.

Problem: 1831 of 1912 TSM entries have winding_n=0 and closure_score=0.5
because they were ingested but never passed through an orbital cycle.
Without winding/closure variance, holonomic retrieval degrades to random.

Solution: simulate one orbital pass per entry using:
  - phi_berry (already correct from semantic encoder)
  -
