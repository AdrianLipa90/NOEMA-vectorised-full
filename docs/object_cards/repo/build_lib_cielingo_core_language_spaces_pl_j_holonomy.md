# j_holonomy.py — build/lib/cielingo_core/language_spaces/pl/j_holonomy.py

## Tożsamość
- **id_karty:** `REPO-J_HOLONOMY-C1A4`
- **ścieżka:** `build/lib/cielingo_core/language_spaces/pl/j_holonomy.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.522`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo_core/language_spaces/pl/j_holonomy.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.522 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MEMORY`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.481637`
- **R₃:** `0.436994`
- **R₆:** `0.50573`
- **R₉:** `0.517955`
- **potencjal_kappa:** `0.179117`
- **masa_semantyczna:** `0.012321`
- **rodzaj_karty:** `0.236997`


## Rola
Regional J/Kuramoto holonomy guard for CIELingo 0.5J.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** JKuramotoComponent, JKuramotoHolonomyReport
- **funkcje:** `clamp01`, `_component`, `build_pl_kuramoto_holonomy`, `attach_kuramoto_report_to_local_j`, `validate`, `to_dict`, `validate`, `to_dict`

## Opis
Regional J/Kuramoto holonomy guard for CIELingo 0.5J.

Purpose:
- convert local regional grammar pressures into coherent bounded phase
  components;
- preserve the narrow SurfaceSolution ABI by storing a JSON-compatible
  holonomy report inside local_j;
- prevent ad-hoc J fields from drifting away from Kuramoto-style phase
  coupling.

This is not a physical oscillator runtime. It is a semantic-ph
